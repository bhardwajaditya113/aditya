"""
Base Agent implementation for the Superintelligence Multi-Modal Agentic AI Framework.

This module provides the foundational BaseAgent class that all specialized agents
inherit from, implementing core functionality like message handling, safety checks,
tool integration, and multi-modal processing capabilities.
"""

import asyncio
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Union, AsyncIterator
from enum import Enum
import json
import logging

from ..config import AgentConfig, SafetyLevel
from ..multimodal import MultiModalInput, MultiModalOutput


class MessageType(Enum):
    """Types of messages that can be processed by agents."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    CODE = "code"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    SYSTEM = "system"


class AgentCapability(Enum):
    """Capabilities that agents can have."""
    TEXT_PROCESSING = "text_processing"
    IMAGE_ANALYSIS = "image_analysis"
    AUDIO_PROCESSING = "audio_processing"
    VIDEO_UNDERSTANDING = "video_understanding"
    WEB_SEARCH = "web_search"
    CODE_EXECUTION = "code_execution"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    REASONING = "reasoning"
    PLANNING = "planning"
    SAFETY_MONITORING = "safety_monitoring"


@dataclass
class AgentMessage:
    """Message structure for agent communication."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    message_type: MessageType = MessageType.TEXT
    sender: str = "user"
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Multi-modal content
    images: List[str] = field(default_factory=list)  # URLs or base64
    audio: List[str] = field(default_factory=list)
    videos: List[str] = field(default_factory=list)
    documents: List[str] = field(default_factory=list)
    
    # Tool-related fields
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    tool_results: List[Dict[str, Any]] = field(default_factory=list)
    
    # Context and reasoning
    context: Optional[str] = None
    reasoning_chain: List[str] = field(default_factory=list)
    confidence: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization."""
        return {
            "id": self.id,
            "content": self.content,
            "message_type": self.message_type.value,
            "sender": self.sender,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "images": self.images,
            "audio": self.audio,
            "videos": self.videos,
            "documents": self.documents,
            "tool_calls": self.tool_calls,
            "tool_results": self.tool_results,
            "context": self.context,
            "reasoning_chain": self.reasoning_chain,
            "confidence": self.confidence
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentMessage':
        """Create message from dictionary."""
        data = data.copy()
        data["message_type"] = MessageType(data.get("message_type", "text"))
        data["timestamp"] = datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat()))
        return cls(**data)


@dataclass
class AgentResponse:
    """Response structure from agents."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    agent_name: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    confidence: float = 1.0
    
    # Multi-modal outputs
    generated_images: List[str] = field(default_factory=list)
    generated_audio: List[str] = field(default_factory=list)
    
    # Reasoning and explanation
    reasoning_steps: List[str] = field(default_factory=list)
    tool_calls_made: List[Dict[str, Any]] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    
    # Safety and compliance
    safety_assessment: Dict[str, Any] = field(default_factory=dict)
    constitutional_compliance: bool = True
    harm_score: float = 0.0
    
    # Performance metrics
    processing_time: float = 0.0
    tokens_used: int = 0
    cost_estimate: float = 0.0
    
    # Error handling
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary for serialization."""
        return {
            "id": self.id,
            "content": self.content,
            "agent_name": self.agent_name,
            "timestamp": self.timestamp.isoformat(),
            "confidence": self.confidence,
            "generated_images": self.generated_images,
            "generated_audio": self.generated_audio,
            "reasoning_steps": self.reasoning_steps,
            "tool_calls_made": self.tool_calls_made,
            "sources": self.sources,
            "safety_assessment": self.safety_assessment,
            "constitutional_compliance": self.constitutional_compliance,
            "harm_score": self.harm_score,
            "processing_time": self.processing_time,
            "tokens_used": self.tokens_used,
            "cost_estimate": self.cost_estimate,
            "errors": self.errors,
            "warnings": self.warnings
        }


class BaseAgent(ABC):
    """
    Base class for all agents in the Superintelligence framework.
    
    Provides core functionality including:
    - Message processing and routing
    - Safety checks and constitutional AI
    - Tool integration
    - Multi-modal input/output handling
    - Logging and monitoring
    """
    
    def __init__(self, config: AgentConfig, name: Optional[str] = None):
        """Initialize the base agent."""
        self.config = config
        self.name = name or self.__class__.__name__
        self.agent_id = str(uuid.uuid4())
        
        # Set up logging
        self.logger = logging.getLogger(f"agent.{self.name}")
        self.logger.setLevel(getattr(logging, config.log_level))
        
        # Initialize capabilities
        self.capabilities: List[AgentCapability] = []
        self._initialize_capabilities()
        
        # Message history
        self.message_history: List[AgentMessage] = []
        self.response_history: List[AgentResponse] = []
        
        # Performance tracking
        self.total_tokens_used = 0
        self.total_cost = 0.0
        self.total_requests = 0
        
        # Safety monitoring
        self.safety_violations = 0
        self.last_safety_check = datetime.now()
        
        self.logger.info(f"Initialized {self.name} agent with ID {self.agent_id}")
    
    @abstractmethod
    def _initialize_capabilities(self) -> None:
        """Initialize the specific capabilities of this agent."""
        pass
    
    @abstractmethod
    async def _process_message(self, message: AgentMessage) -> AgentResponse:
        """Process a message and return a response. Must be implemented by subclasses."""
        pass
    
    async def process(self, message: Union[str, AgentMessage]) -> AgentResponse:
        """
        Main entry point for processing messages.
        
        Args:
            message: Either a string or an AgentMessage object
            
        Returns:
            AgentResponse with the processed result
        """
        start_time = datetime.now()
        
        # Convert string to AgentMessage if needed
        if isinstance(message, str):
            message = AgentMessage(content=message, sender="user")
        
        # Store message in history
        self.message_history.append(message)
        
        try:
            # Safety pre-check
            if self.config.safety.enable_constitutional_ai:
                safety_result = await self._safety_precheck(message)
                if not safety_result["safe"]:
                    return self._create_safety_refusal_response(safety_result)
            
            # Process the message
            response = await self._process_message(message)
            response.agent_name = self.name
            
            # Safety post-check
            if self.config.safety.enable_constitutional_ai:
                response = await self._safety_postcheck(response)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            response.processing_time = processing_time
            
            # Store response in history
            self.response_history.append(response)
            
            # Update performance metrics
            self._update_metrics(response)
            
            self.logger.info(f"Processed message {message.id} in {processing_time:.2f}s")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing message {message.id}: {str(e)}")
            return self._create_error_response(str(e), message.id)
    
    async def process_stream(self, message: Union[str, AgentMessage]) -> AsyncIterator[str]:
        """
        Process a message and yield response chunks for streaming.
        
        Args:
            message: Either a string or an AgentMessage object
            
        Yields:
            String chunks of the response
        """
        if not self.config.enable_streaming:
            response = await self.process(message)
            yield response.content
            return
        
        # Convert string to AgentMessage if needed
        if isinstance(message, str):
            message = AgentMessage(content=message, sender="user")
        
        # For base implementation, just yield the full response
        # Subclasses can override for true streaming
        response = await self.process(message)
        
        # Yield response in chunks
        content = response.content
        chunk_size = 50  # characters per chunk
        
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i + chunk_size]
            yield chunk
            await asyncio.sleep(0.01)  # Small delay for streaming effect
    
    async def _safety_precheck(self, message: AgentMessage) -> Dict[str, Any]:
        """
        Perform safety checks on incoming messages.
        
        Args:
            message: The message to check
            
        Returns:
            Dictionary with safety assessment
        """
        safety_result = {
            "safe": True,
            "violations": [],
            "risk_score": 0.0,
            "explanation": ""
        }
        
        # Check for harmful content
        if self.config.safety.enable_harm_detection:
            harm_score = await self._detect_harm(message.content)
            safety_result["risk_score"] = harm_score
            
            if harm_score > self.config.safety.toxicity_threshold:
                safety_result["safe"] = False
                safety_result["violations"].append("harmful_content")
                safety_result["explanation"] = "Message contains potentially harmful content"
        
        # Check against constitutional values
        if self.config.safety.enable_constitutional_ai:
            constitutional_check = await self._check_constitutional_compliance(message)
            if not constitutional_check["compliant"]:
                safety_result["safe"] = False
                safety_result["violations"].extend(constitutional_check["violations"])
        
        return safety_result
    
    async def _safety_postcheck(self, response: AgentResponse) -> AgentResponse:
        """
        Perform safety checks on generated responses.
        
        Args:
            response: The response to check
            
        Returns:
            Modified response with safety assessment
        """
        # Check response for harmful content
        if self.config.safety.enable_harm_detection:
            harm_score = await self._detect_harm(response.content)
            response.harm_score = harm_score
            
            if harm_score > self.config.safety.toxicity_threshold:
                response.content = self.config.safety.refusal_message
                response.constitutional_compliance = False
                response.warnings.append("Response flagged for harmful content")
        
        # Populate safety assessment
        response.safety_assessment = {
            "harm_score": response.harm_score,
            "constitutional_compliance": response.constitutional_compliance,
            "safety_level": self.config.safety.level.value,
            "timestamp": datetime.now().isoformat()
        }
        
        return response
    
    async def _detect_harm(self, text: str) -> float:
        """
        Detect harmful content in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Harm score between 0.0 and 1.0
        """
        # Simple implementation - in practice would use specialized models
        harmful_keywords = [
            "violence", "hate", "illegal", "harmful", "dangerous",
            "self-harm", "suicide", "drugs", "weapons"
        ]
        
        text_lower = text.lower()
        harmful_count = sum(1 for keyword in harmful_keywords if keyword in text_lower)
        
        # Simple scoring based on keyword presence
        harm_score = min(harmful_count * 0.2, 1.0)
        
        return harm_score
    
    async def _check_constitutional_compliance(self, message: AgentMessage) -> Dict[str, Any]:
        """
        Check if message complies with constitutional values.
        
        Args:
            message: Message to check
            
        Returns:
            Dictionary with compliance assessment
        """
        # Simplified implementation - would integrate with constitutional AI models
        result = {
            "compliant": True,
            "violations": [],
            "explanation": ""
        }
        
        # Check against core values
        for value in self.config.safety.core_values:
            if value == "human_autonomy" and "force" in message.content.lower():
                result["compliant"] = False
                result["violations"].append("autonomy_violation")
            elif value == "beneficence" and "harm" in message.content.lower():
                result["compliant"] = False
                result["violations"].append("maleficence")
        
        return result
    
    def _create_safety_refusal_response(self, safety_result: Dict[str, Any]) -> AgentResponse:
        """Create a response for safety violations."""
        response = AgentResponse(
            content=self.config.safety.refusal_message,
            agent_name=self.name,
            constitutional_compliance=False,
            harm_score=safety_result["risk_score"],
            safety_assessment=safety_result
        )
        
        if self.config.safety.enable_warning:
            response.warnings.append(f"Safety violation: {safety_result['explanation']}")
        
        self.safety_violations += 1
        return response
    
    def _create_error_response(self, error_message: str, message_id: str) -> AgentResponse:
        """Create a response for errors."""
        return AgentResponse(
            content="I apologize, but I encountered an error while processing your request.",
            agent_name=self.name,
            errors=[error_message],
            confidence=0.0
        )
    
    def _update_metrics(self, response: AgentResponse) -> None:
        """Update performance metrics."""
        self.total_requests += 1
        self.total_tokens_used += response.tokens_used
        self.total_cost += response.cost_estimate
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Get the capabilities of this agent."""
        return self.capabilities.copy()
    
    def has_capability(self, capability: AgentCapability) -> bool:
        """Check if agent has a specific capability."""
        return capability in self.capabilities
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for this agent."""
        return {
            "agent_name": self.name,
            "agent_id": self.agent_id,
            "total_requests": self.total_requests,
            "total_tokens_used": self.total_tokens_used,
            "total_cost": self.total_cost,
            "safety_violations": self.safety_violations,
            "capabilities": [cap.value for cap in self.capabilities],
            "uptime": (datetime.now() - self.last_safety_check).total_seconds()
        }
    
    def reset_metrics(self) -> None:
        """Reset performance metrics."""
        self.total_requests = 0
        self.total_tokens_used = 0
        self.total_cost = 0.0
        self.safety_violations = 0
    
    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"{self.__class__.__name__}(name={self.name}, id={self.agent_id[:8]})"