"""
Multi-modal processing module for the Superintelligence AI Framework.

This module provides comprehensive multi-modal input/output processing including
vision, language, audio, and cross-modal fusion capabilities.
"""

from .base import MultiModalInput, MultiModalOutput, ModalityType
from .vision import VisionProcessor
from .language import LanguageProcessor
from .audio import AudioProcessor
from .fusion import MultiModalFusion

__all__ = [
    "MultiModalInput",
    "MultiModalOutput", 
    "ModalityType",
    "VisionProcessor",
    "LanguageProcessor",
    "AudioProcessor", 
    "MultiModalFusion"
]