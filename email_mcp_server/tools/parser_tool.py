"""
Email Parser Tool.
Parses raw email content (RFC 2822 format) into structured components.
"""

import re
import time
from mcp.server.fastmcp import Context
from models import EmailParserInput, AttachmentInfo, EmailParserOutput


async def parse_email(input_data: EmailParserInput, ctx: Context) -> EmailParserOutput:
    """
    Parse raw email content (RFC 2822 format) into structured components.
    Extracts headers, body, attachments, and links.
    """
    await ctx.info("Starting email parsing...")
    
    start_time = time.time()
    
    try:
        raw = input_data.raw_email
        
        # Parse headers
        headers = {}
        header_section = raw.split("\n\n")[0] if "\n\n" in raw else raw
        
        for line in header_section.split("\n"):
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value.strip()
        
        # Extract key fields
        subject = headers.get("Subject", "")
        from_address = headers.get("From", "")
        to_addresses = [addr.strip() for addr in headers.get("To", "").split(",") if addr.strip()]
        cc_addresses = [addr.strip() for addr in headers.get("Cc", "").split(",") if addr.strip()]
        date = headers.get("Date")
        reply_to = headers.get("Reply-To")
        
        # Extract body
        body_parts = raw.split("\n\n", 1)
        body_content = body_parts[1] if len(body_parts) > 1 else ""
        
        # Simple HTML detection
        body_html = None
        body_text = body_content
        
        if "<html" in body_content.lower() or "<!doctype" in body_content.lower():
            body_html = body_content
            # Simple HTML to text conversion (in production, use BeautifulSoup)
            body_text = re.sub(r'<[^>]+>', ' ', body_content)
            body_text = re.sub(r'\s+', ' ', body_text).strip()
        
        # Extract links
        links = []
        if input_data.extract_links:
            links = re.findall(r'https?://[^\s<>"\')\]]+', raw)
        
        # Mock attachments
        attachments = []
        if input_data.extract_attachments:
            # In production, parse MIME parts
            if "Content-Disposition: attachment" in raw:
                attachments.append(AttachmentInfo(
                    filename="document.pdf",
                    content_type="application/pdf",
                    size=102400,
                    content_id="<attachment1>"
                ))
        
        processing_time = int((time.time() - start_time) * 1000)
        
        await ctx.info(f"Email parsed successfully in {processing_time}ms")
        
        return EmailParserOutput(
            success=True,
            headers=headers,
            subject=subject,
            from_address=from_address,
            to_addresses=to_addresses,
            cc_addresses=cc_addresses,
            bcc_addresses=[],
            date=date,
            body_text=body_text[:1000] if body_text else "",
            body_html=body_html[:1000] if body_html else None,
            attachments=attachments,
            links=links[:10],
            reply_to=reply_to
        )
    except Exception as e:
        await ctx.error(f"Email parsing failed: {str(e)}")
        return EmailParserOutput(
            success=False,
            headers={},
            subject="",
            from_address="",
            to_addresses=[],
            cc_addresses=[],
            bcc_addresses=[],
            date=None,
            body_text="",
            body_html=None,
            attachments=[],
            links=[],
            reply_to=None
        )
