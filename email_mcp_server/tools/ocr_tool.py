"""
OCR (Optical Character Recognition) Tool.
Extracts text from images with confidence scoring.
"""

import time
from mcp.server.fastmcp import Context
from models import OcrInput, OcrOutput, OcrRegion


async def ocr_extract(input_data: OcrInput, ctx: Context) -> OcrOutput:
    """
    Extract text from images using OCR (Optical Character Recognition).
    Supports various image formats and languages with confidence scoring.
    """
    await ctx.info(f"Starting OCR extraction with language: {input_data.language}")
    
    start_time = time.time()
    
    try:
        # Simulate OCR processing (in production, use pytesseract or cloud OCR)
        sample_text = """
        INVOICE #12345
        Date: 2024-01-15
        Total: $1,250.00
        
        Thank you for your business!
        """
        
        # Calculate mock confidence based on image quality hint
        confidence = 92.5 if input_data.enhance_image else 78.0
        
        processing_time = int((time.time() - start_time) * 1000)
        
        await ctx.info(f"OCR completed in {processing_time}ms with confidence {confidence}%")
        
        return OcrOutput(
            success=True,
            text=sample_text.strip(),
            confidence=confidence,
            language_detected=input_data.language,
            processing_time_ms=processing_time,
            regions=[
                OcrRegion(x=10, y=10, width=200, height=50, text="INVOICE #12345"),
                OcrRegion(x=10, y=70, width=150, height=30, text="Date: 2024-01-15")
            ],
            errors=[]
        )
    except Exception as e:
        await ctx.error(f"OCR extraction failed: {str(e)}")
        return OcrOutput(
            success=False,
            text="",
            confidence=0.0,
            language_detected="",
            processing_time_ms=int((time.time() - start_time) * 1000),
            regions=[],
            errors=[str(e)]
        )
