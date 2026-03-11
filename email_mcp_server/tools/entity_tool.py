"""
Entity Extraction Tool.
Extracts named entities from email text using NLP patterns.
"""

import re
import time
from mcp.server.fastmcp import Context
from models import EntityExtractorInput, ExtractedEntity, EntityExtractorOutput


async def extract_entities(input_data: EntityExtractorInput, ctx: Context) -> EntityExtractorOutput:
    """
    Extract named entities from email text.
    Identifies persons, organizations, dates, amounts, emails, phones, and addresses.
    """
    await ctx.info(f"Starting entity extraction for types: {input_data.entity_types}")
    
    start_time = time.time()
    
    try:
        text = input_data.text
        entities = []
        entity_types = input_data.entity_types
        extract_all = "all" in entity_types
        
        # Person extraction (simple pattern - in production use NER model)
        if extract_all or "person" in entity_types:
            person_pattern = r'\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b'
            for match in re.finditer(person_pattern, text):
                if match.group() not in ["The", "This", "That", "From", "Subject"]:
                    entities.append(ExtractedEntity(
                        entity=match.group(),
                        type="person",
                        confidence=0.75,
                        position={"start": match.start(), "end": match.end()},
                        normalized_value=match.group()
                    ))
        
        # Email extraction
        if extract_all or "email" in entity_types:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            for match in re.finditer(email_pattern, text):
                entities.append(ExtractedEntity(
                    entity=match.group(),
                    type="email",
                    confidence=0.99,
                    position={"start": match.start(), "end": match.end()},
                    normalized_value=match.group().lower()
                ))
        
        # Phone extraction
        if extract_all or "phone" in entity_types:
            phone_pattern = r'\b\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b|\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
            for match in re.finditer(phone_pattern, text):
                entities.append(ExtractedEntity(
                    entity=match.group(),
                    type="phone",
                    confidence=0.90,
                    position={"start": match.start(), "end": match.end()},
                    normalized_value=re.sub(r'\D', '', match.group())
                ))
        
        # Date extraction
        if extract_all or "date" in entity_types:
            date_patterns = [
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
                r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b',
                r'\b\d{4}-\d{2}-\d{2}\b'
            ]
            for pattern in date_patterns:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    entities.append(ExtractedEntity(
                        entity=match.group(),
                        type="date",
                        confidence=0.85,
                        position={"start": match.start(), "end": match.end()},
                        normalized_value=match.group()
                    ))
        
        # Amount extraction
        if extract_all or "amount" in entity_types:
            amount_pattern = r'\$[\d,]+\.?\d*|\b\d+\.\d{2}\b|\b\d{1,3}(?:,\d{3})+\b'
            for match in re.finditer(amount_pattern, text):
                entities.append(ExtractedEntity(
                    entity=match.group(),
                    type="amount",
                    confidence=0.88,
                    position={"start": match.start(), "end": match.end()},
                    normalized_value=match.group().replace("$", "").replace(",", "")
                ))
        
        # Organization extraction (simple pattern)
        if extract_all or "organization" in entity_types:
            org_pattern = r'\b([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)+(?:\s+(?:Inc|LLC|Ltd|Corp|Company|Co\.))?)\b'
            for match in re.finditer(org_pattern, text):
                if match.group() not in ["The", "This"]:
                    entities.append(ExtractedEntity(
                        entity=match.group(),
                        type="organization",
                        confidence=0.70,
                        position={"start": match.start(), "end": match.end()},
                        normalized_value=match.group()
                    ))
        
        # URL extraction
        if extract_all or "url" in entity_types:
            url_pattern = r'https?://[^\s<>"\')\]]+'
            for match in re.finditer(url_pattern, text):
                entities.append(ExtractedEntity(
                    entity=match.group(),
                    type="url",
                    confidence=0.95,
                    position={"start": match.start(), "end": match.end()},
                    normalized_value=match.group()
                ))
        
        # Count by type
        entity_counts = {}
        for entity in entities:
            entity_counts[entity.type] = entity_counts.get(entity.type, 0) + 1
        
        processing_time = int((time.time() - start_time) * 1000)
        
        await ctx.info(f"Extracted {len(entities)} entities in {processing_time}ms")
        
        return EntityExtractorOutput(
            success=True,
            entities=entities,
            entity_counts=entity_counts,
            processing_time_ms=processing_time
        )
    except Exception as e:
        await ctx.error(f"Entity extraction failed: {str(e)}")
        return EntityExtractorOutput(
            success=False,
            entities=[],
            entity_counts={},
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
