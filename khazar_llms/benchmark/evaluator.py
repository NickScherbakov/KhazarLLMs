"""Evaluation engine for running benchmarks."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from ..orchestration.ensemble import Ensemble
from ..agents.base import Message
from .metrics import (
    Metric,
    DiversityMetric,
    SynthesisQualityMetric,
    CreativeTensionMetric,
    EmergenceMetric,
    ConvergenceMetric,
    RoleAdherenceMetric,
)
from .test_cases import BENCHMARK_PROMPTS, get_all_prompts


def calculate_grade(score: float) -> str:
    """
    Convert numeric score to letter grade.
    
    Args:
        score: Numeric score between 0 and 100
        
    Returns:
        Letter grade (A+ to F)
    """
    if score >= 95:
        return "A+"
    elif score >= 90:
        return "A"
    elif score >= 87:
        return "A-"
    elif score >= 83:
        return "B+"
    elif score >= 80:
        return "B"
    elif score >= 77:
        return "B-"
    elif score >= 73:
        return "C+"
    elif score >= 70:
        return "C"
    elif score >= 67:
        return "C-"
    elif score >= 63:
        return "D+"
    elif score >= 60:
        return "D"
    else:
        return "F"


@dataclass
class MetricResult:
    """Result for a single metric."""
    name: str
    score: float
    description: str
    grade: str = ""

    def __post_init__(self):
        """Calculate grade after initialization."""
        if not self.grade:
            self.grade = calculate_grade(self.score)


@dataclass
class BenchmarkResult:
    """Result for a single benchmark evaluation."""
    prompt: str
    category: str
    conversation: List[Message]
    metric_results: List[MetricResult]
    overall_score: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the benchmark result."""
        return {
            "prompt": self.prompt,
            "category": self.category,
            "overall_score": self.overall_score,
            "overall_grade": calculate_grade(self.overall_score),
            "metrics": {
                result.name: {
                    "score": result.score,
                    "grade": result.grade,
                }
                for result in self.metric_results
            },
            "timestamp": self.timestamp,
        }


@dataclass
class FullBenchmarkReport:
    """Complete benchmark report across all test cases."""
    results: List[BenchmarkResult]
    category_scores: Dict[str, float]
    overall_metrics: Dict[str, float]
    overall_score: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the full benchmark."""
        return {
            "overall_score": self.overall_score,
            "overall_grade": calculate_grade(self.overall_score),
            "category_scores": self.category_scores,
            "metric_averages": self.overall_metrics,
            "num_tests": len(self.results),
            "timestamp": self.timestamp,
        }


class BenchmarkEvaluator:
    """Engine for evaluating ensemble creativity."""

    def __init__(self, ensemble: Ensemble, metrics: Optional[List[Metric]] = None):
        """
        Initialize the benchmark evaluator.
        
        Args:
            ensemble: The ensemble to evaluate
            metrics: List of metrics to use (defaults to all standard metrics)
        """
        self.ensemble = ensemble
        self.metrics = metrics or [
            DiversityMetric(),
            SynthesisQualityMetric(),
            CreativeTensionMetric(),
            EmergenceMetric(),
            ConvergenceMetric(),
            RoleAdherenceMetric(),
        ]

    async def evaluate(self, prompt: str, category: str = "general") -> BenchmarkResult:
        """
        Run a single evaluation.
        
        Args:
            prompt: The creative task prompt
            category: Category of the prompt
            
        Returns:
            BenchmarkResult with scores for all metrics
        """
        # Run the ensemble on the prompt
        results = await self.ensemble.collaborate(prompt)
        conversation = results["conversation"]

        # Calculate all metrics
        metric_results = []
        for metric in self.metrics:
            score = metric.calculate(conversation, prompt)
            metric_results.append(
                MetricResult(
                    name=metric.get_name(),
                    score=score,
                    description=metric.get_description(),
                )
            )

        # Calculate overall score
        overall_score = sum(mr.score for mr in metric_results) / len(metric_results)

        # Create metadata
        metadata = {
            "ensemble_mode": self.ensemble.mode.value,
            "num_agents": len(self.ensemble.agents),
            "num_iterations": self.ensemble.max_iterations,
            "conversation_length": len(conversation),
            "agent_names": [agent.name for agent in self.ensemble.agents],
        }

        return BenchmarkResult(
            prompt=prompt,
            category=category,
            conversation=conversation,
            metric_results=metric_results,
            overall_score=overall_score,
            metadata=metadata,
        )

    async def run_full_benchmark(
        self,
        categories: Optional[List[str]] = None,
        prompts_per_category: Optional[int] = None,
    ) -> FullBenchmarkReport:
        """
        Run all standard test cases.
        
        Args:
            categories: List of categories to test (None = all)
            prompts_per_category: Limit prompts per category (None = all)
            
        Returns:
            FullBenchmarkReport with results across all tests
        """
        results = []
        
        # Determine which categories to test
        test_categories = categories or list(BENCHMARK_PROMPTS.keys())
        
        # Run benchmarks for each category
        for category in test_categories:
            prompts = BENCHMARK_PROMPTS.get(category, [])
            
            # Limit prompts if requested
            if prompts_per_category:
                prompts = prompts[:prompts_per_category]
            
            for prompt in prompts:
                result = await self.evaluate(prompt, category)
                results.append(result)

        # Calculate category scores
        category_scores = {}
        for category in test_categories:
            category_results = [r for r in results if r.category == category]
            if category_results:
                avg_score = sum(r.overall_score for r in category_results) / len(category_results)
                category_scores[category] = avg_score

        # Calculate overall metric averages
        overall_metrics = {}
        if results:
            for metric in self.metrics:
                metric_name = metric.get_name()
                metric_scores = [
                    mr.score
                    for result in results
                    for mr in result.metric_results
                    if mr.name == metric_name
                ]
                if metric_scores:
                    overall_metrics[metric_name] = sum(metric_scores) / len(metric_scores)

        # Calculate overall score
        overall_score = sum(r.overall_score for r in results) / len(results) if results else 0.0

        # Create metadata
        metadata = {
            "ensemble_mode": self.ensemble.mode.value,
            "num_agents": len(self.ensemble.agents),
            "num_iterations": self.ensemble.max_iterations,
            "agent_names": [agent.name for agent in self.ensemble.agents],
            "categories_tested": test_categories,
            "total_prompts": len(results),
        }

        return FullBenchmarkReport(
            results=results,
            category_scores=category_scores,
            overall_metrics=overall_metrics,
            overall_score=overall_score,
            metadata=metadata,
        )
