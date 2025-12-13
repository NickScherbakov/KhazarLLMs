# KhazarLLMs Benchmark System

## Overview

The KhazarLLMs Benchmark is the **world's first comprehensive framework for measuring collective AI creativity**. Unlike traditional benchmarks that evaluate individual AI models, this system measures how well multiple AI agents collaborate to produce creative outputs.

## Vision

This benchmark positions KhazarLLMs as both an academic and industry standard for multi-agent creative systems. It provides:

- **Quantitative metrics** for collective creativity
- **Reproducible methodology** for research
- **Comparison framework** for different configurations
- **Scientific rigor** for multi-agent AI evaluation

## Core Metrics

The benchmark evaluates six fundamental dimensions of collective creativity:

### 1. Diversity Score (0-100)

**What it measures:** Semantic diversity across agent responses

**Why it matters:** Creative collaboration requires diverse perspectives. If all agents say similar things, there's no benefit to having multiple agents.

**Methodology:**
- Uses TF-IDF vectorization and cosine similarity (when sklearn available)
- Calculates pairwise similarity between agent responses within iterations
- Diversity = 1 - average_similarity
- Fallback: Unique word ratio for simple diversity measurement

**Interpretation:**
- **80-100:** Exceptional diversity - agents bring truly unique perspectives
- **60-79:** Good diversity - healthy range of viewpoints
- **40-59:** Moderate diversity - some overlap expected
- **0-39:** Low diversity - possible groupthink or role confusion

**Optimal range:** 60-85 (too much diversity can lead to chaos)

### 2. Synthesis Quality (0-100)

**What it measures:** How well the final synthesis incorporates diverse viewpoints

**Why it matters:** A good synthesis doesn't just pick one idea - it integrates multiple perspectives into something coherent and comprehensive.

**Methodology:**
- Extracts key concepts from early messages (original ideas)
- Extracts concepts from synthesis messages (final output)
- Calculates coverage ratio: what % of original ideas appear in synthesis
- Evaluates coherence based on synthesis length and structure
- Combined score: 70% coverage + 30% coherence

**Interpretation:**
- **90-100:** Excellent synthesis - comprehensive and coherent
- **70-89:** Good synthesis - most ideas integrated
- **50-69:** Adequate synthesis - some ideas missed
- **0-49:** Poor synthesis - many ideas lost or incoherent

**Optimal range:** 70-90

### 3. Creative Tension Index (0-100)

**What it measures:** Productive disagreement and debate quality

**Why it matters:** Creative breakthroughs often come from constructive conflict. Too much agreement can mean no critical thinking; too much conflict can be unproductive.

**Methodology:**
- Detects challenge/disagreement keywords (however, but, disagree, question, etc.)
- Detects resolution keywords (combine, integrate, synthesis, balance, etc.)
- Normalizes by conversation length
- Scores balance between challenge and resolution

**Interpretation:**
- **80-100:** Excellent tension - strong debate with good resolution
- **60-79:** Good tension - healthy disagreement
- **40-59:** Moderate tension - some challenge present
- **0-39:** Low tension - insufficient critical engagement

**Optimal range:** 60-80 (balance is key)

### 4. Emergence Score (0-100)

**What it measures:** Novel ideas that emerged from collaboration

**Why it matters:** This captures the "whole greater than sum of parts" phenomenon - ideas that no single agent had but emerged from their interaction.

**Methodology:**
- Splits conversation into early (first 50%) and late (last 50%) phases
- Extracts concepts and word pairs (bigrams) from each phase
- Emergent concepts = concepts in late phase but not in early phase
- Calculates emergence ratio normalized to 30-50% optimal range
- Combines concept emergence (60%) and bigram emergence (40%)

**Interpretation:**
- **70-100:** Exceptional emergence - collaboration creating new ideas
- **50-69:** Good emergence - clear collaborative benefit
- **30-49:** Moderate emergence - some new ideas
- **0-29:** Low emergence - mostly recombination of existing ideas

**Optimal range:** 40-70 (some continuity expected)

### 5. Convergence Rate (0-100)

**What it measures:** Speed and quality of reaching meaningful consensus

**Why it matters:** Efficient collaboration reaches good conclusions without too many iterations. Too fast can mean shallow exploration; too slow can mean inefficiency.

