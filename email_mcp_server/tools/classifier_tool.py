"""
Email Classifier Tool.
Classifies emails into categories with confidence scores.
"""

import re
import time
from mcp.server.fastmcp import Context
from models import (
    EmailClassifierInput, 
    ClassificationResult, 
    EmailClassifierOutput,
    EmailCategory,
    EmailPriority
)


async def classify_email(input_data: EmailClassifierInput, ctx: Context) -> EmailClassifierOutput:
    """
    Classify emails into categories with confidence scores.
    Extracts entities and determines priority level.
    """
    await ctx.info(f"Starting email classification: {input_data.email_subject[:50]}...")
    
    start_time = time.time()
    
    try:
        content = f"{input_data.email_subject} {input_data.email_body}".lower()
        
        # Classification logic
        category_scores = {}
        
        # Invoice detection
        if any(word in content for word in ["invoice", "bill", "payment due", "amount due"]):
            category_scores[EmailCategory.INVOICE] = 0.92
        
        # Receipt detection
        if any(word in content for word in ["receipt", "payment received", "thank you for your payment"]):
            category_scores[EmailCategory.RECEIPT] = 0.88
        
        # Spam detection
        if any(word in content for word in ["free", "win", "prize", "click here", "limited time", "act now"]):
            category_scores[EmailCategory.SPAM] = 0.75
        
        # Promotional detection
        if any(word in content for word in ["sale", "discount", "offer", "promotion", "deal", "save"]):
            category_scores[EmailCategory.PROMOTIONAL] = 0.85
        
        # Newsletter detection
        if any(word in content for word in ["newsletter", "subscribe", "unsubscribe", "update", "news"]):
            category_scores[EmailCategory.NEWSLETTER] = 0.80
        
        # Support detection
        if any(word in content for word in ["support", "help desk", "ticket", "issue", "problem"]):
            category_scores[EmailCategory.SUPPORT] = 0.87
        
        # Work detection
        if any(word in content for word in ["project", "deadline", "report", "meeting", "team"]):
            category_scores[EmailCategory.WORK] = 0.78
        
        # Default to OTHER if no strong match
        if not category_scores:
            category_scores[EmailCategory.OTHER] = 0.60
        
        # Get primary category
        primary_category = max(category_scores, key=category_scores.get)
        primary_confidence = category_scores[primary_category]
        
        # Alternative categories
        alternatives = [
            {"category": cat.value, "score": score}
            for cat, score in sorted(category_scores.items(), key=lambda x: x[1], reverse=True)[1:3]
        ]
        
        # Priority determination
        priority = EmailPriority.MEDIUM
        priority_confidence = 0.70
        
        if any(word in content for word in ["urgent", "asap", "emergency", "critical"]):
            priority = EmailPriority.URGENT
            priority_confidence = 0.90
        elif any(word in content for word in ["important", "action required", "please review"]):
            priority = EmailPriority.HIGH
            priority_confidence = 0.82
        elif primary_category == EmailCategory.SPAM:
            priority = EmailPriority.LOW
            priority_confidence = 0.85
        
        # Key indicators
        indicators = []
        if "invoice" in content:
            indicators.append("Contains 'invoice'")
        if "payment" in content:
            indicators.append("Contains 'payment'")
        if "urgent" in content:
            indicators.append("Marked as urgent")
        if input_data.attachments:
            indicators.append(f"Has {len(input_data.attachments)} attachment(s)")
        
        # Entity extraction
        entities = {
            "dates": re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b', input_data.email_body),
            "emails": re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', input_data.email_body),
            "amounts": re.findall(r'\$[\d,]+\.?\d*|\b\d+\.\d{2}\b', input_data.email_body),
            "phones": re.findall(r'\b\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', input_data.email_body),
            "urls": re.findall(r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?', input_data.email_body)
        }
        
        processing_time = int((time.time() - start_time) * 1000)
        
        await ctx.info(f"Classification complete: {primary_category.value} in {processing_time}ms")
        
        return EmailClassifierOutput(
            success=True,
            classification=ClassificationResult(
                category=primary_category,
                confidence=primary_confidence,
                alternative_categories=alternatives,
                priority=priority,
                priority_confidence=priority_confidence,
                key_indicators=indicators
            ),
            entities=entities,
            processing_time_ms=processing_time
        )
    except Exception as e:
        await ctx.error(f"Email classification failed: {str(e)}")
        return EmailClassifierOutput(
            success=False,
            classification=ClassificationResult(
                category=EmailCategory.OTHER,
                confidence=0.0,
                alternative_categories=[],
                priority=EmailPriority.LOW,
                priority_confidence=0.0,
                key_indicators=[]
            ),
            entities={},
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
