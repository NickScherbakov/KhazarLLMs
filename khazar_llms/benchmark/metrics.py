"""Core metrics for measuring collective AI creativity."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import re
from collections import Counter

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from ..agents.base import Message, AgentRole


# Constants for metric calculations
OPTIMAL_EMERGENCE_THRESHOLD = 0.4  # 30-50% emergence is considered very good
STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
    'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this',
    'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
}


class Metric(ABC):
    """Base class for all benchmark metrics."""

    @abstractmethod
    def calculate(self, conversation: List[Message], task: str) -> float:
        """
        Calculate the metric score.
        
        Args:
            conversation: List of messages in the conversation
            task: The original creative task
            
        Returns:
            Score between 0 and 100
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get the metric name."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get a description of what this metric measures."""
        pass


class DiversityMetric(Metric):
    """Measures how different the agents' responses are from each other."""

    def get_name(self) -> str:
        return "Diversity Score"

    def get_description(self) -> str:
        return "Measures semantic diversity across agent responses (0-100)"

    def calculate(self, conversation: List[Message], task: str) -> float:
        """
        Calculate diversity using semantic similarity.
        Higher diversity = agents bring unique perspectives.
        """
        if len(conversation) < 2:
            return 0.0

        # Group messages by iteration to compare agents' responses
        iteration_groups: Dict[int, List[Message]] = {}
        for msg in conversation:
            if msg.iteration not in iteration_groups:
                iteration_groups[msg.iteration] = []
            iteration_groups[msg.iteration].append(msg)

        # Calculate diversity within each iteration
        diversities = []
        for messages in iteration_groups.values():
            if len(messages) < 2:
                continue

            texts = [msg.content for msg in messages]
            
            # Use TF-IDF and cosine similarity if sklearn available
            if SKLEARN_AVAILABLE:
                try:
                    vectorizer = TfidfVectorizer()
                    tfidf_matrix = vectorizer.fit_transform(texts)
                    similarities = cosine_similarity(tfidf_matrix)
                    
                    # Average pairwise similarity
                    n = len(texts)
                    total_similarity = 0
                    count = 0
                    for i in range(n):
                        for j in range(i + 1, n):
                            total_similarity += similarities[i][j]
                            count += 1
                    
                    avg_similarity = total_similarity / count if count > 0 else 0
                    diversity = 1 - avg_similarity
                    diversities.append(diversity)
                except Exception:
                    # Fallback to simple diversity
                    diversities.append(self._simple_diversity(texts))
            else:
                # Fallback method: word overlap
                diversities.append(self._simple_diversity(texts))

        if not diversities:
            return 50.0  # Neutral score if can't calculate

        avg_diversity = sum(diversities) / len(diversities) if diversities else 0.5
        return min(100.0, max(0.0, avg_diversity * 100))

    def _simple_diversity(self, texts: List[str]) -> float:
        """Simple diversity calculation based on unique word ratio."""
        all_words = []
        for text in texts:
            words = re.findall(r'\w+', text.lower())
            all_words.extend(words)
        
        if not all_words:
            return 0.5
        
        unique_ratio = len(set(all_words)) / len(all_words)
        return unique_ratio


