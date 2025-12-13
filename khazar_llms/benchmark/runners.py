"""Benchmark runner for executing full benchmark suites."""

from typing import List, Optional
from pathlib import Path

from ..orchestration.ensemble import Ensemble
from .evaluator import BenchmarkEvaluator, FullBenchmarkReport
from .reporters import MarkdownReporter, JSONReporter, HTMLReporter
from .test_cases import get_categories


class BenchmarkRunner:
    """Orchestrates full benchmark execution."""

    def __init__(self, ensemble: Ensemble):
        """
        Initialize benchmark runner.
        
        Args:
            ensemble: The ensemble to benchmark
        """
        self.ensemble = ensemble
        self.evaluator = BenchmarkEvaluator(ensemble)

    async def run(
        self,
        categories: Optional[List[str]] = None,
        iterations: int = 3,
        prompts_per_category: Optional[int] = None,
    ) -> FullBenchmarkReport:
        """
        Run a complete benchmark.
        
        Args:
            categories: List of categories to test (None = all)
            iterations: Number of iterations for ensemble
            prompts_per_category: Limit prompts per category (None = all)
            
        Returns:
            FullBenchmarkReport with complete results
        """
        # Set ensemble iterations
        original_iterations = self.ensemble.max_iterations
        self.ensemble.max_iterations = iterations

        try:
            # Run the full benchmark
            report = await self.evaluator.run_full_benchmark(
                categories=categories,
                prompts_per_category=prompts_per_category,
            )
            
            return report
        finally:
            # Restore original iterations
            self.ensemble.max_iterations = original_iterations

    async def run_single(self, prompt: str, category: str = "custom") -> FullBenchmarkReport:
        """
        Run benchmark on a single custom prompt.
        
        Args:
            prompt: The creative task prompt
            category: Category label for the prompt
            
        Returns:
            FullBenchmarkReport with single result
        """
        result = await self.evaluator.evaluate(prompt, category)
        
        # Create a report with single result
        report = FullBenchmarkReport(
            results=[result],
            category_scores={category: result.overall_score},
            overall_metrics={
                mr.name: mr.score for mr in result.metric_results
            },
            overall_score=result.overall_score,
            metadata=result.metadata,
        )
        
        return report

    def save_report(
        self,
        report: FullBenchmarkReport,
        output_path: Path,
        format: str = "markdown",
    ) -> Path:
        """
        Save benchmark report to file.
        
        Args:
            report: The benchmark report to save
            output_path: Path to save the report
            format: Output format ('markdown', 'json', or 'html')
            
        Returns:
            Path to saved report
        """
        if format == "markdown":
            return MarkdownReporter.save(report, output_path)
        elif format == "json":
            return JSONReporter.save(report, output_path)
        elif format == "html":
            return HTMLReporter.save(report, output_path)
        else:
            raise ValueError(f"Unknown format: {format}. Use 'markdown', 'json', or 'html'")

    def print_summary(self, report: FullBenchmarkReport):
        """Print a summary of benchmark results to console."""
        print("\n" + "=" * 80)
        print("KHAZAR LLMs BENCHMARK RESULTS")
        print("=" * 80)
        print(f"\nOverall Score: {report.overall_score:.1f} / 100 ({report.get_summary()['overall_grade']})")
        print(f"Total Tests: {len(report.results)}")
        print(f"Timestamp: {report.timestamp}")
        
        print("\nMetric Breakdown:")
        print("-" * 80)
        for metric_name, score in report.overall_metrics.items():
            from .evaluator import MetricResult
            grade = MetricResult(name="temp", score=score, description="").grade
            print(f"  {metric_name:.<50} {score:>6.1f} ({grade})")
        
        print("\nCategory Performance:")
        print("-" * 80)
        for category, score in sorted(report.category_scores.items()):
            from .evaluator import MetricResult
            grade = MetricResult(name="temp", score=score, description="").grade
            category_name = category.replace('_', ' ').title()
            print(f"  {category_name:.<50} {score:>6.1f} ({grade})")
        
        print("\n" + "=" * 80 + "\n")
