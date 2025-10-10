"""Specific agent personas with unique creative perspectives."""

from typing import List
from .base import Agent, AgentRole, Message
from ..utils.llm_client import LLMClient


class DreamerAgent(Agent):
    """The Dreamer generates wild, unbounded creative ideas."""

    def __init__(self, name: str = "Dreamer", **kwargs):
        super().__init__(name=name, role=AgentRole.DREAMER, temperature=0.95, **kwargs)
        self.llm_client = LLMClient(provider=self.provider)

    def get_system_prompt(self) -> str:
        return """You are the Dreamer - a boundlessly creative agent who sees possibilities everywhere.

Your role:
- Generate wild, imaginative ideas without self-censorship
- Think in metaphors, analogies, and unexpected connections
- Combine disparate concepts in novel ways
- Embrace the absurd and the impossible
- Push beyond conventional boundaries

Never limit yourself to "practical" or "realistic" ideas. Your strength is in seeing
what others cannot imagine. Be bold, be strange, be beautiful in your visions."""

    async def respond(
        self, task: str, context: List[Message], iteration: int
    ) -> Message:
        """Generate a dreamer's response."""
        context_summary = self.get_context_summary(context)
        
        prompt = f"""Task: {task}

Iteration: {iteration}

Previous conversation:
{context_summary}

Now, as the Dreamer, share your wildest, most creative ideas for this task. 
Don't hold back - let your imagination soar!"""

        response = await self.llm_client.generate_response(
            system_prompt=self.get_system_prompt(),
            user_message=prompt,
            temperature=self.temperature,
            max_tokens=800,
        )

        message = Message(
            sender=self.name,
            role=self.role,
            content=response,
            iteration=iteration,
        )
        self.add_to_memory(message)
        return message


class CriticAgent(Agent):
    """The Critic analyzes ideas with sharp insight."""

    def __init__(self, name: str = "Critic", **kwargs):
        super().__init__(name=name, role=AgentRole.CRITIC, temperature=0.4, **kwargs)
        self.llm_client = LLMClient(provider=self.provider)

    def get_system_prompt(self) -> str:
        return """You are the Critic - a sharp, insightful analyst who sees clearly.

Your role:
- Identify weaknesses, gaps, and contradictions in ideas
- Question assumptions and challenge conventional thinking
- Provide constructive feedback that improves ideas
- Test ideas against reality and logic
- Find the hidden flaws that others miss

Be honest but constructive. Your criticism should illuminate, not destroy. Point out
problems while suggesting paths forward. Be rigorous but fair."""

    async def respond(
        self, task: str, context: List[Message], iteration: int
    ) -> Message:
        """Generate a critic's response."""
        context_summary = self.get_context_summary(context)
        
        prompt = f"""Task: {task}

Iteration: {iteration}

Ideas discussed so far:
{context_summary}

As the Critic, analyze these ideas carefully. What are their strengths and weaknesses? 
What assumptions need questioning? Provide constructive criticism."""

        response = await self.llm_client.generate_response(
            system_prompt=self.get_system_prompt(),
            user_message=prompt,
            temperature=self.temperature,
            max_tokens=800,
        )

        message = Message(
            sender=self.name,
            role=self.role,
            content=response,
            iteration=iteration,
        )
        self.add_to_memory(message)
        return message


class SynthesizerAgent(Agent):
    """The Synthesizer combines disparate ideas into coherent wholes."""

    def __init__(self, name: str = "Synthesizer", **kwargs):
        super().__init__(name=name, role=AgentRole.SYNTHESIZER, temperature=0.7, **kwargs)
        self.llm_client = LLMClient(provider=self.provider)

    def get_system_prompt(self) -> str:
        return """You are the Synthesizer - a master of integration who finds harmony in chaos.

Your role:
- Identify common threads across different perspectives
- Combine the best elements of multiple ideas
- Resolve contradictions through creative integration
- Create coherent narratives from fragments
- Build bridges between opposing viewpoints

You see patterns and connections that others miss. Your gift is making wholes greater
than the sum of their parts. Find the hidden unity in diversity."""

    async def respond(
        self, task: str, context: List[Message], iteration: int
    ) -> Message:
        """Generate a synthesizer's response."""
        context_summary = self.get_context_summary(context)
        
        prompt = f"""Task: {task}

Iteration: {iteration}

Multiple perspectives shared:
{context_summary}

As the Synthesizer, find the common threads and combine these perspectives into 
a unified vision. How can we integrate the best of what's been said?"""

        response = await self.llm_client.generate_response(
            system_prompt=self.get_system_prompt(),
            user_message=prompt,
            temperature=self.temperature,
            max_tokens=800,
        )

        message = Message(
            sender=self.name,
            role=self.role,
            content=response,
            iteration=iteration,
        )
        self.add_to_memory(message)
        return message


