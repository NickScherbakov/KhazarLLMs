"""Ensemble management for coordinating multiple agents."""

import asyncio
from typing import List, Dict, Any, Optional
from enum import Enum

from ..agents.base import Agent, Message


class ConversationMode(str, Enum):
    """Different modes for agent conversations."""

    SEQUENTIAL = "sequential"  # Agents speak one after another
    PARALLEL = "parallel"  # Agents respond simultaneously
    DEBATE = "debate"  # Agents engage in structured debate
    CONSENSUS = "consensus"  # Agents work toward agreement


class Ensemble:
    """Manages a collection of agents working together."""

    def __init__(
        self,
        agents: List[Agent],
        mode: ConversationMode = ConversationMode.SEQUENTIAL,
        max_iterations: int = 5,
    ):
        """
        Initialize an ensemble of agents.
        
        Args:
            agents: List of Agent instances to coordinate
            mode: Conversation mode for the ensemble
            max_iterations: Maximum number of conversation rounds
        """
        self.agents = agents
        self.mode = mode
        self.max_iterations = max_iterations
        self.conversation_history: List[Message] = []

    async def run_iteration(
        self, task: str, iteration: int
    ) -> List[Message]:
        """
        Run one iteration of the creative conversation.
        
        Args:
            task: The creative task for agents to work on
            iteration: Current iteration number
            
        Returns:
            List of messages generated in this iteration
        """
        messages = []

        if self.mode == ConversationMode.SEQUENTIAL:
            # Each agent responds in sequence
            for agent in self.agents:
                message = await agent.respond(task, self.conversation_history, iteration)
                self.conversation_history.append(message)
                messages.append(message)

        elif self.mode == ConversationMode.PARALLEL:
            # All agents respond simultaneously
            tasks = [
                agent.respond(task, self.conversation_history, iteration)
                for agent in self.agents
            ]
            responses = await asyncio.gather(*tasks)
            for message in responses:
                self.conversation_history.append(message)
                messages.append(message)

        elif self.mode == ConversationMode.DEBATE:
            # Agents respond in pairs, alternating perspectives
            for i in range(0, len(self.agents), 2):
                if i + 1 < len(self.agents):
                    # Two agents respond
                    agent1, agent2 = self.agents[i], self.agents[i + 1]
                    msg1, msg2 = await asyncio.gather(
                        agent1.respond(task, self.conversation_history, iteration),
                        agent2.respond(task, self.conversation_history, iteration),
                    )
                    self.conversation_history.extend([msg1, msg2])
                    messages.extend([msg1, msg2])
                else:
                    # Odd agent out responds alone
                    message = await self.agents[i].respond(
                        task, self.conversation_history, iteration
                    )
                    self.conversation_history.append(message)
                    messages.append(message)

        elif self.mode == ConversationMode.CONSENSUS:
            # Similar to sequential but agents explicitly try to build consensus
            for agent in self.agents:
                message = await agent.respond(task, self.conversation_history, iteration)
                self.conversation_history.append(message)
                messages.append(message)

        return messages

    async def collaborate(self, task: str) -> Dict[str, Any]:
        """
        Run a full creative collaboration session.
        
        Args:
            task: The creative task for the ensemble to work on
            
        Returns:
            Dictionary containing conversation history and final synthesis
        """
        self.conversation_history = []

        for iteration in range(self.max_iterations):
            await self.run_iteration(task, iteration)

        return {
            "task": task,
            "mode": self.mode,
            "iterations": self.max_iterations,
            "conversation": self.conversation_history,
            "agent_count": len(self.agents),
        }

    def get_agent_by_role(self, role: str) -> Optional[Agent]:
        """Get the first agent with the specified role."""
        for agent in self.agents:
            if agent.role.value == role:
                return agent
        return None

    def add_agent(self, agent: Agent):
        """Add an agent to the ensemble."""
        self.agents.append(agent)

    def remove_agent(self, agent_name: str) -> bool:
        """Remove an agent by name."""
        for i, agent in enumerate(self.agents):
            if agent.name == agent_name:
                del self.agents[i]
                return True
        return False

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the ensemble configuration."""
        return {
            "mode": self.mode,
            "max_iterations": self.max_iterations,
            "agents": [
                {
                    "name": agent.name,
                    "role": agent.role.value,
                    "temperature": agent.temperature,
                }
                for agent in self.agents
            ],
            "conversation_length": len(self.conversation_history),
        }
