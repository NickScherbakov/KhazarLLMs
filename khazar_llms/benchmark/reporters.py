"""Report generators for benchmark results."""

import json
from typing import Dict, Any
from pathlib import Path
from datetime import datetime

from .evaluator import BenchmarkResult, FullBenchmarkReport, MetricResult, calculate_grade


class MarkdownReporter:
    """Generate Markdown reports from benchmark results."""

    @staticmethod
    def generate(report: FullBenchmarkReport) -> str:
        """Generate a Markdown report."""
        md = []
        
        # Header
        md.append("# KhazarLLMs Benchmark Report")
        md.append("")
        md.append(f"**Generated:** {report.timestamp}")
        md.append(f"**Ensemble Mode:** {report.metadata.get('ensemble_mode', 'N/A')}")
        md.append(f"**Agents:** {', '.join(report.metadata.get('agent_names', []))}")
        md.append(f"**Total Tests:** {len(report.results)}")
        md.append("")
        
        # Summary Table
        md.append("## Overall Summary")
        md.append("")
        md.append("| Metric | Score | Grade |")
        md.append("|--------|-------|-------|")
        
        for metric_name, score in report.overall_metrics.items():
            grade = calculate_grade(score)
            md.append(f"| {metric_name} | {score:.1f} | {grade} |")
        
        md.append("")
        md.append(f"**Overall Score: {report.overall_score:.1f} / 100 ({report.get_summary()['overall_grade']})**")
        md.append("")
        
        # Category Scores
        md.append("## Category Performance")
        md.append("")
        md.append("| Category | Score | Grade |")
        md.append("|----------|-------|-------|")
        
        for category, score in sorted(report.category_scores.items()):
            grade = calculate_grade(score)
            md.append(f"| {category} | {score:.1f} | {grade} |")
        
        md.append("")
        
        # Detailed Results
        md.append("## Detailed Results by Category")
        md.append("")
        
        # Group results by category
        by_category: Dict[str, list] = {}
        for result in report.results:
            if result.category not in by_category:
                by_category[result.category] = []
            by_category[result.category].append(result)
        
        for category in sorted(by_category.keys()):
            md.append(f"### {category.replace('_', ' ').title()}")
            md.append("")
            
            for result in by_category[category]:
                md.append(f"#### Prompt: {result.prompt}")
                md.append("")
                md.append(f"**Overall Score:** {result.overall_score:.1f} ({result.get_summary()['overall_grade']})")
                md.append("")
                md.append("| Metric | Score | Grade |")
                md.append("|--------|-------|-------|")
                
                for mr in result.metric_results:
                    md.append(f"| {mr.name} | {mr.score:.1f} | {mr.grade} |")
                
                md.append("")
        
        # Methodology
        md.append("## Methodology")
        md.append("")
        md.append("This benchmark evaluates collective AI creativity across six core metrics:")
        md.append("")
        md.append("- **Diversity Score**: Semantic diversity across agent responses")
        md.append("- **Synthesis Quality**: How well ideas are integrated into synthesis")
        md.append("- **Creative Tension Index**: Productive disagreement and debate quality")
        md.append("- **Emergence Score**: Novel ideas that emerged from collaboration")
        md.append("- **Convergence Rate**: Speed and quality of reaching consensus")
        md.append("- **Role Adherence**: How well agents maintain their designated roles")
        md.append("")
        md.append("Each metric is scored 0-100, with letter grades assigned:")
        md.append("- A+ (95-100), A (90-94), A- (87-89)")
        md.append("- B+ (83-86), B (80-82), B- (77-79)")
        md.append("- C+ (73-76), C (70-72), C- (67-69)")
        md.append("- D+ (63-66), D (60-62)")
        md.append("- F (0-59)")
        md.append("")
        
        return "\n".join(md)

    @staticmethod
    def save(report: FullBenchmarkReport, filepath: Path) -> Path:
        """Save report to Markdown file."""
        content = MarkdownReporter.generate(report)
        filepath.write_text(content)
        return filepath


