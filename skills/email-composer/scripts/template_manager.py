"""
Email Template Manager - Manage and generate email templates.

This module provides utilities for creating, storing, and retrieving
email templates for common business scenarios.
"""

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum


class EmailType(Enum):
    """Types of business emails."""
    INTRODUCTION = "introduction"
    REQUEST = "request"
    FOLLOW_UP = "follow_up"
    PROPOSAL = "proposal"
    THANK_YOU = "thank_you"
    APOLOGY = "apology"
    MEETING_REQUEST = "meeting_request"
    STATUS_UPDATE = "status_update"
    COVER_LETTER = "cover_letter"
    RESIGNATION = "resignation"


@dataclass
class EmailTemplate:
    """Email template structure."""
    name: str
    email_type: EmailType
    subject_template: str
    opening_template: str
    body_template: str
    closing_template: str
    placeholders: List[str]
    tone_default: str = "semiformal"


# Default templates for common email types
DEFAULT_TEMPLATES: Dict[str, EmailTemplate] = {
    "introduction": EmailTemplate(
        name="Introduction Email",
        email_type=EmailType.INTRODUCTION,
        subject_template="Introduction - {sender_name}",
        opening_template="I hope this email finds you well. My name is {sender_name}, and I am the {sender_title} at {sender_company}.",
        body_template="I am reaching out to {purpose}. {details}\n\nI would welcome the opportunity to {call_to_action}.",
        closing_template="I look forward to {follow_up_statement}. Please feel free to contact me at {sender_phone} or reply to this email.",
        placeholders=[
            "sender_name", "sender_title", "sender_company",
            "purpose", "details", "call_to_action",
            "follow_up_statement", "sender_phone"
        ],
    ),
    "follow_up": EmailTemplate(
        name="Follow-Up Email",
        email_type=EmailType.FOLLOW_UP,
        subject_template="Following Up: {original_subject}",
        opening_template="I wanted to follow up on our previous correspondence regarding {topic}.",
        body_template="As discussed, {key_points}\n\n{additional_details}\n\nI wanted to check if you have had a chance to {action_item}.",
        closing_template="Please let me know if you need any additional information. I am happy to {offer}.",
        placeholders=[
            "original_subject", "topic", "key_points",
            "additional_details", "action_item", "offer"
        ],
    ),
    "meeting_request": EmailTemplate(
        name="Meeting Request",
        email_type=EmailType.MEETING_REQUEST,
        subject_template="Meeting Request - {meeting_purpose}",
        opening_template="I would like to request a meeting to discuss {meeting_purpose}.",
        body_template="The meeting would focus on {agenda_items}.\n\nProposed dates/times:\n{proposed_times}\n\nMeeting duration: {duration}",
        closing_template="Please let me know which time works best for you, or suggest an alternative that fits your schedule.",
        placeholders=[
            "meeting_purpose", "agenda_items",
            "proposed_times", "duration"
        ],
    ),
    "thank_you": EmailTemplate(
        name="Thank You Email",
        email_type=EmailType.THANK_YOU,
        subject_template="Thank You - {reason}",
        opening_template="I wanted to express my sincere gratitude for {reason}.",
        body_template="{details}\n\nYour {contribution_type} was invaluable and {impact}.",
        closing_template="Thank you again for your support. I look forward to {future_interaction}.",
        placeholders=[
            "reason", "details", "contribution_type",
            "impact", "future_interaction"
        ],
    ),
    "request": EmailTemplate(
        name="Request Email",
        email_type=EmailType.REQUEST,
        subject_template="Request: {request_subject}",
        opening_template="I am writing to request {request_description}.",
        body_template="{background}\n\nThe specific request is: {specific_request}\n\n{justification}\n\nIf approved, this would {benefit}.",
        closing_template="Please let me know if you need any additional information to process this request. The deadline for this request is {deadline}.",
        placeholders=[
            "request_subject", "request_description",
            "background", "specific_request", "justification",
            "benefit", "deadline"
        ],
    ),
    "status_update": EmailTemplate(
        name="Status Update",
        email_type=EmailType.STATUS_UPDATE,
        subject_template="Status Update: {project_name} - {date}",
        opening_template="Here is the status update for {project_name} as of {date}.",
        body_template="**Current Status:** {status}\n\n**Completed:**\n{completed_items}\n\n**In Progress:**\n{in_progress_items}\n\n**Next Steps:**\n{next_steps}",
        closing_template="Please let me know if you have any questions or need clarification on any items.",
        placeholders=[
            "project_name", "date", "status",
            "completed_items", "in_progress_items", "next_steps"
        ],
    ),
    "apology": EmailTemplate(
        name="Apology Email",
        email_type=EmailType.APOLOGY,
        subject_template="Apology - {apology_subject}",
        opening_template="I am writing to sincerely apologize for {apology_subject}.",
        body_template="{explanation}\n\nI understand that this {impact}. I take full responsibility for {responsibility}.\n\nTo prevent this from happening again, {preventive_action}.",
        closing_template="I am committed to {commitment}. Please let me know how I can {remedy}.",
        placeholders=[
            "apology_subject", "explanation", "impact",
            "responsibility", "preventive_action",
            "commitment", "remedy"
        ],
    ),
}


