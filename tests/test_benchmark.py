"""Tests for benchmark system."""

import pytest
from khazar_llms.agents.base import Message, AgentRole
from khazar_llms.agents.personas import DreamerAgent, CriticAgent, SynthesizerAgent
from khazar_llms.orchestration.ensemble import Ensemble, ConversationMode
from khazar_llms.benchmark.metrics import (
    DiversityMetric,
    SynthesisQualityMetric,
    CreativeTensionMetric,
    EmergenceMetric,
    ConvergenceMetric,
    RoleAdherenceMetric,
)
from khazar_llms.benchmark.evaluator import BenchmarkEvaluator, MetricResult
from khazar_llms.benchmark.test_cases import (
    BENCHMARK_PROMPTS,
    get_all_prompts,
    get_category_prompts,
    get_categories,
)
from khazar_llms.benchmark.reporters import (
    MarkdownReporter,
    JSONReporter,
    HTMLReporter,
)
from khazar_llms.benchmark.runners import BenchmarkRunner
from pathlib import Path
import json


# Test Metrics

def test_diversity_metric():
    """Test diversity metric calculation."""
    metric = DiversityMetric()
    
    # Create diverse messages
    messages = [
        Message(sender="A", role=AgentRole.DREAMER, content="The sky is blue and vast", iteration=0),
        Message(sender="B", role=AgentRole.CRITIC, content="Consider the economic implications", iteration=0),
        Message(sender="C", role=AgentRole.POET, content="A river flows through mountains", iteration=0),
    ]
    
    score = metric.calculate(messages, "test task")
    assert 0 <= score <= 100
    assert metric.get_name() == "Diversity Score"
    assert "diversity" in metric.get_description().lower()


def test_diversity_metric_similar_content():
    """Test diversity metric with similar content."""
    metric = DiversityMetric()
    
    # Create similar messages
    messages = [
        Message(sender="A", role=AgentRole.DREAMER, content="This is a test message", iteration=0),
        Message(sender="B", role=AgentRole.CRITIC, content="This is a test message", iteration=0),
    ]
    
    score = metric.calculate(messages, "test task")
    # Similar content should have lower diversity
    assert score < 60


def test_synthesis_quality_metric():
    """Test synthesis quality metric."""
    metric = SynthesisQualityMetric()
    
    messages = [
        Message(sender="A", role=AgentRole.DREAMER, content="Innovation creativity imagination", iteration=0),
        Message(sender="B", role=AgentRole.CRITIC, content="Analysis evaluation critique", iteration=0),
        Message(sender="C", role=AgentRole.SYNTHESIZER, content="Innovation and analysis combined through creativity and evaluation", iteration=1),
    ]
    
    score = metric.calculate(messages, "test task")
    assert 0 <= score <= 100
    assert metric.get_name() == "Synthesis Quality"


def test_creative_tension_metric():
    """Test creative tension metric."""
    metric = CreativeTensionMetric()
    
    messages = [
        Message(sender="A", role=AgentRole.DREAMER, content="This is amazing", iteration=0),
        Message(sender="B", role=AgentRole.CRITIC, content="However I disagree because of flaws", iteration=0),
        Message(sender="C", role=AgentRole.SYNTHESIZER, content="Let's combine and integrate both views", iteration=1),
    ]
    
    score = metric.calculate(messages, "test task")
    assert 0 <= score <= 100
    assert "tension" in metric.get_name().lower()


def test_emergence_metric():
    """Test emergence metric."""
    metric = EmergenceMetric()
    
    messages = [
        Message(sender="A", role=AgentRole.DREAMER, content="Ideas about creativity and innovation", iteration=0),
        Message(sender="B", role=AgentRole.CRITIC, content="Analysis of problems", iteration=0),
        Message(sender="C", role=AgentRole.SYNTHESIZER, content="Synthesis brings transformation and evolution", iteration=1),
    ]
    
    score = metric.calculate(messages, "test task")
    assert 0 <= score <= 100
    assert "emergence" in metric.get_name().lower()


def test_convergence_metric():
    """Test convergence metric."""
    metric = ConvergenceMetric()
    
    messages = [
        Message(sender="A", role=AgentRole.DREAMER, content="Different ideas", iteration=0),
        Message(sender="B", role=AgentRole.CRITIC, content="More different ideas", iteration=0),
        Message(sender="C", role=AgentRole.SYNTHESIZER, content="Now we agree and reach consensus together", iteration=1),
    ]
    
    score = metric.calculate(messages, "test task")
    assert 0 <= score <= 100
    assert "convergence" in metric.get_name().lower()


def test_role_adherence_metric():
    """Test role adherence metric."""
    metric = RoleAdherenceMetric()
    
    messages = [
        Message(sender="Dreamer", role=AgentRole.DREAMER, content="I imagine creative wild boundless possibilities and visions", iteration=0),
        Message(sender="Critic", role=AgentRole.CRITIC, content="However I critique the flaws and analyze the weaknesses", iteration=0),
    ]
    
    score = metric.calculate(messages, "test task")
    assert 0 <= score <= 100
    assert "role" in metric.get_name().lower()