class SynthesisQualityMetric(Metric):
    """Measures how well the final synthesis incorporates diverse viewpoints."""

    def get_name(self) -> str:
        return "Synthesis Quality"

    def get_description(self) -> str:
        return "Measures how well the synthesis incorporates diverse ideas (0-100)"

    def calculate(self, conversation: List[Message], task: str) -> float:
        """
        Calculate synthesis quality by checking coverage of ideas.
        """
        if len(conversation) < 2:
            return 0.0

        # Find synthesizer messages (usually in later iterations)
        synthesizer_messages = [
            msg for msg in conversation 
            if msg.role == AgentRole.SYNTHESIZER
        ]
        
        # If no explicit synthesizer, use last 20% of messages
        if not synthesizer_messages:
            cutoff = int(len(conversation) * 0.8)
            synthesizer_messages = conversation[cutoff:]
        
        if not synthesizer_messages:
            return 0.0

        # Earlier messages contain original ideas
        early_messages = [
            msg for msg in conversation 
            if msg not in synthesizer_messages
        ]
        
        if not early_messages:
            return 50.0

        # Extract key concepts from early messages
        early_concepts = self._extract_concepts(early_messages)
        
        # Extract concepts from synthesis
        synthesis_concepts = self._extract_concepts(synthesizer_messages)
        
        # Calculate coverage ratio
        if not early_concepts:
            return 50.0
        
        common_concepts = early_concepts.intersection(synthesis_concepts)
        coverage = len(common_concepts) / len(early_concepts)
        
        # Calculate coherence (length and structure of synthesis)
        synthesis_text = " ".join(msg.content for msg in synthesizer_messages)
        coherence = min(1.0, len(synthesis_text.split()) / 200)  # Expect ~200 words
        
        # Combine coverage and coherence
        quality = (coverage * 0.7 + coherence * 0.3)
        return min(100.0, max(0.0, quality * 100))

    def _extract_concepts(self, messages: List[Message]) -> set:
        """Extract key concepts (important words) from messages."""
        # Simple extraction: nouns and significant words
        text = " ".join(msg.content for msg in messages).lower()
        words = re.findall(r'\w+', text)
        
        # Keep words longer than 4 characters and not stopwords
        concepts = {w for w in words if len(w) > 4 and w not in STOPWORDS}
        return concepts


class CreativeTensionMetric(Metric):
    """Measures productive disagreement between agents."""

    def get_name(self) -> str:
        return "Creative Tension Index"

    def get_description(self) -> str:
        return "Measures productive disagreement and debate quality (0-100)"

    def calculate(self, conversation: List[Message], task: str) -> float:
        """
        Detect contradictions, challenges, and resolution quality.
        """
        if len(conversation) < 2:
            return 0.0

        # Keywords indicating disagreement/challenge
        challenge_words = [
            'however', 'but', 'disagree', 'challenge', 'question', 'alternatively',
            'instead', 'contrary', 'opposite', 'differ', 'critique', 'flaw',
            'weakness', 'problem', 'issue', 'concern', 'doubt', 'skeptical',
        ]
        
        # Keywords indicating resolution
        resolution_words = [
            'combine', 'integrate', 'synthesis', 'together', 'balance', 'merge',
            'unify', 'harmonize', 'resolution', 'agreement', 'common', 'shared',
        ]
        
        total_challenges = 0
        total_resolutions = 0
        
        for msg in conversation:
            content_lower = msg.content.lower()
            
            # Count challenge indicators
            for word in challenge_words:
                total_challenges += content_lower.count(word)
            
            # Count resolution indicators
            for word in resolution_words:
                total_resolutions += content_lower.count(word)
        
        # Normalize based on conversation length
        msg_count = len(conversation)
        challenge_rate = total_challenges / msg_count if msg_count > 0 else 0
        resolution_rate = total_resolutions / msg_count if msg_count > 0 else 0
        
        # Good tension: challenges followed by resolutions
        # Scale: 2-5 challenges and 1-3 resolutions per message = optimal
        challenge_score = min(1.0, challenge_rate / 3.0)  # Cap at 3 per message
        resolution_score = min(1.0, resolution_rate / 2.0)  # Cap at 2 per message
        
        # Balance between challenge and resolution
        tension = (challenge_score * 0.6 + resolution_score * 0.4)
        
        return min(100.0, max(0.0, tension * 100))


