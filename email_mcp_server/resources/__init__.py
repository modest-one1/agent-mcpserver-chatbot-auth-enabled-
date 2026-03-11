"""
Resources module for Email Intelligence MCP Server.
Contains all MCP resource providers.
"""

from .templates_resource import get_professional_email_templates
from .patterns_resource import get_email_extraction_patterns

__all__ = [
    "get_professional_email_templates",
    "get_email_extraction_patterns",
]
