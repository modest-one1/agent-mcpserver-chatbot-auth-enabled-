"""
Email Extraction Patterns Resource.
Provides regex patterns for extracting data from emails.
"""

import json


def get_email_extraction_patterns() -> str:
    """
    Common regex patterns for email content extraction.
    Useful for parsing dates, amounts, phone numbers, and more.
    
    Returns:
        JSON string containing regex patterns
    """
    patterns = {
        "email_address": {
            "pattern": r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b',
            "description": "Extract email addresses",
            "example": "contact@example.com"
        },
        "phone_number_us": {
            "pattern": r'\\(?(\\d{3})\\)?[-.\\s]?(\\d{3})[-.\\s]?(\\d{4})',
            "description": "US phone numbers in various formats",
            "example": "(555) 123-4567, 555-123-4567"
        },
        "phone_number_international": {
            "pattern": r'\\+?\\d{1,3}[-.\\s]?\\(?(\\d{1,4})\\)?[-.\\s]?(\\d{1,4})[-.\\s]?(\\d{1,9})',
            "description": "International phone numbers",
            "example": "+1-555-123-4567"
        },
        "date_us": {
            "pattern": r'\\b(0?[1-9]|1[0-2])[/-](0?[1-9]|[12]\\d|3[01])[/-](\\d{2}|\\d{4})\\b',
            "description": "US date format (MM/DD/YYYY)",
            "example": "12/31/2024, 1/1/25"
        },
        "date_iso": {
            "pattern": r'\\b\\d{4}-\\d{2}-\\d{2}\\b',
            "description": "ISO 8601 date format",
            "example": "2024-12-31"
        },
        "date_verbose": {
            "pattern": r'\\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \\d{1,2},? \\d{4}\\b',
            "description": "Verbose date format",
            "example": "January 15, 2024, Dec 1, 2024"
        },
        "currency": {
            "pattern": r'\\$[\\d,]+\\.?\\d*',
            "description": "Currency amounts with dollar sign",
            "example": "$1,234.56, $50"
        },
        "currency_decimal": {
            "pattern": r'\\b\\d+\\.\\d{2}\\b',
            "description": "Decimal amounts (likely currency)",
            "example": "1234.56"
        },
        "invoice_number": {
            "pattern": r'(?i)(?:invoice|inv)[#\\s:]?\\s*([A-Z0-9-]+)',
            "description": "Invoice numbers",
            "example": "Invoice #12345, INV-2024-001"
        },
        "order_number": {
            "pattern": r'(?i)(?:order|ord)[#\\s:]?\\s*([A-Z0-9-]+)',
            "description": "Order numbers",
            "example": "Order #ABC123, ORD-456"
        },
        "tracking_number": {
            "pattern": r'\\b(1Z[A-Z0-9]{16}|[A-Z]{2}\\d{9}[A-Z]{2}|\\d{12,22})\\b',
            "description": "Common tracking number formats (UPS, FedEx, USPS)",
            "example": "1Z999AA10123456784"
        },
        "url": {
            "pattern": r'https?://(?:[-\\w.])+(?:[:\\d]+)?(?:/(?:[\\w/_.])*(?:\\?(?:[\\w&=%.])*)?(?:#(?:[\\w.])*)?)?',
            "description": "HTTP/HTTPS URLs",
            "example": "https://example.com/path?query=value"
        },
        "credit_card": {
            "pattern": r'\\b(?:\\d{4}[-\\s]?){3}\\d{4}\\b',
            "description": "Credit card numbers (masked recommended)",
            "example": "1234-5678-9012-3456"
        },
        "ssn": {
            "pattern": r'\\b\\d{3}-\\d{2}-\\d{4}\\b',
            "description": "US Social Security Numbers",
            "example": "123-45-6789"
        },
        "ip_address": {
            "pattern": r'\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b',
            "description": "IPv4 addresses",
            "example": "192.168.1.1"
        },
        "postal_code_us": {
            "pattern": r'\\b\\d{5}(?:-\\d{4})?\\b',
            "description": "US ZIP codes",
            "example": "12345, 12345-6789"
        }
    }
    
    return json.dumps(patterns, indent=2)
