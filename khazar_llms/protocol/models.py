"""KPS data models using Pydantic."""

from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
import uuid


class Archetype(str, Enum):
    """Standard KPS archetypes."""
    CREATIVE_VISIONARY = "creative_visionary"
    ANALYTICAL_CHALLENGER = "analytical_challenger"
    INTEGRATIVE_HARMONIZER = "integrative_harmonizer"
    CONTEXTUAL_THINKER = "contextual_thinker"
    DISRUPTIVE_ICONOCLAST = "disruptive_iconoclast"
    STRUCTURAL_ORGANIZER = "structural_organizer"
    AESTHETIC_ARTISAN = "aesthetic_artisan"


class Capability(str, Enum):
    """Standard agent capabilities."""
    GENERATE = "generate"
    RESPOND = "respond"
    SYNTHESIZE = "synthesize"
    CRITIQUE = "critique"
    VOTE = "vote"
    MODERATE = "moderate"


class Provider(str, Enum):
    """LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MOCK = "mock"
    CUSTOM = "custom"


class Persona(BaseModel):
    """Agent persona definition."""
    name: str
    archetype: str  # Allows custom archetypes
    symbol: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r'^#[0-9a-fA-F]{6}$')
    system_prompt: str = Field(..., min_length=10)
    traits: Optional[List[str]] = None
    communication_style: Optional[str] = None


class KPSAgent(BaseModel):
    """KPS-compliant agent definition."""
    agent_id: str
    persona: Persona
    capabilities: List[str]
    provider: str
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=1.0)
    metadata: Optional[Dict[str, Any]] = None

    @staticmethod
    def generate_id(prefix: str = "agent") -> str:
        """Generate a unique agent ID."""
        return f"{prefix}-{uuid.uuid4()}"


class MessageSender(BaseModel):
    """Message sender information."""
    agent_id: str
    persona_name: str


class MessageContent(BaseModel):
    """Message content structure."""
    text: str
    format: str = "plain"
    language: str = "en"


class Intent(str, Enum):
    """Standard message intents."""
    PROPOSE = "propose"
    CHALLENGE = "challenge"
    SUPPORT = "support"
    SYNTHESIZE = "synthesize"
    QUESTION = "question"
    REDIRECT = "redirect"
    CONCLUDE = "conclude"
    ACKNOWLEDGE = "acknowledge"


class MessageMetadata(BaseModel):
    """Message metadata."""
    round: int = Field(..., ge=0)
    turn: int = Field(..., ge=0)
    mode: str
    responding_to: Optional[List[str]] = None
    stage_direction: Optional[str] = None


class MessageAnnotations(BaseModel):
    """Message annotations."""
    sentiment: Optional[str] = None
    intent: str
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)


class KPSMessage(BaseModel):
    """KPS-compliant message."""
    message_id: str
    session_id: str
    timestamp: str  # ISO 8601
    sender: MessageSender
    content: MessageContent
    metadata: MessageMetadata
    annotations: Optional[MessageAnnotations] = None

    @staticmethod
    def generate_id() -> str:
        """Generate a unique message ID."""
        return str(uuid.uuid4())


class SessionState(str, Enum):
    """Session states."""
    INITIALIZED = "INITIALIZED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    RESUMED = "RESUMED"
    SYNTHESIZING = "SYNTHESIZING"
    COMPLETED = "COMPLETED"
    TERMINATED = "TERMINATED"


class Mode(str, Enum):
    """Orchestration modes."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    DEBATE = "debate"
    CONSENSUS = "consensus"


class SynthesisStrategy(str, Enum):
    """Synthesis strategies."""
    FINAL_AGENT = "final_agent"
    VOTING = "voting"
    MERGE = "merge"
    ITERATIVE = "iterative"


class SessionConfig(BaseModel):
    """Session configuration."""
    mode: str
    max_rounds: int = Field(..., ge=1)
    max_tokens_per_turn: Optional[int] = Field(None, ge=1)
    synthesis_strategy: str
    consensus_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    timeout_seconds: Optional[int] = Field(None, ge=1)


class KPSSession(BaseModel):
    """KPS-compliant session."""
    session_id: str
    prompt: str = Field(..., min_length=1)
    state: str
    config: SessionConfig
    participants: List[str] = Field(..., min_length=1)
    created_at: str  # ISO 8601
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    @staticmethod
    def generate_id() -> str:
        """Generate a unique session ID."""
        return str(uuid.uuid4())


class SynthesisContent(BaseModel):
    """Synthesis content."""
    text: str
    format: str = "plain"
    language: str = "en"


class SynthesisMetrics(BaseModel):
    """Synthesis quality metrics."""
    agreement_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    diversity_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    coherence_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class DissentingView(BaseModel):
    """Dissenting perspective in synthesis."""
    agent_id: str
    message_id: str
    summary: str


class KPSSynthesis(BaseModel):
    """KPS-compliant synthesis output."""
    synthesis_id: str
    session_id: str
    strategy: str
    synthesizer_agent_id: Optional[str] = None
    content: SynthesisContent
    sources: List[str] = Field(..., min_length=1)
    metrics: Optional[SynthesisMetrics] = None
    dissenting_views: Optional[List[DissentingView]] = None
    created_at: str  # ISO 8601

    @staticmethod
    def generate_id() -> str:
        """Generate a unique synthesis ID."""
        return str(uuid.uuid4())


class EventType(str, Enum):
    """Standard event types."""
    SESSION_INITIALIZED = "session.initialized"
    SESSION_STARTED = "session.started"
    AGENT_JOINED = "agent.joined"
    AGENT_LEFT = "agent.left"
    TURN_STARTED = "turn.started"
    TURN_COMPLETED = "turn.completed"
    ROUND_STARTED = "round.started"
    ROUND_COMPLETED = "round.completed"
    SYNTHESIS_STARTED = "synthesis.started"
    SYNTHESIS_COMPLETED = "synthesis.completed"
    SESSION_PAUSED = "session.paused"
    SESSION_RESUMED = "session.resumed"
    SESSION_COMPLETED = "session.completed"
    SESSION_TERMINATED = "session.terminated"
    ERROR_OCCURRED = "error.occurred"


class KPSEvent(BaseModel):
    """KPS event."""
    event_type: str
    timestamp: str  # ISO 8601
    session_id: str
    data: Optional[Dict[str, Any]] = None


class ErrorCode(str, Enum):
    """Standard KPS error codes."""
    KPS_001 = "KPS-001"  # Agent Timeout
    KPS_002 = "KPS-002"  # Invalid Message Format
    KPS_003 = "KPS-003"  # Session Not Found
    KPS_004 = "KPS-004"  # Consensus Not Reached
    KPS_005 = "KPS-005"  # Provider Error
    KPS_006 = "KPS-006"  # Invalid Agent Configuration
    KPS_007 = "KPS-007"  # Max Rounds Exceeded
    KPS_008 = "KPS-008"  # Unauthorized Access
    KPS_009 = "KPS-009"  # Invalid Session State
    KPS_010 = "KPS-010"  # Synthesis Failed


class KPSError(BaseModel):
    """KPS error response."""
    code: str = Field(..., pattern=r'^KPS-[0-9]{3}$')
    message: str
    timestamp: str  # ISO 8601
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    recovery_suggestion: Optional[str] = None
