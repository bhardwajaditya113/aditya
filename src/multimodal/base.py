"""
Base classes and data structures for multi-modal processing.

This module defines the core interfaces and data structures used across
all modalities in the Superintelligence AI Framework.
"""

import base64
import io
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, BinaryIO
import torch
import numpy as np
from PIL import Image


class ModalityType(Enum):
    """Types of modalities supported by the framework."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    CODE = "code"
    EMBEDDING = "embedding"
    KNOWLEDGE_GRAPH = "knowledge_graph"


class ProcessingStatus(Enum):
    """Status of processing operations."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CACHED = "cached"


@dataclass
class ModalityMetadata:
    """Metadata for modality content."""
    
    modality_type: ModalityType
    format: str  # e.g., "jpeg", "wav", "mp4", "pdf"
    size: Optional[int] = None  # file size in bytes
    dimensions: Optional[tuple] = None  # (width, height) for images/videos
    duration: Optional[float] = None  # duration in seconds for audio/video
    encoding: str = "utf-8"
    language: Optional[str] = None
    quality: Optional[str] = None  # "high", "medium", "low"
    source: Optional[str] = None  # URL or file path
    created_at: Optional[str] = None
    processed_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            "modality_type": self.modality_type.value,
            "format": self.format,
            "size": self.size,
            "dimensions": self.dimensions,
            "duration": self.duration,
            "encoding": self.encoding,
            "language": self.language,
            "quality": self.quality,
            "source": self.source,
            "created_at": self.created_at,
            "processed_at": self.processed_at
        }


@dataclass
class MultiModalInput:
    """Container for multi-modal input data."""
    
    # Text content
    text: Optional[str] = None
    
    # Visual content
    images: List[Union[str, Image.Image, np.ndarray]] = field(default_factory=list)
    videos: List[Union[str, np.ndarray]] = field(default_factory=list)
    
    # Audio content
    audio: List[Union[str, np.ndarray]] = field(default_factory=list)
    
    # Document content
    documents: List[Union[str, Dict[str, Any]]] = field(default_factory=list)
    
    # Code content
    code: List[Dict[str, str]] = field(default_factory=list)  # {"language": "python", "content": "..."}
    
    # Metadata for each modality
    metadata: Dict[str, List[ModalityMetadata]] = field(default_factory=dict)
    
    # Processing instructions
    processing_options: Dict[str, Any] = field(default_factory=dict)
    
    def add_text(self, text: str, metadata: Optional[ModalityMetadata] = None) -> None:
        """Add text content."""
        self.text = text
        if metadata:
            self.metadata.setdefault("text", []).append(metadata)
    
    def add_image(self, image: Union[str, Image.Image, np.ndarray], 
                  metadata: Optional[ModalityMetadata] = None) -> None:
        """Add image content."""
        self.images.append(image)
        if metadata:
            self.metadata.setdefault("images", []).append(metadata)
    
    def add_audio(self, audio: Union[str, np.ndarray], 
                  metadata: Optional[ModalityMetadata] = None) -> None:
        """Add audio content."""
        self.audio.append(audio)
        if metadata:
            self.metadata.setdefault("audio", []).append(metadata)
    
    def add_video(self, video: Union[str, np.ndarray], 
                  metadata: Optional[ModalityMetadata] = None) -> None:
        """Add video content."""
        self.videos.append(video)
        if metadata:
            self.metadata.setdefault("videos", []).append(metadata)
    
    def add_document(self, document: Union[str, Dict[str, Any]], 
                     metadata: Optional[ModalityMetadata] = None) -> None:
        """Add document content."""
        self.documents.append(document)
        if metadata:
            self.metadata.setdefault("documents", []).append(metadata)
    
    def add_code(self, code: str, language: str = "python", 
                 metadata: Optional[ModalityMetadata] = None) -> None:
        """Add code content."""
        self.code.append({"language": language, "content": code})
        if metadata:
            self.metadata.setdefault("code", []).append(metadata)
    
    def get_modalities(self) -> List[ModalityType]:
        """Get list of modalities present in the input."""
        modalities = []
        if self.text:
            modalities.append(ModalityType.TEXT)
        if self.images:
            modalities.append(ModalityType.IMAGE)
        if self.audio:
            modalities.append(ModalityType.AUDIO)
        if self.videos:
            modalities.append(ModalityType.VIDEO)
        if self.documents:
            modalities.append(ModalityType.DOCUMENT)
        if self.code:
            modalities.append(ModalityType.CODE)
        return modalities
    
    def is_multimodal(self) -> bool:
        """Check if input contains multiple modalities."""
        return len(self.get_modalities()) > 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "text": self.text,
            "images": [self._serialize_image(img) for img in self.images],
            "audio": [self._serialize_audio(aud) for aud in self.audio],
            "videos": [self._serialize_video(vid) for vid in self.videos],
            "documents": self.documents,
            "code": self.code,
            "metadata": {k: [m.to_dict() for m in v] for k, v in self.metadata.items()},
            "processing_options": self.processing_options
        }
    
    def _serialize_image(self, image: Union[str, Image.Image, np.ndarray]) -> str:
        """Serialize image to base64 string."""
        if isinstance(image, str):
            return image
        elif isinstance(image, Image.Image):
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode()
        elif isinstance(image, np.ndarray):
            image_pil = Image.fromarray(image.astype(np.uint8))
            buffer = io.BytesIO()
            image_pil.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode()
        return str(image)
    
    def _serialize_audio(self, audio: Union[str, np.ndarray]) -> str:
        """Serialize audio to base64 string."""
        if isinstance(audio, str):
            return audio
        # For numpy arrays, would need proper audio encoding
        return str(audio)
    
    def _serialize_video(self, video: Union[str, np.ndarray]) -> str:
        """Serialize video to string representation."""
        if isinstance(video, str):
            return video
        return str(video)


