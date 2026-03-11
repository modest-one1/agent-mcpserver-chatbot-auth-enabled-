"""
Helper utilities for the Email Intelligence MCP Server.
"""

import re


def format_processing_time(milliseconds: int) -> str:
    """
    Format processing time in a human-readable format.
    
    Args:
        milliseconds: Processing time in milliseconds
    
    Returns:
        Formatted string (e.g., "1.25s" or "150ms")
    """
    if milliseconds >= 1000:
        return f"{milliseconds / 1000:.2f}s"
    return f"{milliseconds}ms"


def sanitize_email_content(content: str) -> str:
    """
    Sanitize email content by removing potentially harmful content.
    
    Args:
        content: Raw email content
    
    Returns:
        Sanitized content
    """
    # Remove null bytes
    content = content.replace('\x00', '')
    
    # Normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Limit length to prevent memory issues
    max_length = 10 * 1024 * 1024  # 10MB
    if len(content) > max_length:
        content = content[:max_length]
    
    return content


def truncate_text(text: str, max_length: int = 1000, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_domain_from_email(email: str) -> str:
    """
    Extract domain from email address.
    
    Args:
        email: Email address
    
    Returns:
        Domain part of email
    """
    if "@" in email:
        return email.split("@")[1]
    return ""


def is_valid_email_format(email: str) -> bool:
    """
    Check if string is a valid email format.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid format
    """
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    return bool(re.match(pattern, email))