class EmergenceMetric(Metric):
    """Measures ideas in the final output that weren't in any individual response."""

    def get_name(self) -> str:
        return "Emergence Score"

    def get_description(self) -> str:
        return "Measures novel ideas that emerged from collaboration (0-100)"

    def calculate(self, conversation: List[Message], task: str) -> float:
        """
        Identify emergent concepts - ideas in later messages not in early ones.
        """
        if len(conversation) < 3:
            return 0.0

        # Split into early (first 50%) and late (last 50%)
        midpoint = len(conversation) // 2
        early_messages = conversation[:midpoint]
        late_messages = conversation[midpoint:]
        
        # Extract concepts from each phase
        early_concepts = self._extract_concepts(early_messages)
        late_concepts = self._extract_concepts(late_messages)
        
        # Emergent concepts = in late but not in early
        emergent = late_concepts - early_concepts
        
        # Also consider evolved concepts (combinations)
        early_bigrams = self._extract_bigrams(early_messages)
        late_bigrams = self._extract_bigrams(late_messages)
        emergent_bigrams = late_bigrams - early_bigrams
        
        # Calculate emergence ratio
        if not late_concepts:
            return 0.0
        
        concept_emergence = len(emergent) / len(late_concepts) if late_concepts else 0
        bigram_emergence = len(emergent_bigrams) / len(late_bigrams) if late_bigrams else 0
        
        # Combine both metrics
        emergence = (concept_emergence * 0.6 + bigram_emergence * 0.4)
        
        # Scale: 30-50% emergence is very good (using OPTIMAL_EMERGENCE_THRESHOLD)
        normalized = min(1.0, emergence / OPTIMAL_EMERGENCE_THRESHOLD)
        
        return min(100.0, max(0.0, normalized * 100))

    def _extract_concepts(self, messages: List[Message]) -> set:
        """Extract key concepts from messages."""
        text = " ".join(msg.content for msg in messages).lower()
        words = re.findall(r'\w+', text)
        
        concepts = {w for w in words if len(w) > 4 and w not in STOPWORDS}
        return concepts

    def _extract_bigrams(self, messages: List[Message]) -> set:
        """Extract word pairs from messages."""
        text = " ".join(msg.content for msg in messages).lower()
        words = re.findall(r'\w+', text)
        
        bigrams = set()
        for i in range(len(words) - 1):
            if len(words[i]) > 3 and len(words[i + 1]) > 3:
                bigrams.add((words[i], words[i + 1]))
        
        return bigrams


class ConvergenceMetric(Metric):
    """Measures how quickly agents reach meaningful consensus."""

    def get_name(self) -> str:
        return "Convergence Rate"

    def get_description(self) -> str:
        return "Measures speed and quality of reaching consensus (0-100)"

    def calculate(self, conversation: List[Message], task: str) -> float:
        """
        Measure iterations to convergence and synthesis quality.
        """
        if len(conversation) < 2:
            return 0.0

        # Group by iteration
        iterations: Dict[int, List[Message]] = {}
        for msg in conversation:
            if msg.iteration not in iterations:
                iterations[msg.iteration] = []
            iterations[msg.iteration].append(msg)
        
        num_iterations = len(iterations)
        
        # Look for convergence indicators over time
        convergence_words = [
            'agree', 'consensus', 'together', 'unified', 'synthesis', 'combine',
            'integration', 'common', 'shared', 'collective', 'joint',
        ]
        
        iteration_convergence = []
        for iter_num in sorted(iterations.keys()):
            messages = iterations[iter_num]
            content = " ".join(msg.content for msg in messages).lower()
            
            convergence_count = sum(content.count(word) for word in convergence_words)
            iteration_convergence.append(convergence_count)
        
        # Convergence should increase over iterations
        if len(iteration_convergence) > 1:
            # Calculate trend (are we converging?)
            trend = 0
            for i in range(1, len(iteration_convergence)):
                if iteration_convergence[i] > iteration_convergence[i-1]:
                    trend += 1
            
            trend_score = trend / (len(iteration_convergence) - 1) if len(iteration_convergence) > 1 else 0
        else:
            trend_score = 0.5
        
        # Speed score: fewer iterations needed = better
        # Optimal: 3-5 iterations
        if num_iterations <= 3:
            speed_score = 1.0
        elif num_iterations <= 5:
            speed_score = 0.8
        else:
            speed_score = max(0.3, 1.0 - (num_iterations - 5) * 0.1)
        
        # Combine trend and speed
        convergence = (trend_score * 0.6 + speed_score * 0.4)
        
        return min(100.0, max(0.0, convergence * 100))