# Test Test Cases

def test_benchmark_prompts_structure():
    """Test that benchmark prompts are properly structured."""
    assert isinstance(BENCHMARK_PROMPTS, dict)
    assert len(BENCHMARK_PROMPTS) == 5
    assert "divergent_thinking" in BENCHMARK_PROMPTS
    assert "philosophical" in BENCHMARK_PROMPTS
    assert "practical_creative" in BENCHMARK_PROMPTS
    assert "artistic" in BENCHMARK_PROMPTS
    assert "problem_solving" in BENCHMARK_PROMPTS


def test_get_all_prompts():
    """Test getting all prompts."""
    prompts = get_all_prompts()
    assert isinstance(prompts, list)
    assert len(prompts) == 10  # 2 prompts per category * 5 categories


def test_get_category_prompts():
    """Test getting prompts for specific category."""
    prompts = get_category_prompts("philosophical")
    assert isinstance(prompts, list)
    assert len(prompts) == 2
    
    with pytest.raises(ValueError):
        get_category_prompts("nonexistent")


def test_get_categories():
    """Test getting all categories."""
    categories = get_categories()
    assert isinstance(categories, list)
    assert len(categories) == 5


# Test Evaluator

def test_metric_result_grading():
    """Test grade calculation."""
    result = MetricResult(name="Test", score=95.0, description="Test metric")
    assert result.grade == "A+"
    
    result = MetricResult(name="Test", score=85.0, description="Test metric")
    assert result.grade == "B+"
    
    result = MetricResult(name="Test", score=50.0, description="Test metric")
    assert result.grade == "F"


@pytest.mark.asyncio
async def test_benchmark_evaluator_single():
    """Test running single evaluation."""
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
    ]
    
    ensemble = Ensemble(agents=agents, max_iterations=2)
    evaluator = BenchmarkEvaluator(ensemble)
    
    result = await evaluator.evaluate("Test prompt", category="test")
    
    assert result.prompt == "Test prompt"
    assert result.category == "test"
    assert len(result.metric_results) == 6  # All 6 metrics
    assert 0 <= result.overall_score <= 100
    assert result.timestamp


@pytest.mark.asyncio
async def test_benchmark_evaluator_full():
    """Test running full benchmark."""
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
        SynthesizerAgent(provider="mock"),
    ]
    
    ensemble = Ensemble(agents=agents, max_iterations=2)
    evaluator = BenchmarkEvaluator(ensemble)
    
    # Run with limited prompts for speed
    report = await evaluator.run_full_benchmark(
        categories=["philosophical"],
        prompts_per_category=1,
    )
    
    assert len(report.results) == 1
    assert "philosophical" in report.category_scores
    assert len(report.overall_metrics) == 6
    assert 0 <= report.overall_score <= 100


# Test Reporters

@pytest.mark.asyncio
async def test_markdown_reporter(tmp_path):
    """Test Markdown reporter."""
    agents = [DreamerAgent(provider="mock"), CriticAgent(provider="mock")]
    ensemble = Ensemble(agents=agents, max_iterations=1)
    evaluator = BenchmarkEvaluator(ensemble)
    
    report = await evaluator.run_full_benchmark(
        categories=["philosophical"],
        prompts_per_category=1,
    )
    
    # Generate markdown
    md_content = MarkdownReporter.generate(report)
    assert "# KhazarLLMs Benchmark Report" in md_content
    assert "Overall Summary" in md_content
    assert "Diversity Score" in md_content
    
    # Save to file
    md_path = tmp_path / "test_report.md"
    saved_path = MarkdownReporter.save(report, md_path)
    assert saved_path.exists()
    assert saved_path.read_text() == md_content


@pytest.mark.asyncio
async def test_json_reporter(tmp_path):
    """Test JSON reporter."""
    agents = [DreamerAgent(provider="mock"), CriticAgent(provider="mock")]
    ensemble = Ensemble(agents=agents, max_iterations=1)
    evaluator = BenchmarkEvaluator(ensemble)
    
    report = await evaluator.run_full_benchmark(
        categories=["philosophical"],
        prompts_per_category=1,
    )
    
    # Generate JSON
    json_content = JSONReporter.generate(report)
    data = json.loads(json_content)
    
    assert "overall_score" in data
    assert "results" in data
    assert "overall_metrics" in data
    assert len(data["results"]) == 1
    
    # Save to file
    json_path = tmp_path / "test_report.json"
    saved_path = JSONReporter.save(report, json_path)
    assert saved_path.exists()
    assert json.loads(saved_path.read_text()) == data


