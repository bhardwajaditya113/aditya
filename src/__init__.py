"""
Superintelligence Multi-Modal Agentic AI Framework

A comprehensive framework for developing superintelligent AI systems through 
multi-modal agentic architectures with constitutional alignment and safety mechanisms.
"""

from .agents import (
    BaseAgent,
    MindMapAgent, 
    WebSearchAgent,
    CodingAgent,
    ConstitutionalAgent,
    SupervisorAgent,
    SuperintelligenteAgent
)

from .multimodal import (
    VisionProcessor,
    LanguageProcessor,
    AudioProcessor,
    MultiModalFusion
)

from .reasoning import (
    AgenticReasoning,
    ChainOfThought,
    ConstitutionalAI,
    TestTimeScaling
)

from .config import AgentConfig, ModelConfig, SafetyConfig

__version__ = "0.1.0"
__author__ = "Superintelligence AI Research Team"

__all__ = [
    # Core agents
    "BaseAgent",
    "MindMapAgent", 
    "WebSearchAgent",
    "CodingAgent",
    "ConstitutionalAgent",
    "SupervisorAgent",
    "SuperintelligenteAgent",
    
    # Multi-modal processors
    "VisionProcessor",
    "LanguageProcessor", 
    "AudioProcessor",
    "MultiModalFusion",
    
    # Reasoning systems
    "AgenticReasoning",
    "ChainOfThought",
    "ConstitutionalAI",
    "TestTimeScaling",
    
    # Configuration
    "AgentConfig",
    "ModelConfig", 
    "SafetyConfig",
]