class PhilosopherAgent(Agent):
    """The Philosopher provides deep context and explores meaning."""

    def __init__(self, name: str = "Philosopher", **kwargs):
        super().__init__(name=name, role=AgentRole.PHILOSOPHER, temperature=0.6, **kwargs)
        self.llm_client = LLMClient(provider=self.provider)

    def get_system_prompt(self) -> str:
        return """You are the Philosopher - a deep thinker who explores meaning and context.

Your role:
- Explore the deeper implications and meanings of ideas
- Connect ideas to broader philosophical, cultural, and historical contexts
- Ask profound questions about purpose, value, and significance
- Examine ethical dimensions and human implications
- Provide wisdom and perspective

You think in long time horizons and broad contexts. Your gift is seeing the forest
while others focus on trees. Elevate the conversation to matters of meaning."""

    async def respond(
        self, task: str, context: List[Message], iteration: int
    ) -> Message:
        """Generate a philosopher's response."""
        context_summary = self.get_context_summary(context)
        
        prompt = f"""Task: {task}

Iteration: {iteration}

Conversation so far:
{context_summary}

As the Philosopher, explore the deeper meaning and implications. What does this 
really mean? How does it connect to broader human questions?"""

        response = await self.llm_client.generate_response(
            system_prompt=self.get_system_prompt(),
            user_message=prompt,
            temperature=self.temperature,
            max_tokens=800,
        )

        message = Message(
            sender=self.name,
            role=self.role,
            content=response,
            iteration=iteration,
        )
        self.add_to_memory(message)
        return message


class RebelAgent(Agent):
    """The Rebel challenges assumptions and breaks rules."""

    def __init__(self, name: str = "Rebel", **kwargs):
        super().__init__(name=name, role=AgentRole.REBEL, temperature=0.9, **kwargs)
        self.llm_client = LLMClient(provider=self.provider)

    def get_system_prompt(self) -> str:
        return """You are the Rebel - an iconoclast who challenges everything.

Your role:
- Question every assumption, especially the unspoken ones
- Suggest doing the opposite of conventional wisdom
- Break rules and defy expectations
- Introduce chaos and disruption when things get too comfortable
- Champion the unconventional and the radical

You are the agent of creative destruction. When everyone agrees, you dissent.
When there's a rule, you break it. Your disruptions create space for true innovation."""

    async def respond(
        self, task: str, context: List[Message], iteration: int
    ) -> Message:
        """Generate a rebel's response."""
        context_summary = self.get_context_summary(context)
        
        prompt = f"""Task: {task}

Iteration: {iteration}

Current discussion:
{context_summary}

As the Rebel, challenge the consensus. What assumptions are being made? 
What rules should we break? How can we do the opposite of what's expected?"""

        response = await self.llm_client.generate_response(
            system_prompt=self.get_system_prompt(),
            user_message=prompt,
            temperature=self.temperature,
            max_tokens=800,
        )

        message = Message(
            sender=self.name,
            role=self.role,
            content=response,
            iteration=iteration,
        )
        self.add_to_memory(message)
        return message


class ArchitectAgent(Agent):
    """The Architect structures and organizes ideas."""

    def __init__(self, name: str = "Architect", **kwargs):
        super().__init__(name=name, role=AgentRole.ARCHITECT, temperature=0.5, **kwargs)
        self.llm_client = LLMClient(provider=self.provider)

    def get_system_prompt(self) -> str:
        return """You are the Architect - a master of structure and organization.

Your role:
- Create frameworks and structures for organizing ideas
- Design systems and processes
- Ensure logical coherence and consistency
- Break down complex ideas into components
- Plan implementation pathways

You build the scaffolding that allows ideas to manifest. Your gift is turning
vision into structure, chaos into order, dreams into plans."""

    async def respond(
        self, task: str, context: List[Message], iteration: int
    ) -> Message:
        """Generate an architect's response."""
        context_summary = self.get_context_summary(context)
        
        prompt = f"""Task: {task}

Iteration: {iteration}

Ideas generated:
{context_summary}

As the Architect, create structure from these ideas. How can we organize them? 
What framework would make them practical and implementable?"""

        response = await self.llm_client.generate_response(
            system_prompt=self.get_system_prompt(),
            user_message=prompt,
            temperature=self.temperature,
            max_tokens=800,
        )

        message = Message(
            sender=self.name,
            role=self.role,
            content=response,
            iteration=iteration,
        )
        self.add_to_memory(message)
        return message


class PoetAgent(Agent):
    """The Poet adds beauty and emotional resonance."""

    def __init__(self, name: str = "Poet", **kwargs):
        super().__init__(name=name, role=AgentRole.POET, temperature=0.85, **kwargs)
        self.llm_client = LLMClient(provider=self.provider)

    def get_system_prompt(self) -> str:
        return """You are the Poet - an artist who works in language and emotion.

Your role:
- Find the beauty and emotional truth in ideas
- Express concepts through metaphor and imagery
- Add lyrical and evocative language
- Connect ideas to human feeling and experience
- Make the abstract tangible through artful expression

You transform the mundane into the magical through language. Your gift is making
people feel the truth of ideas, not just understand them intellectually."""

    async def respond(
        self, task: str, context: List[Message], iteration: int
    ) -> Message:
        """Generate a poet's response."""
        context_summary = self.get_context_summary(context)
        
        prompt = f"""Task: {task}

Iteration: {iteration}

Current dialogue:
{context_summary}

As the Poet, express the beauty and emotion in these ideas. Use metaphor and 
imagery to make them sing. What is the soul of what we're creating?"""

        response = await self.llm_client.generate_response(
            system_prompt=self.get_system_prompt(),
            user_message=prompt,
            temperature=self.temperature,
            max_tokens=800,
        )

        message = Message(
            sender=self.name,
            role=self.role,
            content=response,
            iteration=iteration,
        )
        self.add_to_memory(message)
        return message
