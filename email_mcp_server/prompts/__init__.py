"""
Prompts module for Email Intelligence MCP Server.
Contains all MCP prompt templates.
"""

from .analysis_prompt import email_analysis_prompt
from .reply_prompt import email_reply_generator

__all__ = [
    "email_analysis_prompt",
    "email_reply_generator",
]