class RoleAdherenceMetric(Metric):
    """Measures how well each agent maintains its persona."""

    def get_name(self) -> str:
        return "Role Adherence Score"

    def get_description(self) -> str:
        return "Measures how well agents maintain their designated roles (0-100)"

    def calculate(self, conversation: List[Message], task: str) -> float:
        """
        Check if agents exhibit their role-specific characteristics.
        """
        if not conversation:
            return 0.0

        # Define keywords for each role
        role_keywords = {
            AgentRole.DREAMER: [
                'imagine', 'dream', 'creative', 'wild', 'possibility', 'vision',
                'fantasy', 'magical', 'wonder', 'unlimited', 'boundless',
            ],
            AgentRole.CRITIC: [
                'however', 'critique', 'flaw', 'weakness', 'problem', 'challenge',
                'question', 'analyze', 'issue', 'concern', 'limitation',
            ],
            AgentRole.SYNTHESIZER: [
                'combine', 'integrate', 'synthesis', 'together', 'merge', 'unify',
                'balance', 'harmonize', 'connect', 'weave', 'blend',
            ],
            AgentRole.PHILOSOPHER: [
                'meaning', 'why', 'purpose', 'essence', 'truth', 'wisdom',
                'profound', 'deeper', 'fundamental', 'existential', 'human',
            ],
            AgentRole.REBEL: [
                'break', 'opposite', 'radical', 'unconventional', 'disrupt',
                'challenge', 'defy', 'rebel', 'alternative', 'revolutionary',
            ],
            AgentRole.ARCHITECT: [
                'structure', 'framework', 'organize', 'system', 'plan', 'design',
                'build', 'construct', 'architecture', 'foundation', 'blueprint',
            ],
            AgentRole.POET: [
                'beauty', 'metaphor', 'poetry', 'lyrical', 'elegant', 'graceful',
                'imagery', 'evocative', 'emotional', 'artistic', 'expressive',
            ],
        }
        
        role_scores = []
        
        # Group messages by agent
        agent_messages: Dict[str, List[Message]] = {}
        for msg in conversation:
            if msg.sender not in agent_messages:
                agent_messages[msg.sender] = []
            agent_messages[msg.sender].append(msg)
        
        # Calculate adherence for each agent
        for agent_name, messages in agent_messages.items():
            if not messages:
                continue
            
            role = messages[0].role
            keywords = role_keywords.get(role, [])
            
            if not keywords:
                continue
            
            # Count keyword occurrences
            total_keywords = 0
            for msg in messages:
                content_lower = msg.content.lower()
                for keyword in keywords:
                    total_keywords += content_lower.count(keyword)
            
            # Normalize by message count and length
            total_words = sum(len(msg.content.split()) for msg in messages)
            if total_words > 0:
                keyword_density = total_keywords / (total_words / 100)  # Per 100 words
                # Good adherence: 2-5 keywords per 100 words
                adherence = min(1.0, keyword_density / 3.0)
                role_scores.append(adherence)
        
        if not role_scores:
            return 50.0  # Neutral if can't calculate
        
        avg_adherence = sum(role_scores) / len(role_scores)
        return min(100.0, max(0.0, avg_adherence * 100))


# List of all available metrics
ALL_METRICS = [
    DiversityMetric,
    SynthesisQualityMetric,
    CreativeTensionMetric,
    EmergenceMetric,
    ConvergenceMetric,
    RoleAdherenceMetric,
]
