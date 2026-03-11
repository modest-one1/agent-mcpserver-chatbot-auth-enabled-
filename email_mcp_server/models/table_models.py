"""
Table extraction models.
"""

from typing import Optional, List, Any
from pydantic import BaseModel, Field


class TableData(BaseModel):
    """Data structure for an extracted table."""
    table_index: int = Field(
        ..., 
        description="Table index"
    )
    headers: List[str] = Field(
        default=[], 
        description="Table headers"
    )
    rows: List[List[Any]] = Field(
        ..., 
        description="Table rows"
    )
    row_count: int = Field(
        ..., 
        description="Number of rows"
    )
    col_count: int = Field(
        ..., 
        description="Number of columns"
    )
    confidence: float = Field(
        ..., 
        description="Extraction confidence (0-100)"
    )


class TableExtractorInput(BaseModel):
    """Input parameters for table extraction."""
    source_data: str = Field(
        ..., 
        description="Email body, HTML content, or base64 document"
    )
    source_type: str = Field(
        default="html", 
        description="Type: html, pdf, image, csv, text"
    )
    table_index: Optional[int] = Field(
        default=None, 
        description="Specific table index to extract (None for all)"
    )
    output_format: str = Field(
        default="json", 
        description="Output format: json, csv, markdown, html"
    )
    include_headers: bool = Field(
        default=True, 
        description="Include table headers in output"
    )
    merge_cells: bool = Field(
        default=False, 
        description="Merge cells with same content"
    )


class TableExtractorOutput(BaseModel):
    """Output from table extraction."""
    success: bool = Field(
        ..., 
        description="Whether extraction was successful"
    )
    tables: List[TableData] = Field(
        ..., 
        description="Extracted tables"
    )
    total_tables: int = Field(
        ..., 
        description="Total number of tables found"
    )
    output_format: str = Field(
        ..., 
        description="Output format used"
    )
    processing_time_ms: int = Field(
        ..., 
        description="Processing time in milliseconds"
    )
    errors: List[str] = Field(
        default=[], 
        description="Any errors encountered"
    )