**Methodology:**
- Tracks convergence indicators (agreement, consensus, synthesis words)
- Measures trend: are convergence indicators increasing over iterations?
- Evaluates speed: fewer iterations is better (optimal: 3-5)
- Combined score: 60% trend quality + 40% speed

**Interpretation:**
- **90-100:** Excellent convergence - fast and high quality
- **70-89:** Good convergence - efficient collaboration
- **50-69:** Moderate convergence - acceptable pace
- **0-49:** Poor convergence - too slow or low quality

**Optimal range:** 70-90

### 6. Role Adherence Score (0-100)

**What it measures:** How well each agent maintains its designated persona

**Why it matters:** If agents don't maintain distinct roles, the ensemble loses its multi-perspective advantage. Role clarity ensures diverse contributions.

**Methodology:**
- Defines role-specific keywords for each agent type:
  - Dreamer: imagine, creative, vision, possibility
  - Critic: critique, flaw, challenge, analyze
  - Synthesizer: combine, integrate, harmonize
  - Philosopher: meaning, purpose, wisdom, profound
  - Rebel: radical, disrupt, challenge, unconventional
  - Architect: structure, framework, system, design
  - Poet: beauty, metaphor, emotional, lyrical
- Counts keyword occurrences in each agent's messages
- Normalizes by message length (keywords per 100 words)
- Optimal: 2-5 role keywords per 100 words

**Interpretation:**
- **90-100:** Excellent adherence - strong role differentiation
- **75-89:** Good adherence - clear role identity
- **60-74:** Moderate adherence - some role blending
- **0-59:** Poor adherence - roles indistinct

**Optimal range:** 75-95

## Standard Test Cases

The benchmark includes 10 carefully designed prompts across 5 categories:

### Divergent Thinking
Tests ability to generate unconventional ideas
- "Invent a new color that doesn't exist"
- "Design a musical instrument for underwater use"

### Philosophical
Tests deep reasoning and meaning-making
- "What would a world without time look like?"
- "How might consciousness exist without memory?"

### Practical Creative
Tests applied creativity to real challenges
- "Design a city for 1 million people on Mars"
- "Create a new form of democratic governance"

### Artistic
Tests aesthetic and emotional creativity
- "Describe a painting that captures the feeling of nostalgia for a place you've never been"
- "Write an opening line for a novel about the last library on Earth"

### Problem Solving
Tests collaborative problem-solving
- "How might we eliminate loneliness in modern cities?"
- "Design an education system for the year 2100"

## Usage

### Command Line Interface

Run full benchmark suite:
```bash
python -m khazar_llms.cli benchmark --full
```

Run specific category:
```bash
python -m khazar_llms.cli benchmark --category philosophical
```

Run single custom prompt:
```bash
python -m khazar_llms.cli benchmark --prompt "Design a new language"
```

Save results in different formats:
```bash
# Save as Markdown
python -m khazar_llms.cli benchmark --full --output results.md

# Save as JSON
python -m khazar_llms.cli benchmark --full --output results.json --format json

# Save as HTML
python -m khazar_llms.cli benchmark --full --output results.html --format html
```

### Python API

```python
from khazar_llms.agents.personas import DreamerAgent, CriticAgent, SynthesizerAgent
from khazar_llms.orchestration.ensemble import Ensemble, ConversationMode
from khazar_llms.benchmark import BenchmarkRunner

# Create ensemble
agents = [
    DreamerAgent(provider="mock"),
    CriticAgent(provider="mock"),
    SynthesizerAgent(provider="mock"),
]

ensemble = Ensemble(
    agents=agents,
    mode=ConversationMode.SEQUENTIAL,
    max_iterations=3,
)

# Run benchmark
runner = BenchmarkRunner(ensemble)
report = await runner.run(iterations=3)

# Print summary
runner.print_summary(report)

# Save report
runner.save_report(report, Path("report.md"), format="markdown")
```

## Report Formats

### Markdown
Human-readable format with tables and grades. Perfect for documentation and README files.

### JSON
Machine-readable format for programmatic analysis. Includes all raw data and metadata.

### HTML
Beautiful web-viewable format with styling and colors. Great for presentations and sharing.

## Interpreting Results

### Overall Scores and Grades