@dataclass
class MultiModalOutput:
    """Container for multi-modal output data."""
    
    # Generated content
    text: Optional[str] = None
    images: List[Union[str, Image.Image, np.ndarray]] = field(default_factory=list)
    audio: List[Union[str, np.ndarray]] = field(default_factory=list)
    videos: List[Union[str, np.ndarray]] = field(default_factory=list)
    
    # Embeddings and features
    embeddings: Dict[str, torch.Tensor] = field(default_factory=dict)
    features: Dict[str, Any] = field(default_factory=dict)
    
    # Analysis results
    classifications: Dict[str, Any] = field(default_factory=dict)
    detections: List[Dict[str, Any]] = field(default_factory=list)
    annotations: List[Dict[str, Any]] = field(default_factory=list)
    
    # Processing metadata
    processing_status: ProcessingStatus = ProcessingStatus.PENDING
    processing_time: float = 0.0
    model_info: Dict[str, str] = field(default_factory=dict)
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    
    # Error handling
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def add_text(self, text: str, confidence: float = 1.0) -> None:
        """Add generated text."""
        self.text = text
        self.confidence_scores["text"] = confidence
    
    def add_image(self, image: Union[str, Image.Image, np.ndarray], 
                  confidence: float = 1.0) -> None:
        """Add generated image."""
        self.images.append(image)
        self.confidence_scores[f"image_{len(self.images)}"] = confidence
    
    def add_embedding(self, modality: str, embedding: torch.Tensor) -> None:
        """Add embedding for a modality."""
        self.embeddings[modality] = embedding
    
    def add_classification(self, category: str, result: Any, 
                          confidence: float = 1.0) -> None:
        """Add classification result."""
        self.classifications[category] = result
        self.confidence_scores[f"classification_{category}"] = confidence
    
    def add_detection(self, detection: Dict[str, Any]) -> None:
        """Add object detection result."""
        self.detections.append(detection)
    
    def add_annotation(self, annotation: Dict[str, Any]) -> None:
        """Add annotation result."""
        self.annotations.append(annotation)
    
    def add_error(self, error: str) -> None:
        """Add error message."""
        self.errors.append(error)
        self.processing_status = ProcessingStatus.FAILED
    
    def add_warning(self, warning: str) -> None:
        """Add warning message."""
        self.warnings.append(warning)
    
    def get_overall_confidence(self) -> float:
        """Get overall confidence score."""
        if not self.confidence_scores:
            return 0.0
        return sum(self.confidence_scores.values()) / len(self.confidence_scores)
    
    def is_successful(self) -> bool:
        """Check if processing was successful."""
        return self.processing_status == ProcessingStatus.COMPLETED and not self.errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "text": self.text,
            "images": [self._serialize_image(img) for img in self.images],
            "audio": [str(aud) for aud in self.audio],
            "videos": [str(vid) for vid in self.videos],
            "embeddings": {k: v.tolist() if isinstance(v, torch.Tensor) else v 
                          for k, v in self.embeddings.items()},
            "features": self.features,
            "classifications": self.classifications,
            "detections": self.detections,
            "annotations": self.annotations,
            "processing_status": self.processing_status.value,
            "processing_time": self.processing_time,
            "model_info": self.model_info,
            "confidence_scores": self.confidence_scores,
            "errors": self.errors,
            "warnings": self.warnings
        }
    
    def _serialize_image(self, image: Union[str, Image.Image, np.ndarray]) -> str:
        """Serialize image to base64 string."""
        if isinstance(image, str):
            return image
        elif isinstance(image, Image.Image):
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode()
        elif isinstance(image, np.ndarray):
            image_pil = Image.fromarray(image.astype(np.uint8))
            buffer = io.BytesIO()
            image_pil.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode()
        return str(image)


class BaseModalityProcessor(ABC):
    """Abstract base class for modality processors."""
    
    def __init__(self, model_config: Dict[str, Any]):
        """Initialize the processor with model configuration."""
        self.model_config = model_config
        self.model = None
        self.is_loaded = False
        self._load_model()
    
    @abstractmethod
    def _load_model(self) -> None:
        """Load the model for this processor."""
        pass
    
    @abstractmethod
    async def process(self, input_data: MultiModalInput) -> MultiModalOutput:
        """Process input data and return output."""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Get list of supported input formats."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Get list of processor capabilities."""
        pass
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.is_loaded
    
    def unload_model(self) -> None:
        """Unload model to free memory."""
        self.model = None
        self.is_loaded = False
    
    def get_model_info(self) -> Dict[str, str]:
        """Get information about the loaded model."""
        return {
            "model_name": self.model_config.get("name", "unknown"),
            "model_type": self.model_config.get("type", "unknown"),
            "version": self.model_config.get("version", "unknown"),
            "provider": self.model_config.get("provider", "unknown")
        }