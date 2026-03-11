"""
Email parsing models.
"""

from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class AttachmentInfo(BaseModel):
    """Information about an email attachment."""
    filename: str = Field(
        ..., 
        description="Attachment filename"
    )
    content_type: str = Field(
        ..., 
        description="MIME content type"
    )
    size: int = Field(
        ..., 
        description="Attachment size in bytes"
    )
    content_id: Optional[str] = Field(
        default=None, 
        description="Content-ID if available"
    )


class EmailParserInput(BaseModel):
    """Input parameters for email parsing."""
    raw_email: str = Field(
        ..., 
        description="Raw email content (RFC 2822 format)"
    )
    extract_attachments: bool = Field(
        default=True, 
        description="Extract attachment metadata"
    )
    parse_headers: bool = Field(
        default=True, 
        description="Parse all email headers"
    )
    extract_links: bool = Field(
        default=True, 
        description="Extract all URLs from email"
    )


class EmailParserOutput(BaseModel):
    """Output from email parsing."""
    success: bool = Field(
        ..., 
        description="Whether parsing was successful"
    )
    headers: Dict[str, str] = Field(
        ..., 
        description="Email headers"
    )
    subject: str = Field(
        ..., 
        description="Email subject"
    )
    from_address: str = Field(
        ..., 
        description="From address"
    )
    to_addresses: List[str] = Field(
        ..., 
        description="To addresses"
    )
    cc_addresses: List[str] = Field(
        default=[], 
        description="CC addresses"
    )
    bcc_addresses: List[str] = Field(
        default=[], 
        description="BCC addresses"
    )
    date: Optional[str] = Field(
        default=None, 
        description="Email date"
    )
    body_text: str = Field(
        ..., 
        description="Plain text body"
    )
    body_html: Optional[str] = Field(
        default=None, 
        description="HTML body if available"
    )
    attachments: List[AttachmentInfo] = Field(
        ..., 
        description="Attachment information"
    )
    links: List[str] = Field(
        ..., 
        description="Extracted URLs"
    )
    reply_to: Optional[str] = Field(
        default=None, 
        description="Reply-To address"
    )