class JSONReporter:
    """Generate JSON reports from benchmark results."""

    @staticmethod
    def generate(report: FullBenchmarkReport) -> str:
        """Generate a JSON report."""
        data = {
            "timestamp": report.timestamp,
            "overall_score": report.overall_score,
            "overall_grade": report.get_summary()["overall_grade"],
            "metadata": report.metadata,
            "overall_metrics": report.overall_metrics,
            "category_scores": report.category_scores,
            "results": [
                {
                    "prompt": result.prompt,
                    "category": result.category,
                    "overall_score": result.overall_score,
                    "overall_grade": result.get_summary()["overall_grade"],
                    "metrics": [
                        {
                            "name": mr.name,
                            "score": mr.score,
                            "grade": mr.grade,
                            "description": mr.description,
                        }
                        for mr in result.metric_results
                    ],
                    "metadata": result.metadata,
                    "timestamp": result.timestamp,
                }
                for result in report.results
            ],
        }
        
        return json.dumps(data, indent=2)

    @staticmethod
    def save(report: FullBenchmarkReport, filepath: Path) -> Path:
        """Save report to JSON file."""
        content = JSONReporter.generate(report)
        filepath.write_text(content)
        return filepath


class HTMLReporter:
    """Generate HTML reports from benchmark results."""

    @staticmethod
    def generate(report: FullBenchmarkReport) -> str:
        """Generate an HTML report."""
        html = []
        
        # HTML header
        html.append("<!DOCTYPE html>")
        html.append("<html lang='en'>")
        html.append("<head>")
        html.append("  <meta charset='UTF-8'>")
        html.append("  <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html.append("  <title>KhazarLLMs Benchmark Report</title>")
        html.append("  <style>")
        html.append(HTMLReporter._get_css())
        html.append("  </style>")
        html.append("</head>")
        html.append("<body>")
        
        # Header
        html.append("  <div class='container'>")
        html.append("    <header>")
        html.append("      <h1>🎭 KhazarLLMs Benchmark Report</h1>")
        html.append(f"      <p class='subtitle'>Generated: {report.timestamp}</p>")
        html.append("    </header>")
        
        # Overall Summary
        html.append("    <section class='summary'>")
        html.append("      <h2>Overall Summary</h2>")
        html.append(f"      <div class='score-box'>")
        html.append(f"        <div class='score-value'>{report.overall_score:.1f}</div>")
        html.append(f"        <div class='score-grade'>{report.get_summary()['overall_grade']}</div>")
        html.append(f"      </div>")
        html.append("    </section>")
        
        # Metrics Table
        html.append("    <section class='metrics'>")
        html.append("      <h2>Metric Breakdown</h2>")
        html.append("      <table>")
        html.append("        <thead>")
        html.append("          <tr>")
        html.append("            <th>Metric</th>")
        html.append("            <th>Score</th>")
        html.append("            <th>Grade</th>")
        html.append("          </tr>")
        html.append("        </thead>")
        html.append("        <tbody>")
        
        for metric_name, score in report.overall_metrics.items():
            grade = calculate_grade(score)
            grade_class = HTMLReporter._grade_class(grade)
            html.append("          <tr>")
            html.append(f"            <td>{metric_name}</td>")
            html.append(f"            <td>{score:.1f}</td>")
            html.append(f"            <td class='{grade_class}'>{grade}</td>")
            html.append("          </tr>")
        
        html.append("        </tbody>")
        html.append("      </table>")
        html.append("    </section>")
        
        # Category Performance
        html.append("    <section class='categories'>")
        html.append("      <h2>Category Performance</h2>")
        html.append("      <table>")
        html.append("        <thead>")
        html.append("          <tr>")
        html.append("            <th>Category</th>")
        html.append("            <th>Score</th>")
        html.append("            <th>Grade</th>")
        html.append("          </tr>")
        html.append("        </thead>")
        html.append("        <tbody>")
        
        for category, score in sorted(report.category_scores.items()):
            grade = calculate_grade(score)
            grade_class = HTMLReporter._grade_class(grade)
            html.append("          <tr>")
            html.append(f"            <td>{category.replace('_', ' ').title()}</td>")
            html.append(f"            <td>{score:.1f}</td>")
            html.append(f"            <td class='{grade_class}'>{grade}</td>")
            html.append("          </tr>")
        
        html.append("        </tbody>")
        html.append("      </table>")
        html.append("    </section>")
        
        # Metadata
        html.append("    <section class='metadata'>")
        html.append("      <h2>Configuration</h2>")
        html.append("      <ul>")
        html.append(f"        <li><strong>Ensemble Mode:</strong> {report.metadata.get('ensemble_mode', 'N/A')}</li>")
        html.append(f"        <li><strong>Agents:</strong> {', '.join(report.metadata.get('agent_names', []))}</li>")
        html.append(f"        <li><strong>Total Tests:</strong> {len(report.results)}</li>")
        html.append(f"        <li><strong>Iterations:</strong> {report.metadata.get('num_iterations', 'N/A')}</li>")
        html.append("      </ul>")
        html.append("    </section>")
        
        # Footer
        html.append("    <footer>")
        html.append("      <p>Generated by KhazarLLMs Benchmark System</p>")
        html.append("    </footer>")
        html.append("  </div>")
        html.append("</body>")
        html.append("</html>")
        
        return "\n".join(html)

    @staticmethod
    def _get_css() -> str:
        """Get CSS styles for HTML report."""
        return """
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
      background: #f5f5f5;
    }
    .container {
      background: white;
      padding: 40px;
      border-radius: 10px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    header {
      text-align: center;
      margin-bottom: 40px;
      border-bottom: 3px solid #4CAF50;
      padding-bottom: 20px;
    }
    h1 {
      color: #2c3e50;
      margin: 0;
      font-size: 2.5em;
    }
    .subtitle {
      color: #7f8c8d;
      margin: 10px 0 0 0;
    }
    section {
      margin: 40px 0;
    }
    h2 {
      color: #34495e;
      border-left: 4px solid #4CAF50;
      padding-left: 15px;
      margin-bottom: 20px;
    }
    .score-box {
      text-align: center;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 30px;
      border-radius: 10px;
      margin: 20px 0;
    }
    .score-value {
      font-size: 4em;
      font-weight: bold;
      margin: 0;
    }
    .score-grade {
      font-size: 2em;
      margin: 10px 0 0 0;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }
    th, td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }
    th {
      background: #34495e;
      color: white;
      font-weight: bold;
    }
    tr:hover {
      background: #f5f5f5;
    }
    .grade-a { color: #27ae60; font-weight: bold; }
    .grade-b { color: #3498db; font-weight: bold; }
    .grade-c { color: #f39c12; font-weight: bold; }
    .grade-d { color: #e67e22; font-weight: bold; }
    .grade-f { color: #e74c3c; font-weight: bold; }
    .metadata ul {
      list-style: none;
      padding: 0;
    }
    .metadata li {
      padding: 10px;
      background: #ecf0f1;
      margin: 5px 0;
      border-radius: 5px;
    }
    footer {
      text-align: center;
      margin-top: 60px;
      padding-top: 20px;
      border-top: 1px solid #ddd;
      color: #7f8c8d;
    }
        """

    @staticmethod
    def _grade_class(grade: str) -> str:
        """Get CSS class for grade."""
        if grade.startswith('A'):
            return 'grade-a'
        elif grade.startswith('B'):
            return 'grade-b'
        elif grade.startswith('C'):
            return 'grade-c'
        elif grade.startswith('D'):
            return 'grade-d'
        else:
            return 'grade-f'

    @staticmethod
    def save(report: FullBenchmarkReport, filepath: Path) -> Path:
        """Save report to HTML file."""
        content = HTMLReporter.generate(report)
        filepath.write_text(content)
        return filepath
