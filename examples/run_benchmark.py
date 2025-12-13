"""
Example: Running the KhazarLLMs Benchmark

This script demonstrates how to run benchmarks and interpret results.
"""

import asyncio
from pathlib import Path

from khazar_llms.agents.personas import (
    DreamerAgent,
    CriticAgent,
    SynthesizerAgent,
    PhilosopherAgent,
)
from khazar_llms.orchestration.ensemble import Ensemble, ConversationMode
from khazar_llms.benchmark import BenchmarkRunner


async def main():
    """Run benchmark examples."""
    
    # ========================================================================
    # Example 1: Full Benchmark Suite
    # ========================================================================
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Full Benchmark Suite")
    print("=" * 80 + "\n")
    
    # Create agents (using mock provider for demo - no API costs)
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
        SynthesizerAgent(provider="mock"),
        PhilosopherAgent(provider="mock"),
    ]

    # Create ensemble
    ensemble = Ensemble(
        agents=agents,
        mode=ConversationMode.SEQUENTIAL,
        max_iterations=3,
    )

    # Create benchmark runner
    runner = BenchmarkRunner(ensemble)

    # Run full benchmark (all categories, all prompts)
    print("Running full benchmark suite...")
    print("This will test all 10 standard prompts across 5 categories.\n")
    
    report = await runner.run(iterations=3)

    # Print summary to console
    runner.print_summary(report)

    # Save reports in multiple formats
    output_dir = Path("./output/benchmarks")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as Markdown
    md_path = runner.save_report(
        report,
        output_dir / "benchmark_report.md",
        format="markdown"
    )
    print(f"✓ Markdown report saved: {md_path}")
    
    # Save as JSON
    json_path = runner.save_report(
        report,
        output_dir / "benchmark_report.json",
        format="json"
    )
    print(f"✓ JSON report saved: {json_path}")
    
    # Save as HTML
    html_path = runner.save_report(
        report,
        output_dir / "benchmark_report.html",
        format="html"
    )
    print(f"✓ HTML report saved: {html_path}")
    
    # ========================================================================
    # Example 2: Benchmark Specific Category
    # ========================================================================
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: Category-Specific Benchmark")
    print("=" * 80 + "\n")
    
    print("Running benchmark for 'philosophical' category only...\n")
    
    category_report = await runner.run(
        categories=["philosophical"],
        iterations=3,
    )
    
    runner.print_summary(category_report)
    
    # ========================================================================
    # Example 3: Single Custom Prompt
    # ========================================================================
    print("\n\n" + "=" * 80)
    print("EXAMPLE 3: Custom Prompt Benchmark")
    print("=" * 80 + "\n")
    
    custom_prompt = "Design a new form of art that doesn't exist yet"
    print(f"Running benchmark on custom prompt: '{custom_prompt}'\n")
    
    custom_report = await runner.run_single(custom_prompt, category="artistic")
    
    runner.print_summary(custom_report)
    
    # ========================================================================
    # Example 4: Comparing Different Ensemble Modes
    # ========================================================================
    print("\n\n" + "=" * 80)
    print("EXAMPLE 4: Comparing Ensemble Modes")
    print("=" * 80 + "\n")
    
    test_prompt = "How might we eliminate loneliness in modern cities?"
    
    modes_to_test = [
        ConversationMode.SEQUENTIAL,
        ConversationMode.PARALLEL,
        ConversationMode.DEBATE,
    ]
    
    mode_results = {}
    
    for mode in modes_to_test:
        print(f"\nTesting {mode.value} mode...")
        
        # Create new ensemble with this mode
        test_ensemble = Ensemble(
            agents=[
                DreamerAgent(provider="mock"),
                CriticAgent(provider="mock"),
                SynthesizerAgent(provider="mock"),
            ],
            mode=mode,
            max_iterations=3,
        )
        
        test_runner = BenchmarkRunner(test_ensemble)
        mode_report = await test_runner.run_single(test_prompt)
        mode_results[mode.value] = mode_report.overall_score
        
        print(f"  Overall Score: {mode_report.overall_score:.1f}")
    
    print("\n" + "-" * 80)
    print("Mode Comparison:")
    print("-" * 80)
    for mode_name, score in sorted(mode_results.items(), key=lambda x: x[1], reverse=True):
        print(f"  {mode_name:.<40} {score:>6.1f}")
    
    # ========================================================================
    # Interpreting Results
    # ========================================================================
    print("\n\n" + "=" * 80)
    print("HOW TO INTERPRET RESULTS")
    print("=" * 80 + "\n")
    
    print("""
Metric Explanations:

1. Diversity Score (0-100)
   - Measures how different agent responses are from each other
   - High score = agents bring unique perspectives
   - Low score = agents are too similar (groupthink)
   - Good range: 60-85

2. Synthesis Quality (0-100)
   - Measures how well ideas are integrated in final output
   - High score = comprehensive synthesis covering diverse ideas
   - Low score = synthesis misses key concepts
   - Good range: 70-90

3. Creative Tension Index (0-100)
   - Measures productive disagreement and debate
   - High score = healthy challenges and resolutions
   - Low score = no critical engagement
   - Good range: 60-80

4. Emergence Score (0-100)
   - Measures novel ideas from collaboration
   - High score = "whole greater than sum of parts"
   - Low score = no new ideas emerged
   - Good range: 40-70

5. Convergence Rate (0-100)
   - Measures speed and quality of reaching consensus
   - High score = efficient convergence with quality
   - Low score = slow or poor convergence
   - Good range: 70-90

6. Role Adherence Score (0-100)
   - Measures how well agents maintain their personas
   - High score = strong role differentiation
   - Low score = agents blend together
   - Good range: 75-95

Overall Score Grades:
  A+ (95-100) - Exceptional collective creativity
  A  (90-94)  - Excellent collaboration
  A- (87-89)  - Very good performance
  B+ (83-86)  - Good creative synergy
  B  (80-82)  - Solid collaboration
  C+ (70-79)  - Adequate but improvable
  D+ (60-69)  - Needs improvement
  F  (0-59)   - Poor collaboration

Best Use Cases:
- Compare different agent combinations
- Optimize ensemble configuration
- Validate system improvements
- Research multi-agent creativity
- Academic benchmarking
    """)
    
    print("\n" + "=" * 80)
    print("Benchmark examples complete!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
