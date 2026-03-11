#!/usr/bin/env python3
"""
Email Intelligence MCP Server
=============================

A comprehensive MCP server for email extraction, analysis, and processing.
Supports OCR, table extraction, email tagging, classification, and more.

This is the main entry point that registers all tools, prompts, and resources.

Modules:
    - models: Pydantic data models for inputs/outputs
    - tools: MCP tool implementations
    - prompts: MCP prompt templates
    - resources: MCP resource providers
    - utils: Helper utilities

Usage:
    python server.py

Configuration:
    See mcp_config.json for complete server configuration and schemas.
"""

from fastmcp import FastMCP, Context
import asyncio
from fastmcp.server.auth import JWTVerifier

# Import all tools
from tools import (
    ocr_extract,
    extract_tables,
    tag_email,
    classify_email,
    parse_email,
    extract_entities,
)

# Import all prompts
from prompts import (
    email_analysis_prompt,
    email_reply_generator,
)


# Import all resources
from resources import (
    get_professional_email_templates,
    get_email_extraction_patterns,
)

import os
from dotenv import load_dotenv
load_dotenv()


TENANT_ID = os.getenv("TENANT_ID", "your-tenant-id")
CLIENT_ID = os.getenv("CLIENT_ID", "your-client-id")
# API audience can be in multiple formats, so we'll define both common ones
API_AUDIENCE = os.getenv("API_AUDIENCE", f"api://{CLIENT_ID}")

# Azure Entra ID JWKS endpoint
JWKS_URI = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"

# Configure Bearer Token authentication for Azure Entra ID

auth = JWTVerifier(
    jwks_uri=JWKS_URI,
    issuer=f"https://sts.windows.net/{TENANT_ID}/",  # Match the token's issuer format in the API
    algorithm="RS256",  # Azure Entra ID uses RS256
    audience=API_AUDIENCE,  # required audience
   # required_scopes=["execute"]  # Optional: add required scopes if needed
)
# Initialize FastMCP server
mcp = FastMCP("email-intelligence-server", auth=auth)


# ============================================================================
# TOOL REGISTRATION
# ============================================================================

@mcp.tool()
async def ocr_extract_tool(input_data, ctx):
    """
    Extract text from images using OCR (Optical Character Recognition).
    Supports various image formats and languages with confidence scoring.
    """
    return await ocr_extract(input_data, ctx)


@mcp.tool()
async def extract_tables_tool(input_data, ctx):
    """
    Extract tables from emails, HTML, PDFs, or images.
    Supports multiple output formats and handles complex table structures.
    """
    return await extract_tables(input_data, ctx)


@mcp.tool()
async def tag_email_tool(input_data, ctx):
    """
    Intelligently tag emails based on content analysis.
    Suggests relevant tags, categories, priority, and sentiment.
    """
    return await tag_email(input_data, ctx)


@mcp.tool()
async def classify_email_tool(input_data, ctx):
    """
    Classify emails into categories with confidence scores.
    Extracts entities and determines priority level.
    """
    return await classify_email(input_data, ctx)


@mcp.tool()
async def parse_email_tool(input_data, ctx):
    """
    Parse raw email content (RFC 2822 format) into structured components.
    Extracts headers, body, attachments, and links.
    """
    return await parse_email(input_data, ctx)


@mcp.tool()
async def extract_entities_tool(input_data, ctx):
    """
    Extract named entities from email text.
    Identifies persons, organizations, dates, amounts, emails, phones, and addresses.
    """
    return await extract_entities(input_data, ctx)


# ============================================================================
# PROMPT REGISTRATION
# ============================================================================

@mcp.prompt()
def email_analysis_prompt_tool(email_subject: str, email_body: str, email_from: str = "") -> str:
    """
    Comprehensive email analysis prompt for extracting insights and action items.
    Use this prompt to analyze email content thoroughly.
    
    Args:
        email_subject: Email subject line
        email_body: Email body content
        email_from: Sender email address (optional)
    """
    return email_analysis_prompt(email_subject, email_body, email_from)


@mcp.prompt()
def email_reply_generator_tool(
    email_subject: str, 
    email_body: str, 
    email_from: str, 
    tone: str = "professional", 
    key_points: str = ""
) -> str:
    """
    Generate professional email replies based on received emails.
    Supports different tones and customizable key points.
    
    Args:
        email_subject: Email subject line
        email_body: Email body content
        email_from: Sender email address
        tone: Tone of the reply (professional, friendly, formal)
        key_points: Key points to address in the reply
    """
    return email_reply_generator(email_subject, email_body, email_from, tone, key_points)


# ============================================================================
# RESOURCE REGISTRATION
# ============================================================================

@mcp.resource("email-templates://professional")
def professional_templates_resource() -> str:
    """
    Professional email templates for common business scenarios.
    Includes meeting requests, follow-ups, introductions, and more.
    """
    return get_professional_email_templates()


@mcp.resource("email-patterns://extraction")
def extraction_patterns_resource() -> str:
    """
    Common regex patterns for email content extraction.
    Useful for parsing dates, amounts, phone numbers, and more.
    """
    return get_email_extraction_patterns()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    # Configure defaults via env vars for FastMCP versions that removed ctor host/port kwargs.
    os.environ.setdefault("FASTMCP_HOST", "0.0.0.0")
    os.environ.setdefault("FASTMCP_PORT", "8000")
    mcp.run(transport="streamable-http")

