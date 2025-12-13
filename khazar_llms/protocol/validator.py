"""KPS validation module for checking compliance with the protocol."""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import ValidationError
from .models import KPSAgent, KPSMessage, KPSSession, KPSSynthesis


class ValidationResult:
    """Result of a KPS validation check."""

    def __init__(self, valid: bool, errors: Optional[List[str]] = None, warnings: Optional[List[str]] = None):
        self.valid = valid
        self.errors = errors or []
        self.warnings = warnings or []

    def __bool__(self):
        return self.valid

    def __repr__(self):
        status = "VALID" if self.valid else "INVALID"
        error_count = len(self.errors)
        warning_count = len(self.warnings)
        return f"<ValidationResult {status}: {error_count} errors, {warning_count} warnings>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
        }


class KPSValidator:
    """Validates messages, sessions, and agents against KPS specification."""

    def __init__(self, schema_dir: Optional[Path] = None):
        """
        Initialize the validator.
        
        Args:
            schema_dir: Path to directory containing JSON schemas (optional)
        """
        self.schema_dir = schema_dir
        if schema_dir:
            self.schemas = self._load_schemas(schema_dir)
        else:
            self.schemas = {}

    def _load_schemas(self, schema_dir: Path) -> Dict[str, Any]:
        """Load JSON schemas from directory."""
        schemas = {}
        schema_files = {
            "agent": "agent.schema.json",
            "message": "message.schema.json",
            "session": "session.schema.json",
            "synthesis": "synthesis.schema.json",
        }
        
        for key, filename in schema_files.items():
            schema_path = schema_dir / filename
            if schema_path.exists():
                with open(schema_path, "r") as f:
                    schemas[key] = json.load(f)
        
        return schemas

    def validate_agent(self, agent: Dict[str, Any]) -> ValidationResult:
        """
        Validate an agent configuration against KPS specification.
        
        Args:
            agent: Agent configuration as dictionary
            
        Returns:
            ValidationResult indicating validity and any errors
        """
        errors = []
        warnings = []

        try:
            # Validate using Pydantic model
            KPSAgent(**agent)
        except ValidationError as e:
            for error in e.errors():
                field = ".".join(str(x) for x in error["loc"])
                errors.append(f"{field}: {error['msg']}")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        # Additional validation checks
        
        # Check if archetype is standard or custom
        standard_archetypes = [
            "creative_visionary",
            "analytical_challenger",
            "integrative_harmonizer",
            "contextual_thinker",
            "disruptive_iconoclast",
            "structural_organizer",
            "aesthetic_artisan",
        ]
        
        archetype = agent.get("persona", {}).get("archetype", "")
        if archetype not in standard_archetypes:
            warnings.append(f"Using custom archetype: {archetype}")

        # Check capabilities
        standard_capabilities = ["generate", "respond", "synthesize", "critique", "vote", "moderate"]
        for cap in agent.get("capabilities", []):
            if cap not in standard_capabilities:
                warnings.append(f"Using custom capability: {cap}")

        return ValidationResult(valid=True, errors=errors, warnings=warnings)

    def validate_message(self, message: Dict[str, Any]) -> ValidationResult:
        """
        Validate a message against KPS specification.
        
        Args:
            message: Message as dictionary
            
        Returns:
            ValidationResult indicating validity and any errors
        """
        errors = []
        warnings = []

        try:
            # Validate using Pydantic model
            KPSMessage(**message)
        except ValidationError as e:
            for error in e.errors():
                field = ".".join(str(x) for x in error["loc"])
                errors.append(f"{field}: {error['msg']}")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        # Additional validation checks
        
        # Check mode is standard
        standard_modes = ["sequential", "parallel", "debate", "consensus"]
        mode = message.get("metadata", {}).get("mode", "")
        if mode not in standard_modes:
            warnings.append(f"Using custom orchestration mode: {mode}")

        # Check intent is standard
        standard_intents = [
            "propose", "challenge", "support", "synthesize",
            "question", "redirect", "conclude", "acknowledge"
        ]
        intent = message.get("annotations", {}).get("intent", "")
        if intent and intent not in standard_intents:
            warnings.append(f"Using custom intent: {intent}")

        return ValidationResult(valid=True, errors=errors, warnings=warnings)

    def validate_session(self, session: Dict[str, Any]) -> ValidationResult:
        """
        Validate a session configuration against KPS specification.
        
        Args:
            session: Session configuration as dictionary
            
        Returns:
            ValidationResult indicating validity and any errors
        """
        errors = []
        warnings = []

        try:
            # Validate using Pydantic model
            KPSSession(**session)
        except ValidationError as e:
            for error in e.errors():
                field = ".".join(str(x) for x in error["loc"])
                errors.append(f"{field}: {error['msg']}")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        # Additional validation checks
        
        # Validate state transitions
        valid_states = [
            "INITIALIZED", "ACTIVE", "PAUSED", "RESUMED",
            "SYNTHESIZING", "COMPLETED", "TERMINATED"
        ]
        state = session.get("state", "")
        if state not in valid_states:
            errors.append(f"Invalid session state: {state}")

        # Check mode
        standard_modes = ["sequential", "parallel", "debate", "consensus"]
        mode = session.get("config", {}).get("mode", "")
        if mode not in standard_modes:
            warnings.append(f"Using custom orchestration mode: {mode}")

        # Check synthesis strategy
        standard_strategies = ["final_agent", "voting", "merge", "iterative"]
        strategy = session.get("config", {}).get("synthesis_strategy", "")
        if strategy not in standard_strategies:
            warnings.append(f"Using custom synthesis strategy: {strategy}")

        return ValidationResult(valid=True, errors=errors, warnings=warnings)

    def validate_synthesis(self, synthesis: Dict[str, Any]) -> ValidationResult:
        """
        Validate a synthesis output against KPS specification.
        
        Args:
            synthesis: Synthesis output as dictionary
            
        Returns:
            ValidationResult indicating validity and any errors
        """
        errors = []
        warnings = []

        try:
            # Validate using Pydantic model
            KPSSynthesis(**synthesis)
        except ValidationError as e:
            for error in e.errors():
                field = ".".join(str(x) for x in error["loc"])
                errors.append(f"{field}: {error['msg']}")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        # Additional validation checks
        
        # Check synthesis strategy
        standard_strategies = ["final_agent", "voting", "merge", "iterative"]
        strategy = synthesis.get("strategy", "")
        if strategy not in standard_strategies:
            warnings.append(f"Using custom synthesis strategy: {strategy}")

        # Validate that sources is not empty
        sources = synthesis.get("sources", [])
        if not sources:
            errors.append("Synthesis must reference at least one source message")

        return ValidationResult(valid=True, errors=errors, warnings=warnings)

    def validate_session_export(self, export_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate a complete session export.
        
        Args:
            export_data: Complete session export including messages and metadata
            
        Returns:
            ValidationResult indicating validity and any errors
        """
        errors = []
        warnings = []

        # Validate session
        if "session" in export_data:
            session_result = self.validate_session(export_data["session"])
            errors.extend(session_result.errors)
            warnings.extend(session_result.warnings)
        else:
            errors.append("Export must include 'session' field")

        # Validate agents
        if "agents" in export_data:
            for i, agent in enumerate(export_data["agents"]):
                agent_result = self.validate_agent(agent)
                if not agent_result.valid:
                    errors.extend([f"Agent {i}: {e}" for e in agent_result.errors])
                warnings.extend([f"Agent {i}: {w}" for w in agent_result.warnings])
        else:
            warnings.append("Export should include 'agents' field")

        # Validate messages
        if "messages" in export_data:
            for i, message in enumerate(export_data["messages"]):
                msg_result = self.validate_message(message)
                if not msg_result.valid:
                    errors.extend([f"Message {i}: {e}" for e in msg_result.errors])
                warnings.extend([f"Message {i}: {w}" for w in msg_result.warnings])
        else:
            warnings.append("Export should include 'messages' field")

        # Validate synthesis if present
        if "synthesis" in export_data:
            synth_result = self.validate_synthesis(export_data["synthesis"])
            errors.extend(synth_result.errors)
            warnings.extend(synth_result.warnings)

        valid = len(errors) == 0
        return ValidationResult(valid=valid, errors=errors, warnings=warnings)
