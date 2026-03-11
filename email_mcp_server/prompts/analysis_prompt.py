"""
Email Analysis Prompt.
Comprehensive analysis template for extracting insights from emails.
"""


def email_analysis_prompt(email_subject: str, email_body: str, email_from: str = "") -> str:
    """
    Comprehensive email analysis prompt for extracting insights and action items.
    Use this prompt to analyze email content thoroughly.
    
    Args:
        email_subject: Email subject line
        email_body: Email body content
        email_from: Sender email address (optional)
    
    Returns:
        A structured prompt template for comprehensive email analysis
    """
    return f"""Please analyze the following email comprehensively:

**FROM:** {email_from}
**SUBJECT:** {email_subject}

**BODY:**
{email_body}

Please provide:

1. **Summary** - A brief summary of the email content (2-3 sentences)

2. **Key Points** - Bullet points of the main information

3. **Action Items** - Any tasks or actions required, with:
   - Action description
   - Who is responsible (if mentioned)
   - Deadline (if mentioned)
   - Priority level

4. **Entities Extracted**:
   - People mentioned
   - Organizations
   - Dates and times
   - Monetary amounts
   - Important numbers

5. **Sentiment Analysis**:
   - Overall tone (positive, negative, neutral)
   - Urgency level
   - Any emotional indicators

6. **Category Suggestions**:
   - Primary category (Work, Personal, Finance, Support, etc.)
   - Tags that would be appropriate

7. **Recommended Response**:
   - Whether a response is needed
   - Suggested response tone
   - Key points to address

8. **Risk Assessment**:
   - Any potential issues or concerns
   - Spam/phishing indicators
   - Confidentiality considerations
"""
