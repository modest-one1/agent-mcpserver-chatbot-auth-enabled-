# Email Intelligence MCP Server

A comprehensive, industry-level [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for email extraction, analysis, and processing. Built with a modular architecture for easy maintenance and extensibility.

Authentication is enabled using JWT bearer-token validation (Azure Entra ID), without role-based authorization checks.

## Features

### Tools (6 Total)

| Tool | Description |
|------|-------------|
| `ocr_extract` | Extract text from images with confidence scoring |
| `extract_tables` | Extract tables from HTML/PDF/images (JSON/CSV/Markdown/HTML output) |
| `tag_email` | AI-powered email tagging with categories & sentiment |
| `classify_email` | Classify emails (invoice, spam, support, etc.) with entity extraction |
| `parse_email` | Parse RFC 2822 emails into structured components |
| `extract_entities` | Extract persons, dates, amounts, emails, phones, URLs |

### Prompts (2 Total)

| Prompt | Description |
|--------|-------------|
| `email_analysis_prompt` | Comprehensive analysis (summary, action items, sentiment, risk) |
| `email_reply_generator` | Generate professional replies with customizable tone |

### Resources (2 Total)

| Resource | Description |
|----------|-------------|
| `email-templates://professional` | 5 email templates (meeting, follow-up, intro, thank you, OOO) |
| `email-patterns://extraction` | 15 regex patterns (emails, phones, dates, currency, tracking, etc.) |

### Security

- JWT bearer authentication enabled via JWKS validation
- Token signature, issuer, and audience are validated
- No role-based authorization required (no required roles/scopes enforced by default)

## Project Structure

```
email_mcp_server/
├── server.py                   # Main entry point - registers all components
├── mcp_config.json             # Complete server configuration and schemas
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── test_server.py              # Test suite
├── README.md                   # Documentation
│
├── models/                     # Data models (Pydantic schemas)
│   ├── __init__.py
│   ├── enums.py                # Enumeration types
│   ├── ocr_models.py           # OCR input/output models
│   ├── table_models.py         # Table extraction models
│   ├── tagger_models.py        # Email tagging models
│   ├── classifier_models.py    # Email classification models
│   ├── parser_models.py        # Email parsing models
│   └── entity_models.py        # Entity extraction models
│
├── tools/                      # MCP tool implementations
│   ├── __init__.py
│   ├── ocr_tool.py             # OCR extraction tool
│   ├── table_tool.py           # Table extraction tool
│   ├── tagger_tool.py          # Email tagging tool
│   ├── classifier_tool.py      # Email classification tool
│   ├── parser_tool.py          # Email parsing tool
│   └── entity_tool.py          # Entity extraction tool
│
├── prompts/                    # MCP prompt templates
│   ├── __init__.py
│   ├── analysis_prompt.py      # Email analysis prompt
│   └── reply_prompt.py         # Reply generator prompt
│
├── resources/                  # MCP resource providers
│   ├── __init__.py
│   ├── templates_resource.py   # Email templates resource
│   └── patterns_resource.py    # Regex patterns resource
│
└── utils/                      # Helper utilities
    ├── __init__.py
    └── helpers.py              # Common helper functions
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Setup

1. Extract the archive:
```bash
unzip email_mcp_server.zip
cd email_mcp_server
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Install additional dependencies for enhanced functionality:
```bash
# For OCR support
pip install pytesseract pillow

# For PDF table extraction
pip install camelot-py pdfplumber

# For HTML parsing
pip install beautifulsoup4 lxml

# For advanced NLP
pip install spacy
python -m spacy download en_core_web_sm
```

## Usage

### Running the Server

```bash
python server.py
```

The server runs with streamable HTTP transport.

Default runtime host and port:

- Host: `0.0.0.0`
- Port: `8000`

These defaults are applied through `FASTMCP_HOST` and `FASTMCP_PORT` when not already set.

### Authentication Setup (No Role-Based Authorization)

Create a `.env` file in the project root:

```env
TENANT_ID=<your-entra-tenant-id>
CLIENT_ID=<your-api-app-client-id>
API_AUDIENCE=api://<your-api-app-client-id>
```

Auth behavior:

- Validates JWT using Azure Entra ID JWKS endpoint
- Verifies token issuer and audience
- Does not enforce role-based authorization
- Optional scope/role checks can be added later in code if needed

### Configuration with Claude Desktop

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "email-intelligence": {
      "command": "python",
      "args": ["/path/to/email_mcp_server/server.py"],
      "env": {
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## Tool Examples

### 1. OCR Extraction

```python
from models import OcrInput

# Input
input_data = OcrInput(
    image_data="base64_encoded_image_or_url",
    image_format="png",
    language="eng",
    enhance_image=True
)

# Output
{
  "success": True,
  "text": "INVOICE #12345\nDate: 2024-01-15\nTotal: $1,250.00",
  "confidence": 92.5,
  "language_detected": "eng",
  "processing_time_ms": 1250,
  "regions": [...],
  "errors": []
}
```

### 2. Table Extraction

```python
from models import TableExtractorInput

# Input
input_data = TableExtractorInput(
    source_data="<table>...</table>",
    source_type="html",
    output_format="json",
    include_headers=True
)

# Output
{
  "success": True,
  "tables": [
    {
      "table_index": 0,
      "headers": ["Item", "Price"],
      "rows": [["Product A", "$50"]],
      "row_count": 1,
      "col_count": 2,
      "confidence": 95.0
    }
  ],
  "total_tables": 1,
  "processing_time_ms": 450
}
```

### 3. Email Tagging

```python
from models import EmailTaggerInput

# Input
input_data = EmailTaggerInput(
    email_subject="Invoice #12345 - Payment Due",
    email_body="Please find attached invoice for $1,250...",
    email_from="billing@company.com",
    max_tags=5
)

# Output
{
  "success": True,
  "tags": [
    {
      "tag": "finance",
      "confidence": 0.95,
      "category": "financial",
      "reason": "Contains payment-related terms"
    }
  ],
  "categories": ["financial"],
  "priority": "high",
  "sentiment": "neutral",
  "processing_time_ms": 180
}
```

### 4. Email Classification

```python
from models import EmailClassifierInput

# Input
input_data = EmailClassifierInput(
    email_subject="URGENT: System downtime",
    email_body="Our production system has been down since 9 AM...",
    email_from="ops@company.com"
)

# Output
{
  "success": True,
  "classification": {
    "category": "support",
    "confidence": 0.92,
    "alternative_categories": [...],
    "priority": "urgent",
    "priority_confidence": 0.95,
    "key_indicators": ["Contains 'urgent'", "Contains 'downtime'"]
  },
  "entities": {
    "dates": ["9 AM"],
    "emails": ["john@company.com"],
    "phones": ["555-123-4567"]
  },
  "processing_time_ms": 220
}
```

### 5. Email Parsing

```python
from models import EmailParserInput

# Input
input_data = EmailParserInput(
    raw_email="From: sender@example.com\nTo: recipient@example.com\nSubject: Test\n\nBody content...",
    extract_attachments=True,
    extract_links=True
)

# Output
{
  "success": True,
  "headers": {...},
  "subject": "Test",
  "from_address": "sender@example.com",
  "to_addresses": ["recipient@example.com"],
  "body_text": "Body content...",
  "attachments": [...],
  "links": [...]
}
```

### 6. Entity Extraction

```python
from models import EntityExtractorInput

# Input
input_data = EntityExtractorInput(
    text="Meeting with John Smith from Acme Corp on January 15, 2024...",
    entity_types=["all"]
)

# Output
{
  "success": True,
  "entities": [
    {
      "entity": "John Smith",
      "type": "person",
      "confidence": 0.85,
      "position": {"start": 12, "end": 22},
      "normalized_value": "John Smith"
    }
  ],
  "entity_counts": {"person": 1, "email": 1},
  "processing_time_ms": 150
}
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TENANT_ID` | Azure Entra tenant ID used to build JWKS and issuer | your-tenant-id |
| `CLIENT_ID` | API application client ID | your-client-id |
| `API_AUDIENCE` | Expected token audience | api://{CLIENT_ID} |
| `FASTMCP_HOST` | FastMCP HTTP bind host | 0.0.0.0 |
| `FASTMCP_PORT` | FastMCP HTTP bind port | 8000 |
| `MCP_LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO |
| `OCR_LANGUAGE` | Default OCR language | eng |
| `MAX_IMAGE_SIZE_MB` | Maximum image size for OCR | 10 |
| `ENABLE_AI_FEATURES` | Enable AI-powered features | true |

### Settings

The server supports the following configurable settings (see `mcp_config.json`):

- **Supported Languages**: eng, fra, deu, spa, ita, por, rus, chi_sim, chi_tra, jpn, kor
- **Table Output Formats**: json, csv, markdown, html
- **Email Categories**: invoice, receipt, spam, promotional, personal, work, support, newsletter, other
- **Priority Levels**: low, medium, high, urgent

## Development

### Adding a New Tool

1. Create a new file in `tools/` directory (e.g., `tools/my_tool.py`):

```python
from mcp.server.fastmcp import Context
from models import MyToolInput, MyToolOutput

async def my_tool(input_data: MyToolInput, ctx: Context) -> MyToolOutput:
    """Tool description"""
    await ctx.info("Processing...")
    # Implementation
    return MyToolOutput(success=True, ...)
```

2. Add models in `models/` directory:

```python
# models/my_tool_models.py
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    param: str = Field(..., description="Parameter")

class MyToolOutput(BaseModel):
    success: bool = Field(..., description="Success flag")
```

3. Register in `server.py`:

```python
from tools import my_tool

@mcp.tool()
async def my_tool_tool(input_data, ctx):
    """Tool description"""
    return await my_tool(input_data, ctx)
```

4. Update `mcp_config.json` with schema

### Testing

```bash
# Run all tests
python test_server.py

# Run the server in development mode
python server.py

# Test with MCP Inspector (if available)
npx @modelcontextprotocol/inspector python server.py
```

## Module Overview

### Models (`models/`)

Contains all Pydantic data models organized by feature:

- **enums.py**: Shared enumeration types (EmailPriority, EmailCategory, etc.)
- **ocr_models.py**: OCR input/output schemas
- **table_models.py**: Table extraction schemas
- **tagger_models.py**: Email tagging schemas
- **classifier_models.py**: Email classification schemas
- **parser_models.py**: Email parsing schemas
- **entity_models.py**: Entity extraction schemas

### Tools (`tools/`)

Each tool is in its own file for easy maintenance:

- **ocr_tool.py**: Image text extraction
- **table_tool.py**: Table extraction from documents
- **tagger_tool.py**: Email content tagging
- **classifier_tool.py**: Email categorization
- **parser_tool.py**: RFC 2822 email parsing
- **entity_tool.py**: Named entity recognition

### Prompts (`prompts/`)

Prompt templates for LLM interactions:

- **analysis_prompt.py**: Comprehensive email analysis
- **reply_prompt.py**: Professional reply generation

### Resources (`resources/`)

Static resource providers:

- **templates_resource.py**: Email templates
- **patterns_resource.py**: Regex patterns

### Utils (`utils/`)

Shared helper functions:

- **helpers.py**: Common utilities (formatting, sanitization, etc.)

## Input/Output Schemas

All tools follow strict JSON Schema definitions:

- **Input Schemas**: Define required fields, types, defaults, and validation rules
- **Output Schemas**: Define response structure with success flags, data, and error handling
- **Examples**: Each tool includes example inputs and outputs

See `mcp_config.json` for complete schema definitions.

## Rate Limits

| Tool | Requests/Minute |
|------|----------------|
| ocr_extract | 60 |
| extract_tables | 100 |
| tag_email | 200 |
| classify_email | 150 |
| parse_email | 300 |
| extract_entities | 250 |

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Support

For issues, questions, or feature requests:

- Open an issue on GitHub
- Contact: support@example.com

## Changelog

### v1.0.0 (2024-01-15)

- Initial release with modular architecture
- 6 tools: OCR, table extraction, tagging, classification, parsing, entity extraction
- 2 prompts: analysis and reply generation
- 2 resources: email templates and regex patterns
- Full JSON Schema definitions for all inputs/outputs
- Comprehensive documentation

### v1.1.0 (2026-03-10)

- Enabled JWT authentication with Azure Entra ID (JWKS-based validation)
- Added documentation for auth setup using `TENANT_ID`, `CLIENT_ID`, and `API_AUDIENCE`
- Clarified that role-based authorization is not required by default
- Updated runtime docs for streamable HTTP transport and `FASTMCP_HOST`/`FASTMCP_PORT`

---

**Built with [MCP SDK](https://github.com/modelcontextprotocol/python-sdk)**
