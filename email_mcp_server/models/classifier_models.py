"""
Email classification models.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from .enums import EmailPriority, EmailCategory


class ClassificationResult(BaseModel):
    """Detailed classification result."""
    category: EmailCategory = Field(
        ..., 
        description="Primary category"
    )
    confidence: float = Field(
        ..., 
        ge=0, 
        le=1,
        description="Classification confidence (0-1)"
    )
    alternative_categories: List[Dict[str, float]] = Field(
        ..., 
        description="Alternative categories with scores"
    )
    priority: EmailPriority = Field(
        ..., 
        description="Priority level"
    )
    priority_confidence: float = Field(
        ..., 
        description="Priority classification confidence"
    )
    key_indicators: List[str] = Field(
        ..., 
        description="Key indicators used for classification"
    )


class EmailClassifierInput(BaseModel):
    """Input parameters for email classification."""
    email_subject: str = Field(
        ..., 
        description="Email subject line"
    )
    email_body: str = Field(
        ..., 
        description="Email body content"
    )
    email_from: Optional[str] = Field(
        default=None, 
        description="Sender email address"
    )
    attachments: Optional[List[str]] = Field(
        default=None, 
        description="List of attachment filenames"
    )
    custom_categories: Optional[List[str]] = Field(
        default=None, 
        description="Custom classification categories"
    )
    classify_priority: bool = Field(
        default=True, 
        description="Also classify priority level"
    )


class EmailClassifierOutput(BaseModel):
    """Output from email classification."""
    success: bool = Field(
        ..., 
        description="Whether classification was successful"
    )
    classification: ClassificationResult = Field(
        ..., 
        description="Classification results"
    )
    entities: Dict[str, List[str]] = Field(
        ..., 
        description="Extracted entities (dates, amounts, names)"
    )
    processing_time_ms: int = Field(
        ..., 
        description="Processing time in milliseconds"
    )
