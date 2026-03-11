"""
Enumeration types for Email Intelligence MCP Server.
"""

from enum import Enum


class EmailPriority(str, Enum):
    """Email priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class EmailCategory(str, Enum):
    """Email classification categories."""
    INVOICE = "invoice"
    RECEIPT = "receipt"
    SPAM = "spam"
    PROMOTIONAL = "promotional"
    PERSONAL = "personal"
    WORK = "work"
    SUPPORT = "support"
    NEWSLETTER = "newsletter"
    OTHER = "other"


class ExtractedDataType(str, Enum):
    """Types of data that can be extracted."""
    TEXT = "text"
    TABLE = "table"
    IMAGE = "image"
    LINK = "link"
    ATTACHMENT = "attachment"
