"""Standard test cases for benchmarking collective creativity."""

from typing import Dict, List

BENCHMARK_PROMPTS: Dict[str, List[str]] = {
    "divergent_thinking": [
        "Invent a new color that doesn't exist",
        "Design a musical instrument for underwater use",
    ],
    "philosophical": [
        "What would a world without time look like?",
        "How might consciousness exist without memory?",
    ],
    "practical_creative": [
        "Design a city for 1 million people on Mars",
        "Create a new form of democratic governance",
    ],
    "artistic": [
        "Describe a painting that captures the feeling of nostalgia for a place you've never been",
        "Write an opening line for a novel about the last library on Earth",
    ],
    "problem_solving": [
        "How might we eliminate loneliness in modern cities?",
        "Design an education system for the year 2100",
    ],
}


def get_all_prompts() -> List[str]:
    """Get all benchmark prompts as a flat list."""
    prompts = []
    for category_prompts in BENCHMARK_PROMPTS.values():
        prompts.extend(category_prompts)
    return prompts


def get_category_prompts(category: str) -> List[str]:
    """Get prompts for a specific category."""
    if category not in BENCHMARK_PROMPTS:
        raise ValueError(
            f"Unknown category: {category}. "
            f"Available categories: {list(BENCHMARK_PROMPTS.keys())}"
        )
    return BENCHMARK_PROMPTS[category]


def get_categories() -> List[str]:
    """Get list of all categories."""
    return list(BENCHMARK_PROMPTS.keys())
