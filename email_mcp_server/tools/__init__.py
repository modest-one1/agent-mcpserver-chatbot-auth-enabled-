"""
Tools module for Email Intelligence MCP Server.
Contains all MCP tool implementations.
"""

from .ocr_tool import ocr_extract
from .table_tool import extract_tables
from .tagger_tool import tag_email
from .classifier_tool import classify_email
from .parser_tool import parse_email
from .entity_tool import extract_entities

__all__ = [
    "ocr_extract",
    "extract_tables",
    "tag_email",
    "classify_email",
    "parse_email",
    "extract_entities",
]
