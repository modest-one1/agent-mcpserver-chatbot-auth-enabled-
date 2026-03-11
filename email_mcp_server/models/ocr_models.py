"""
OCR (Optical Character Recognition) models.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class OcrRegion(BaseModel):
    """A region extracted by OCR with coordinates."""
    x: int = Field(..., description="X coordinate")
    y: int = Field(..., description="Y coordinate")
    width: int = Field(..., description="Region width")
    height: int = Field(..., description="Region height")
    text: str = Field(..., description="Extracted text from this region")


class OcrInput(BaseModel):
    """Input parameters for OCR text extraction."""
    image_data: str = Field(
        ..., 
        description="Base64 encoded image data or image URL"
    )
    image_format: str = Field(
        default="auto", 
        description="Image format: png, jpg, pdf, auto"
    )
    language: str = Field(
        default="eng", 
        description="OCR language code (e.g., eng, fra, deu)"
    )
    enhance_image: bool = Field(
        default=True, 
        description="Apply image enhancement before OCR"
    )
    extract_regions: Optional[List[Dict[str, int]]] = Field(
        default=None, 
        description="Specific regions to extract [x, y, width, height]"
    )


class OcrOutput(BaseModel):
    """Output from OCR text extraction."""
    success: bool = Field(
        ..., 
        description="Whether OCR extraction was successful"
    )
    text: str = Field(
        ..., 
        description="Extracted text content"
    )
    confidence: float = Field(
        ..., 
        ge=0, 
        le=100,
        description="OCR confidence score (0-100)"
    )
    language_detected: str = Field(
        ..., 
        description="Detected language"
    )
    processing_time_ms: int = Field(
        ..., 
        description="Processing time in milliseconds"
    )
    regions: List[OcrRegion] = Field(
        default=[], 
        description="Extracted regions with coordinates"
    )
    errors: List[str] = Field(
        default=[], 
        description="Any errors encountered"
    )