@pytest.mark.asyncio
async def test_html_reporter(tmp_path):
    """Test HTML reporter."""
    agents = [DreamerAgent(provider="mock"), CriticAgent(provider="mock")]
    ensemble = Ensemble(agents=agents, max_iterations=1)
    evaluator = BenchmarkEvaluator(ensemble)
    
    report = await evaluator.run_full_benchmark(
        categories=["philosophical"],
        prompts_per_category=1,
    )
    
    # Generate HTML
    html_content = HTMLReporter.generate(report)
    assert "<!DOCTYPE html>" in html_content
    assert "KhazarLLMs Benchmark Report" in html_content
    assert "Diversity Score" in html_content
    
    # Save to file
    html_path = tmp_path / "test_report.html"
    saved_path = HTMLReporter.save(report, html_path)
    assert saved_path.exists()
    assert saved_path.read_text() == html_content


# Test Runner

@pytest.mark.asyncio
async def test_benchmark_runner_full(tmp_path):
    """Test full benchmark run."""
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
    ]
    
    ensemble = Ensemble(agents=agents, max_iterations=2)
    runner = BenchmarkRunner(ensemble)
    
    # Run limited benchmark
    report = await runner.run(
        categories=["philosophical"],
        iterations=2,
        prompts_per_category=1,
    )
    
    assert len(report.results) == 1
    assert report.overall_score > 0
    
    # Test saving
    md_path = tmp_path / "report.md"
    saved = runner.save_report(report, md_path, format="markdown")
    assert saved.exists()


@pytest.mark.asyncio
async def test_benchmark_runner_single():
    """Test single prompt benchmark."""
    agents = [DreamerAgent(provider="mock"), CriticAgent(provider="mock")]
    ensemble = Ensemble(agents=agents, max_iterations=2)
    runner = BenchmarkRunner(ensemble)
    
    report = await runner.run_single("Test creative prompt", category="test")
    
    assert len(report.results) == 1
    assert report.results[0].prompt == "Test creative prompt"
    assert report.results[0].category == "test"


def test_benchmark_runner_save_formats(tmp_path):
    """Test saving in different formats."""
    from khazar_llms.benchmark.evaluator import FullBenchmarkReport
    
    # Create minimal report
    report = FullBenchmarkReport(
        results=[],
        category_scores={},
        overall_metrics={},
        overall_score=75.0,
    )
    
    agents = [DreamerAgent(provider="mock")]
    ensemble = Ensemble(agents=agents)
    runner = BenchmarkRunner(ensemble)
    
    # Test markdown
    md_path = tmp_path / "test.md"
    saved = runner.save_report(report, md_path, format="markdown")
    assert saved.exists()
    
    # Test JSON
    json_path = tmp_path / "test.json"
    saved = runner.save_report(report, json_path, format="json")
    assert saved.exists()
    
    # Test HTML
    html_path = tmp_path / "test.html"
    saved = runner.save_report(report, html_path, format="html")
    assert saved.exists()
    
    # Test invalid format
    with pytest.raises(ValueError):
        runner.save_report(report, tmp_path / "test.txt", format="invalid")


# Integration Tests

@pytest.mark.asyncio
async def test_full_benchmark_integration():
    """Integration test of full benchmark pipeline."""
    # Create a minimal ensemble
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
        SynthesizerAgent(provider="mock"),
    ]
    
    ensemble = Ensemble(
        agents=agents,
        mode=ConversationMode.SEQUENTIAL,
        max_iterations=2,
    )
    
    # Create runner
    runner = BenchmarkRunner(ensemble)
    
    # Run benchmark on one category
    report = await runner.run(
        categories=["philosophical"],
        iterations=2,
        prompts_per_category=1,
    )
    
    # Verify structure
    assert report.overall_score > 0
    assert len(report.results) == 1
    assert "philosophical" in report.category_scores
    assert len(report.overall_metrics) == 6
    
    # Verify all metrics are present
    metric_names = {
        "Diversity Score",
        "Synthesis Quality",
        "Creative Tension Index",
        "Emergence Score",
        "Convergence Rate",
        "Role Adherence Score",
    }
    assert set(report.overall_metrics.keys()) == metric_names
    
    # Verify each result has all metrics
    for result in report.results:
        result_metric_names = {mr.name for mr in result.metric_results}
        assert result_metric_names == metric_names


@pytest.mark.asyncio
async def test_different_ensemble_modes():
    """Test benchmark with different ensemble modes."""
    modes = [
        ConversationMode.SEQUENTIAL,
        ConversationMode.PARALLEL,
        ConversationMode.DEBATE,
    ]
    
    for mode in modes:
        agents = [
            DreamerAgent(provider="mock"),
            CriticAgent(provider="mock"),
        ]
        
        ensemble = Ensemble(agents=agents, mode=mode, max_iterations=2)
        runner = BenchmarkRunner(ensemble)
        
        report = await runner.run_single("Test prompt")
        
        assert report.overall_score > 0
        assert report.metadata["ensemble_mode"] == mode.value
