"""
Email Formatter - Format and validate email structure.

This module provides utilities for formatting professional emails,
validating structure, and ensuring proper tone.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ToneLevel(Enum):
    """Email tone levels."""
    FORMAL = "formal"
    SEMIFORMAL = "semiformal"
    CASUAL = "casual"


@dataclass
class EmailComponents:
    """Structured email components."""
    subject: str
    salutation: str
    opening: str
    body: str
    closing: str
    sign_off: str
    signature: str


# Salutations by tone
SALUTATIONS = {
    ToneLevel.FORMAL: ["Dear {title} {last_name}", "Dear {full_name}"],
    ToneLevel.SEMIFORMAL: ["Dear {first_name}", "Hi {first_name}"],
    ToneLevel.CASUAL: ["Hi {first_name}", "Hey {first_name}", "Hello {first_name}"],
}

# Sign-offs by tone
SIGN_OFFS = {
    ToneLevel.FORMAL: ["Sincerely", "Best regards", "Kind regards"],
    ToneLevel.SEMIFORMAL: ["Best regards", "Best", "Regards"],
    ToneLevel.CASUAL: ["Thanks", "Best", "Cheers"],
}


def format_email(components: EmailComponents) -> str:
    """
    Format email components into a complete email string.

    Args:
        components: EmailComponents dataclass with all email parts

    Returns:
        Formatted email string
    """
    parts = [
        f"Subject: {components.subject}",
        "",
        components.salutation,
        "",
        components.opening,
        "",
        components.body,
        "",
        components.closing,
        "",
        components.sign_off,
        components.signature,
    ]
    return "\n".join(parts)


def get_salutation(
    tone: ToneLevel,
    first_name: str,
    last_name: str = "",
    title: str = "",
) -> str:
    """
    Generate appropriate salutation based on tone and recipient info.

    Args:
        tone: Desired tone level
        first_name: Recipient's first name
        last_name: Recipient's last name (optional)
        title: Recipient's title (Mr., Ms., Dr., etc.)

    Returns:
        Formatted salutation string
    """
    templates = SALUTATIONS.get(tone, SALUTATIONS[ToneLevel.SEMIFORMAL])
    template = templates[0]

    return template.format(
        first_name=first_name,
        last_name=last_name,
        title=title,
        full_name=f"{title} {last_name}".strip(),
    )


def get_sign_off(tone: ToneLevel) -> str:
    """
    Get appropriate sign-off based on tone.

    Args:
        tone: Desired tone level

    Returns:
        Sign-off string
    """
    sign_offs = SIGN_OFFS.get(tone, SIGN_OFFS[ToneLevel.SEMIFORMAL])
    return sign_offs[0]


def validate_email_structure(email: str) -> dict:
    """
    Validate that an email has proper structure.

    Args:
        email: Email content to validate

    Returns:
        Dictionary with validation results
    """
    results = {
        "valid": True,
        "issues": [],
        "has_subject": False,
        "has_salutation": False,
        "has_body": False,
        "has_sign_off": False,
    }

    lines = email.strip().split("\n")

    # Check for subject line
    for line in lines[:5]:
        if line.lower().startswith("subject:"):
            results["has_subject"] = True
            break

    # Check for common salutations
    salutation_patterns = [
        r"^Dear\s+\w+",
        r"^Hi\s+\w+",
        r"^Hello\s+\w+",
        r"^Hey\s+\w+",
    ]
    for line in lines:
        if any(re.match(p, line) for p in salutation_patterns):
            results["has_salutation"] = True
            break

    # Check for body content (non-empty lines after salutation)
    body_found = False
    for line in lines[2:]:
        if line.strip() and not any(re.match(p, line) for p in salutation_patterns):
            body_found = True
            break
    results["has_body"] = body_found

    # Check for sign-offs
    sign_offs = ["sincerely", "regards", "best", "thanks", "cheers", "best regards"]
    email_lower = email.lower()
    results["has_sign_off"] = any(s in email_lower for s in sign_offs)

    # Determine overall validity
    required = ["has_subject", "has_salutation", "has_body", "has_sign_off"]
    results["valid"] = all(results[r] for r in required)

    if not results["has_subject"]:
        results["issues"].append("Missing subject line")
    if not results["has_salutation"]:
        results["issues"].append("Missing salutation")
    if not results["has_body"]:
        results["issues"].append("Missing body content")
    if not results["has_sign_off"]:
        results["issues"].append("Missing sign-off")

    return results


def analyze_tone(email: str) -> ToneLevel:
    """
    Analyze the tone of an email.

    Args:
        email: Email content to analyze

    Returns:
        Detected ToneLevel
    """
    email_lower = email.lower()

    # Formal indicators
    formal_words = ["sincerely", "kind regards", "dear sir", "dear madam"]
    formal_count = sum(1 for w in formal_words if w in email_lower)

    # Casual indicators
    casual_words = ["hey", "cheers", "thanks!", "no worries", "sounds good"]
    casual_count = sum(1 for w in casual_words if w in email_lower)

    # Determine tone
    if formal_count > casual_count:
        return ToneLevel.FORMAL
    elif casual_count > formal_count:
        return ToneLevel.CASUAL
    else:
        return ToneLevel.SEMIFORMAL


def create_email(
    subject: str,
    recipient_name: str,
    purpose: str,
    details: str,
    closing: str,
    tone: ToneLevel = ToneLevel.SEMIFORMAL,
    sender_name: str = "",
    sender_title: str = "",
) -> str:
    """
    Create a complete email from parameters.

    Args:
        subject: Email subject line
        recipient_name: Recipient's name
        purpose: Main purpose/goal of the email
        details: Additional details
        closing: Closing statement or call to action
        tone: Desired tone level
        sender_name: Sender's name for signature
        sender_title: Sender's title/role

    Returns:
        Complete formatted email
    """
    # Parse recipient name
    name_parts = recipient_name.split()
    first_name = name_parts[0] if name_parts else ""

    salutation = get_salutation(tone, first_name)
    sign_off = get_sign_off(tone)

    components = EmailComponents(
        subject=subject,
        salutation=salutation,
        opening=purpose,
        body=details,
        closing=closing,
        sign_off=sign_off,
        signature=f"{sender_name}\n{sender_title}".strip(),
    )

    return format_email(components)


if __name__ == "__main__":
    # Example usage
    email = create_email(
        subject="Project Update - Q4 Review",
        recipient_name="John Smith",
        purpose="I wanted to provide you with an update on the Q4 project progress.",
        details="We have completed the initial phase and are moving into implementation. Key milestones achieved include:\n\n1. Requirements gathering completed\n2. Architecture finalized\n3. Development team onboarded",
        closing="Please let me know if you have any questions or need additional details.",
        tone=ToneLevel.SEMIFORMAL,
        sender_name="Jane Doe",
        sender_title="Project Manager",
    )

    print(email)
    print("\n" + "=" * 50 + "\n")
    print("Validation:", validate_email_structure(email))