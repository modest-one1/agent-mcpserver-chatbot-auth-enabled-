"""
Email Tagger Tool.
Intelligently tags emails based on content analysis.
"""

import time
from mcp.server.fastmcp import Context
from models import EmailTaggerInput, TagSuggestion, EmailTaggerOutput, EmailPriority


async def tag_email(input_data: EmailTaggerInput, ctx: Context) -> EmailTaggerOutput:
    """
    Intelligently tag emails based on content analysis.
    Suggests relevant tags, categories, priority, and sentiment.
    """
    await ctx.info(f"Starting email tagging for: {input_data.email_subject[:50]}...")
    
    start_time = time.time()
    
    try:
        # Analyze content for tagging
        content = f"{input_data.email_subject} {input_data.email_body}".lower()
        
        # Keyword-based tagging logic (in production, use NLP/ML models)
        tags = []
        
        if any(word in content for word in ["invoice", "payment", "bill", "receipt"]):
            tags.append(TagSuggestion(
                tag="finance", 
                confidence=0.95, 
                category="financial", 
                reason="Contains payment-related terms"
            ))
            tags.append(TagSuggestion(
                tag="invoice", 
                confidence=0.88, 
                category="document", 
                reason="Invoice keywords detected"
            ))
        
        if any(word in content for word in ["urgent", "asap", "immediate", "deadline"]):
            tags.append(TagSuggestion(
                tag="urgent", 
                confidence=0.92, 
                category="priority", 
                reason="Urgency indicators present"
            ))
        
        if any(word in content for word in ["meeting", "schedule", "calendar", "appointment"]):
            tags.append(TagSuggestion(
                tag="meeting", 
                confidence=0.85, 
                category="scheduling", 
                reason="Scheduling terms found"
            ))
        
        if any(word in content for word in ["support", "help", "issue", "problem", "ticket"]):
            tags.append(TagSuggestion(
                tag="support", 
                confidence=0.90, 
                category="service", 
                reason="Support-related content"
            ))
        
        if any(word in content for word in ["promotion", "discount", "sale", "offer", "deal"]):
            tags.append(TagSuggestion(
                tag="promotional", 
                confidence=0.87, 
                category="marketing", 
                reason="Marketing language detected"
            ))
        
        # Add general tags if few detected
        if len(tags) < input_data.max_tags:
            tags.append(TagSuggestion(
                tag="general", 
                confidence=0.70, 
                category="misc", 
                reason="General correspondence"
            ))
        
        # Determine priority
        priority = EmailPriority.MEDIUM
        if "urgent" in content or "asap" in content:
            priority = EmailPriority.URGENT
        elif any(word in content for word in ["important", "action required"]):
            priority = EmailPriority.HIGH
        
        # Determine sentiment
        sentiment = "neutral"
        if any(word in content for word in ["thank", "great", "excellent", "appreciate"]):
            sentiment = "positive"
        elif any(word in content for word in ["complaint", "disappointed", "issue", "problem"]):
            sentiment = "negative"
        
        processing_time = int((time.time() - start_time) * 1000)
        
        await ctx.info(f"Generated {len(tags)} tags in {processing_time}ms")
        
        return EmailTaggerOutput(
            success=True,
            tags=tags[:input_data.max_tags],
            categories=list(set(t.category for t in tags)),
            priority=priority,
            sentiment=sentiment,
            processing_time_ms=processing_time
        )
    except Exception as e:
        await ctx.error(f"Email tagging failed: {str(e)}")
        return EmailTaggerOutput(
            success=False,
            tags=[],
            categories=[],
            priority=EmailPriority.LOW,
            sentiment="unknown",
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
