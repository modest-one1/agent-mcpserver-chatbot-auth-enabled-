"""
Professional Email Templates Resource.
Provides templates for common business email scenarios.
"""

import json


def get_professional_email_templates() -> str:
    """
    Professional email templates for common business scenarios.
    Includes meeting requests, follow-ups, introductions, and more.
    
    Returns:
        JSON string containing email templates
    """
    templates = {
        "meeting_request": {
            "subject": "Meeting Request: [Topic] - [Date/Time Options]",
            "body": """Dear [Name],

I hope this email finds you well. I would like to schedule a meeting to discuss [topic].

**Proposed Agenda:**
- [Agenda item 1]
- [Agenda item 2]
- [Agenda item 3]

**Suggested Times:**
1. [Date/Time Option 1]
2. [Date/Time Option 2]
3. [Date/Time Option 3]

Please let me know which option works best for you, or suggest an alternative time.

Best regards,
[Your Name]"""
        },
        "follow_up": {
            "subject": "Follow-up: [Original Subject]",
            "body": """Dear [Name],

I hope you're doing well. I'm following up on my previous email regarding [topic] sent on [date].

I understand you may be busy, but I wanted to ensure my message didn't get overlooked.

[Restate key point or question]

I look forward to hearing from you.

Best regards,
[Your Name]"""
        },
        "introduction": {
            "subject": "Introduction: [Person A] <> [Person B]",
            "body": """Dear [Name 1] and [Name 2],

I hope this email finds you both well. I'd like to introduce you to each other as I believe there may be synergies between your work.

[Name 1]: [Brief background and current focus]

[Name 2]: [Brief background and current focus]

I'll let you both take it from here. Feel free to connect directly.

Best regards,
[Your Name]"""
        },
        "thank_you": {
            "subject": "Thank You - [Occasion]",
            "body": """Dear [Name],

I wanted to express my sincere gratitude for [specific reason].

[Elaborate on the impact or significance]

I truly appreciate your [time/support/guidance/etc.].

Thank you again.

Best regards,
[Your Name]"""
        },
        "out_of_office": {
            "subject": "Out of Office: [Dates]",
            "body": """Thank you for your email.

I am currently out of the office from [start date] to [end date] with limited access to email.

For urgent matters, please contact [alternative contact name] at [email/phone].

I will respond to your message upon my return.

Best regards,
[Your Name]"""
        }
    }
    
    return json.dumps(templates, indent=2)
