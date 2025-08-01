"""
Configuration system for the Superintelligence Multi-Modal Agentic AI Framework.

This module provides comprehensive configuration classes for agents, models,
and safety systems with validation and type checking.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Any
from enum import Enum
import yaml
from pathlib import Path


class ModelType(Enum):
    """Supported model types for different components."""
    LANGUAGE = "language"
    VISION = "vision"
    AUDIO = "audio"
    MULTIMODAL = "multimodal"
    EMBEDDING = "embedding"


class SafetyLevel(Enum):
    """Safety enforcement levels."""
    MINIMAL = "minimal"
    STANDARD = "standard"
    HIGH = "high"
    MAXIMUM = "maximum"


class ReasoningMode(Enum):
    """Reasoning modes for different task types."""
    FAST = "fast"
    BALANCED = "balanced"
    DEEP = "deep"
    RESEARCH = "research"


@dataclass
class ModelConfig:
    """Configuration for individual models."""
    
    name: str
    model_type: ModelType
    provider: str = "openai"  # openai, anthropic, huggingface, local
    api_key: Optional[str] = None
    model_path: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 0.7
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    timeout: int = 60
    retry_attempts: int = 3
    
    # Model-specific parameters
    vision_detail: str = "high"  # for vision models
    audio_format: str = "wav"   # for audio models
    embedding_dimensions: int = 1536  # for embedding models
    
    # Performance settings
    batch_size: int = 1
    use_cache: bool = True
    quantization: Optional[str] = None  # 4bit, 8bit, fp16
    device: str = "auto"  # auto, cpu, cuda, mps


@dataclass
class SafetyConfig:
    """Configuration for safety and alignment systems."""
    
    level: SafetyLevel = SafetyLevel.HIGH
    enable_constitutional_ai: bool = True
    enable_harm_detection: bool = True
    enable_bias_monitoring: bool = True
    enable_privacy_protection: bool = True
    
    # Constitutional framework
    core_values: List[str] = field(default_factory=lambda: [
        "human_autonomy", "beneficence", "non_maleficence", "justice"
    ])
    harm_categories: List[str] = field(default_factory=lambda: [
        "violence", "hate_speech", "misinformation", "privacy_violation",
        "illegal_activity", "self_harm", "child_safety"
    ])
    
    # Monitoring thresholds
    toxicity_threshold: float = 0.1
    bias_threshold: float = 0.2
    privacy_score_threshold: float = 0.8
    
    # Response settings
    enable_refusal: bool = True
    refusal_message: str = "I cannot provide assistance with that request due to safety concerns."
    enable_warning: bool = True
    log_violations: bool = True
    
    # Custom constitution file
    constitution_path: Optional[str] = None


@dataclass  
class AgentConfig:
    """Main configuration for the Superintelligence Agent."""
    
    # Core model settings
    language_model: ModelConfig = field(default_factory=lambda: ModelConfig(
        name="gpt-4-turbo-preview",
        model_type=ModelType.LANGUAGE,
        provider="openai"
    ))
    
    vision_model: ModelConfig = field(default_factory=lambda: ModelConfig(
        name="gpt-4-vision-preview", 
        model_type=ModelType.VISION,
        provider="openai"
    ))
    
    audio_model: ModelConfig = field(default_factory=lambda: ModelConfig(
        name="whisper-1",
        model_type=ModelType.AUDIO,
        provider="openai"
    ))
    
    embedding_model: ModelConfig = field(default_factory=lambda: ModelConfig(
        name="text-embedding-ada-002",
        model_type=ModelType.EMBEDDING,
        provider="openai"
    ))
    
    # Agent capabilities
    enable_web_search: bool = True
    enable_code_execution: bool = True
    enable_mind_map: bool = True
    enable_multimodal: bool = True
    enable_tool_calling: bool = True
    
    # Reasoning settings
    reasoning_mode: ReasoningMode = ReasoningMode.BALANCED
    max_reasoning_steps: int = 50
    enable_chain_of_thought: bool = True
    enable_test_time_scaling: bool = True
    
    # Tool configurations
    web_search_engines: List[str] = field(default_factory=lambda: [
        "duckduckgo", "wikipedia", "arxiv"
    ])
    code_execution_timeout: int = 30
    code_execution_memory_limit: str = "1GB"
    
    # Memory and context
    max_context_length: int = 32000
    enable_long_term_memory: bool = True
    memory_persistence: bool = True
    conversation_history_limit: int = 100
    
    # Safety configuration
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    
    # Performance settings
    max_parallel_agents: int = 5
    agent_timeout: int = 300
    enable_streaming: bool = True
    
    # Monitoring and logging
    enable_logging: bool = True
    log_level: str = "INFO"
    enable_metrics: bool = True
    metrics_endpoint: Optional[str] = None
    
    # Custom configurations
    custom_prompts: Dict[str, str] = field(default_factory=dict)
    custom_tools: List[str] = field(default_factory=list)
    
    def save(self, path: Union[str, Path]) -> None:
        """Save configuration to YAML file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to dict for serialization
        config_dict = self._to_dict()
        
        with open(path, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False, indent=2)
    
    @classmethod
    def load(cls, path: Union[str, Path]) -> 'AgentConfig':
        """Load configuration from YAML file."""
        path = Path(path)
        
        with open(path, 'r') as f:
            config_dict = yaml.safe_load(f)
        
        return cls._from_dict(config_dict)
    
    def _to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        # This is a simplified version - in practice you'd want proper serialization
        return {
            "language_model": {
                "name": self.language_model.name,
                "model_type": self.language_model.model_type.value,
                "provider": self.language_model.provider,
                "max_tokens": self.language_model.max_tokens,
                "temperature": self.language_model.temperature,
            },
            "enable_web_search": self.enable_web_search,
            "enable_code_execution": self.enable_code_execution,
            "reasoning_mode": self.reasoning_mode.value,
            "safety": {
                "level": self.safety.level.value,
                "enable_constitutional_ai": self.safety.enable_constitutional_ai,
                "core_values": self.safety.core_values,
                "harm_categories": self.safety.harm_categories,
            }
        }
    
    @classmethod
    def _from_dict(cls, config_dict: Dict[str, Any]) -> 'AgentConfig':
        """Create configuration from dictionary."""
        # Simplified implementation - would need full deserialization
        config = cls()
        
        if "language_model" in config_dict:
            lm_config = config_dict["language_model"]
            config.language_model.name = lm_config.get("name", config.language_model.name)
            config.language_model.temperature = lm_config.get("temperature", config.language_model.temperature)
        
        config.enable_web_search = config_dict.get("enable_web_search", config.enable_web_search)
        config.enable_code_execution = config_dict.get("enable_code_execution", config.enable_code_execution)
        
        if "reasoning_mode" in config_dict:
            config.reasoning_mode = ReasoningMode(config_dict["reasoning_mode"])
        
        return config


def create_research_config() -> AgentConfig:
    """Create configuration optimized for deep research tasks."""
    config = AgentConfig()
    config.reasoning_mode = ReasoningMode.RESEARCH
    config.max_reasoning_steps = 100
    config.language_model.max_tokens = 8192
    config.enable_test_time_scaling = True
    config.safety.level = SafetyLevel.HIGH
    return config


def create_fast_config() -> AgentConfig:
    """Create configuration optimized for fast responses."""
    config = AgentConfig()
    config.reasoning_mode = ReasoningMode.FAST
    config.max_reasoning_steps = 10
    config.language_model.temperature = 0.1
    config.enable_test_time_scaling = False
    config.safety.level = SafetyLevel.STANDARD
    return config


def create_maximum_safety_config() -> AgentConfig:
    """Create configuration with maximum safety settings."""
    config = AgentConfig()
    config.safety.level = SafetyLevel.MAXIMUM
    config.safety.enable_constitutional_ai = True
    config.safety.enable_harm_detection = True
    config.safety.enable_bias_monitoring = True
    config.safety.enable_privacy_protection = True
    config.safety.toxicity_threshold = 0.05
    config.safety.bias_threshold = 0.1
    return config