- **A+ (95-100):** Exceptional collective creativity - research-grade performance
- **A (90-94):** Excellent collaboration - production-ready quality
- **A- (87-89):** Very good performance - strong multi-agent synergy
- **B+ (83-86):** Good creative synergy - effective collaboration
- **B (80-82):** Solid collaboration - meets expectations
- **C+ (70-79):** Adequate but improvable - consider optimization
- **D+ (60-69):** Needs improvement - review configuration
- **F (0-59):** Poor collaboration - significant issues

### What to Optimize

**If Diversity is low:**
- Add agents with more distinct roles
- Increase temperature settings
- Try debate or parallel modes

**If Synthesis Quality is low:**
- Add or strengthen Synthesizer agent
- Increase iterations
- Try consensus mode

**If Creative Tension is low:**
- Add Critic or Rebel agents
- Try debate mode
- Increase iterations for more interaction

**If Emergence is low:**
- Increase iterations
- Try parallel or debate modes
- Add more diverse agent roles

**If Convergence is low:**
- Check if iterations are sufficient
- Try sequential or consensus modes
- Add Synthesizer or Architect agents

**If Role Adherence is low:**
- Review agent system prompts
- Reduce temperature (makes agents more consistent)
- Ensure agent roles are well-differentiated

## Academic Use

### Citation

If you use this benchmark in academic work, please cite:

```
KhazarLLMs Collective Creativity Benchmark
Repository: https://github.com/NickScherbakov/KhazarLLMs
```

### Research Applications

- **Multi-agent AI research:** Compare different agent configurations
- **Creativity studies:** Measure collective creative processes
- **Human-AI collaboration:** Understand multi-perspective systems
- **AI evaluation:** Benchmark ensemble AI systems
- **Educational research:** Study collaborative learning in AI

### Reproducibility

All benchmarks include:
- Complete conversation transcripts
- Agent configurations
- Timestamps
- Ensemble settings
- Raw metric scores

This ensures full reproducibility for scientific research.

## Adding Custom Metrics

You can extend the benchmark with custom metrics:

```python
from khazar_llms.benchmark.metrics import Metric
from khazar_llms.agents.base import Message

class MyCustomMetric(Metric):
    def get_name(self) -> str:
        return "My Custom Metric"
    
    def get_description(self) -> str:
        return "Description of what this measures"
    
    def calculate(self, conversation: List[Message], task: str) -> float:
        # Your metric logic here
        score = 0.0  # Calculate score 0-100
        return score

# Use in evaluator
from khazar_llms.benchmark import BenchmarkEvaluator

evaluator = BenchmarkEvaluator(
    ensemble,
    metrics=[
        DiversityMetric(),
        MyCustomMetric(),  # Add your custom metric
    ]
)
```

## Dependencies

### Required
- `numpy>=1.20.0` - For statistical calculations

### Optional
- `scikit-learn>=1.0.0` - For advanced similarity metrics (TF-IDF, cosine similarity)

If scikit-learn is not available, the system falls back to simpler similarity calculations. Results will be consistent but potentially less sophisticated.

## Performance

- **Mock mode:** ~1 second per prompt (no API calls)
- **OpenAI/Anthropic mode:** ~30-60 seconds per prompt (depends on API speed)
- **Full benchmark (10 prompts):** 
  - Mock: ~10 seconds
  - Real LLMs: ~5-10 minutes

## Limitations

1. **Subjective interpretation:** Some creativity aspects are inherently subjective
2. **Language-dependent:** Currently optimized for English
3. **Context-dependent:** Scores depend on task complexity
4. **Snapshot measurement:** Captures one moment, not long-term trends

## Future Enhancements

Potential additions for future versions:

- [ ] Multi-language support
- [ ] Temporal analysis (how creativity evolves over time)
- [ ] Cross-cultural creativity metrics
- [ ] Human evaluation integration
- [ ] Automated hyperparameter optimization
- [ ] Comparative benchmarking against other systems
- [ ] Real-time visualization of metrics during collaboration

## Support

For questions, issues, or contributions:
- GitHub Issues: https://github.com/NickScherbakov/KhazarLLMs/issues
- Documentation: https://github.com/NickScherbakov/KhazarLLMs

## License

This benchmark system is part of the KhazarLLMs project and follows the same license.