class TemplateManager:
    """Manage email templates."""

    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize template manager.

        Args:
            template_dir: Directory to store custom templates
        """
        self.template_dir = template_dir or Path.home() / ".email_templates"
        self.templates = DEFAULT_TEMPLATES.copy()
        self._load_custom_templates()

    def _load_custom_templates(self) -> None:
        """Load custom templates from template directory."""
        if self.template_dir.exists():
            for template_file in self.template_dir.glob("*.json"):
                try:
                    with open(template_file, "r") as f:
                        data = json.load(f)
                        template = EmailTemplate(
                            name=data["name"],
                            email_type=EmailType(data["email_type"]),
                            subject_template=data["subject_template"],
                            opening_template=data["opening_template"],
                            body_template=data["body_template"],
                            closing_template=data["closing_template"],
                            placeholders=data["placeholders"],
                            tone_default=data.get("tone_default", "semiformal"),
                        )
                        self.templates[data["email_type"]] = template
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Warning: Could not load template {template_file}: {e}")

    def get_template(self, email_type: str) -> Optional[EmailTemplate]:
        """
        Get template by email type.

        Args:
            email_type: Type of email template to retrieve

        Returns:
            EmailTemplate if found, None otherwise
        """
        return self.templates.get(email_type)

    def list_templates(self) -> List[str]:
        """
        List all available template types.

        Returns:
            List of template names
        """
        return list(self.templates.keys())

    def fill_template(
        self,
        email_type: str,
        values: Dict[str, str],
    ) -> Dict[str, str]:
        """
        Fill a template with provided values.

        Args:
            email_type: Type of email template
            values: Dictionary of placeholder values

        Returns:
            Dictionary with filled template parts

        Raises:
            ValueError: If template not found or placeholders missing
        """
        template = self.get_template(email_type)
        if not template:
            raise ValueError(f"Template '{email_type}' not found")

        # Check for missing placeholders
        missing = set(template.placeholders) - set(values.keys())
        if missing:
            raise ValueError(f"Missing placeholders: {missing}")

        # Fill templates
        return {
            "name": template.name,
            "subject": template.subject_template.format(**values),
            "opening": template.opening_template.format(**values),
            "body": template.body_template.format(**values),
            "closing": template.closing_template.format(**values),
            "tone": template.tone_default,
        }

    def save_custom_template(
        self,
        template: EmailTemplate,
    ) -> Path:
        """
        Save a custom template to the template directory.

        Args:
            template: EmailTemplate to save

        Returns:
            Path to saved template file
        """
        self.template_dir.mkdir(parents=True, exist_ok=True)

        file_path = self.template_dir / f"{template.email_type.value}.json"
        with open(file_path, "w") as f:
            json.dump(asdict(template), f, indent=2, default=str)

        # Add to in-memory templates
        self.templates[template.email_type.value] = template

        return file_path

    def create_template_from_email(
        self,
        name: str,
        email_type: EmailType,
        subject: str,
        opening: str,
        body: str,
        closing: str,
    ) -> EmailTemplate:
        """
        Create a new template from email parts.

        Args:
            name: Template name
            email_type: Email type
            subject: Subject line (use {placeholders})
            opening: Opening paragraph (use {placeholders})
            body: Body content (use {placeholders})
            closing: Closing paragraph (use {placeholders})

        Returns:
            New EmailTemplate instance
        """
        import re

        # Extract placeholders from all parts
        pattern = r'\{(\w+)\}'
        all_text = f"{subject} {opening} {body} {closing}"
        placeholders = list(set(re.findall(pattern, all_text)))

        return EmailTemplate(
            name=name,
            email_type=email_type,
            subject_template=subject,
            opening_template=opening,
            body_template=body,
            closing_template=closing,
            placeholders=placeholders,
        )


if __name__ == "__main__":
    # Example usage
    manager = TemplateManager()

    print("Available templates:")
    for template_name in manager.list_templates():
        print(f"  - {template_name}")

    # Fill a template
    filled = manager.fill_template("meeting_request", {
        "meeting_purpose": "Q4 Budget Planning",
        "agenda_items": "1. Review current budget\n2. Discuss Q4 projections\n3. Plan resource allocation",
        "proposed_times": "Monday 2pm\nTuesday 10am\nWednesday 3pm",
        "duration": "45 minutes",
    })

    print("\n--- Generated Email ---")
    print(f"Subject: {filled['subject']}")
    print(f"\n{filled['opening']}")
    print(f"\n{filled['body']}")
    print(f"\n{filled['closing']}")