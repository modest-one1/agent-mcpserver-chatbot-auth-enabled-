"""
Email Reply Generator Prompt.
Template for generating professional email replies.
"""


def email_reply_generator(
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
    
    Returns:
        A structured prompt template for generating email replies
    """
    return f"""Please draft a reply to the following email:

**ORIGINAL EMAIL:**
From: {email_from}
Subject: {email_subject}

{email_body}

**REPLY REQUIREMENTS:**
- Tone: {tone}
- Key points to address: {key_points if key_points else "Address all main points from the original email"}

Please generate:

1. **Subject Line** - Appropriate reply subject (typically "Re: {email_subject}")

2. **Greeting** - Professional greeting appropriate for the relationship

3. **Opening** - Acknowledge receipt and thank them if appropriate

4. **Body** - Address all key points:
   - Answer any questions
   - Address concerns
   - Provide requested information
   - Set expectations for next steps

5. **Closing** - Professional sign-off with clear next actions

6. **Signature** - Appropriate closing (Best regards, Thanks, etc.)

**GUIDELINES:**
- Keep it concise but complete
- Match the formality level of the original email
- Be courteous and professional
- Include any necessary disclaimers
- Proofread for clarity and tone
"""
