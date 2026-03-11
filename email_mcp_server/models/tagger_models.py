"""
Email tagging models.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from .enums import EmailPriority


class TagSuggestion(BaseModel):
    """A suggested tag with metadata."""
    tag: str = Field(
        ..., 
        description="Suggested tag name"
    )
    confidence: float = Field(
        ..., 
        ge=0, 
        le=1,
        description="Confidence score (0-1)"
    )
    category: str = Field(
        ..., 
        description="Tag category"
    )
    reason: str = Field(
        ..., 
        description="Reason for suggestion"
    )


class EmailTaggerInput(BaseModel):
    """Input parameters for email tagging."""
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
    existing_tags: Optional[List[str]] = Field(
        default=None, 
        description="Existing tags to consider"
    )
    max_tags: int = Field(
        default=5, 
        description="Maximum number of tags to generate"
    )
    use_ai_suggestions: bool = Field(
        default=True, 
        description="Use AI for intelligent tagging"
    )


class EmailTaggerOutput(BaseModel):
    """Output from email tagging."""
    success: bool = Field(
        ..., 
        description="Whether tagging was successful"
    )
    tags: List[TagSuggestion] = Field(
        ..., 
        description="Suggested tags"
    )
    categories: List[str] = Field(
        ..., 
        description="Detected categories"
    )
    priority: EmailPriority = Field(
        ..., 
        description="Suggested priority"
    )
    sentiment: str = Field(
        ..., 
        description="Detected sentiment"
    )
    processing_time_ms: int = Field(
        ..., 
        description="Processing time in milliseconds"
    )
