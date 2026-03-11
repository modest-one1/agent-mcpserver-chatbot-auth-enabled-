"""
Data models for Email Intelligence MCP Server.
Contains all Pydantic models for inputs, outputs, and enums.
"""

from .enums import EmailPriority, EmailCategory, ExtractedDataType
from .ocr_models import OcrInput, OcrOutput, OcrRegion
from .table_models import TableExtractorInput, TableData, TableExtractorOutput
from .tagger_models import EmailTaggerInput, TagSuggestion, EmailTaggerOutput
from .classifier_models import (
    EmailClassifierInput, 
    ClassificationResult, 
    EmailClassifierOutput
)
from .parser_models import EmailParserInput, AttachmentInfo, EmailParserOutput
from .entity_models import EntityExtractorInput, ExtractedEntity, EntityExtractorOutput

__all__ = [
    # Enums
    "EmailPriority",
    "EmailCategory", 
    "ExtractedDataType",
    # OCR
    "OcrInput",
    "OcrOutput",
    "OcrRegion",
    # Tables
    "TableExtractorInput",
    "TableData",
    "TableExtractorOutput",
    # Tagger
    "EmailTaggerInput",
    "TagSuggestion",
    "EmailTaggerOutput",
    # Classifier
    "EmailClassifierInput",
    "ClassificationResult",
    "EmailClassifierOutput",
    # Parser
    "EmailParserInput",
    "AttachmentInfo",
    "EmailParserOutput",
    # Entities
    "EntityExtractorInput",
    "ExtractedEntity",
    "EntityExtractorOutput",
]
