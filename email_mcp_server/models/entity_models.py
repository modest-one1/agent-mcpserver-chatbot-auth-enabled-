"""
Entity extraction models.
"""

from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class ExtractedEntity(BaseModel):
    """A single extracted entity."""
    entity: str = Field(
        ..., 
        description="Extracted entity text"
    )
    type: str = Field(
        ..., 
        description="Entity type"
    )
    confidence: float = Field(
        ..., 
        ge=0, 
        le=1,
        description="Extraction confidence (0-1)"
    )
    position: Dict[str, int] = Field(
        ..., 
        description="Start and end position in text"
    )
    normalized_value: Optional[str] = Field(
        default=None, 
        description="Normalized value"
    )


class EntityExtractorInput(BaseModel):
    """Input parameters for entity extraction."""
    text: str = Field(
        ..., 
        description="Text to extract entities from"
    )
    entity_types: List[str] = Field(
        default=["all"], 
        description="Types to extract: person, organization, date, email, phone, amount, address, url, all"
    )
    context: Optional[str] = Field(
        default=None, 
        description="Additional context for better extraction"
    )


class EntityExtractorOutput(BaseModel):
    """Output from entity extraction."""
    success: bool = Field(
        ..., 
        description="Whether extraction was successful"
    )
    entities: List[ExtractedEntity] = Field(
        ..., 
        description="Extracted entities"
    )
    entity_counts: Dict[str, int] = Field(
        ..., 
        description="Count by entity type"
    )
    processing_time_ms: int = Field(
        ..., 
        description="Processing time in milliseconds"
    )
