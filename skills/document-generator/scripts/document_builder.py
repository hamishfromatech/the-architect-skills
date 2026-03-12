"""
Document Builder - Build documents from templates.

This module provides utilities for creating professional business
documents from templates with support for various formats.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import re


class DocumentType(Enum):
    """Types of business documents."""
    PROPOSAL = "proposal"
    CONTRACT = "contract"
    REPORT = "report"
    MEMO = "memo"
    LETTER = "letter"
    AGREEMENT = "agreement"
    INVOICE = "invoice"
    BRIEF = "brief"


class DocumentFormat(Enum):
    """Output formats for documents."""
    MARKDOWN = "markdown"
    HTML = "html"
    PLAINTEXT = "plaintext"


@dataclass
class DocumentSection:
    """A section within a document."""
    title: str
    content: str
    subsections: List["DocumentSection"] = field(default_factory=list)
    level: int = 1


@dataclass
class Document:
    """A complete document structure."""
    title: str
    document_type: DocumentType
    sections: List[DocumentSection]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_date: date = field(default_factory=date.today)
    version: str = "1.0"


class DocumentBuilder:
    """Build documents from templates and components."""

    def __init__(self):
        """Initialize the document builder."""
        self.section_counter = 0

    def create_section(
        self,
        title: str,
        content: str,
        level: int = 1,
        subsections: Optional[List[DocumentSection]] = None,
    ) -> DocumentSection:
        """
        Create a document section.

        Args:
            title: Section title
            content: Section content
            level: Heading level (1-6)
            subsections: List of child sections

        Returns:
            DocumentSection instance
        """
        return DocumentSection(
            title=title,
            content=content,
            level=level,
            subsections=subsections or [],
        )

    def build_document(
        self,
        title: str,
        document_type: DocumentType,
        sections: List[DocumentSection],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Document:
        """
        Build a complete document.

        Args:
            title: Document title
            document_type: Type of document
            sections: List of document sections
            metadata: Additional document metadata

        Returns:
            Document instance
        """
        return Document(
            title=title,
            document_type=document_type,
            sections=sections,
            metadata=metadata or {},
        )

    def render_markdown(self, document: Document) -> str:
        """
        Render document as Markdown.

        Args:
            document: Document to render

        Returns:
            Markdown formatted string
        """
        lines = []

        # Title and metadata
        lines.append(f"# {document.title}")
        lines.append("")
        lines.append(f"**Document Type:** {document.document_type.value.title()}")
        lines.append(f"**Date:** {document.created_date.strftime('%B %d, %Y')}")
        lines.append(f"**Version:** {document.version}")

        # Additional metadata
        if document.metadata:
            for key, value in document.metadata.items():
                lines.append(f"**{key.title()}:** {value}")

        lines.append("")
        lines.append("---")
        lines.append("")

        # Render sections
        for section in document.sections:
            lines.extend(self._render_section_markdown(section))

        return "\n".join(lines)

    def _render_section_markdown(
        self,
        section: DocumentSection,
        parent_number: str = "",
    ) -> List[str]:
        """
        Render a section as Markdown.

        Args:
            section: Section to render
            parent_number: Parent section number for nesting

        Returns:
            List of Markdown lines
        """
        lines = []

        # Generate section number
        self.section_counter += 1
        section_num = f"{parent_number}{self.section_counter}" if parent_number else str(self.section_counter)

        # Heading
        heading_prefix = "#" * (section.level + 1)
        lines.append(f"{heading_prefix} {section_num}. {section.title}")
        lines.append("")

        # Content
        if section.content:
            lines.append(section.content)
            lines.append("")

        # Subsections
        for i, subsection in enumerate(section.subsections, 1):
            self.section_counter = 0  # Reset for subsections
            lines.extend(self._render_section_markdown(subsection, f"{section_num}."))

        return lines

    def render_html(self, document: Document) -> str:
        """
        Render document as HTML.

        Args:
            document: Document to render

        Returns:
            HTML formatted string
        """
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            f"<title>{document.title}</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; margin: 40px; }",
            "h1 { color: #333; }",
            "h2 { color: #444; margin-top: 30px; }",
            "h3 { color: #555; }",
            ".metadata { color: #666; margin-bottom: 20px; }",
            ".section { margin: 20px 0; }",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{document.title}</h1>",
            "<div class='metadata'>",
            f"<p><strong>Document Type:</strong> {document.document_type.value.title()}</p>",
            f"<p><strong>Date:</strong> {document.created_date.strftime('%B %d, %Y')}</p>",
            f"<p><strong>Version:</strong> {document.version}</p>",
        ]

        # Additional metadata
        for key, value in document.metadata.items():
            html_parts.append(f"<p><strong>{key.title()}:</strong> {value}</p>")

        html_parts.append("</div>")
        html_parts.append("<hr>")

        # Render sections
        for section in document.sections:
            html_parts.extend(self._render_section_html(section))

        html_parts.extend(["</body>", "</html>"])
        return "\n".join(html_parts)

    def _render_section_html(self, section: DocumentSection) -> List[str]:
        """
        Render a section as HTML.

        Args:
            section: Section to render

        Returns:
            List of HTML lines
        """
        parts = []
        tag = f"h{section.level + 1}"
        parts.append(f"<div class='section'>")
        parts.append(f"<{tag}>{section.title}</{tag}>")
        if section.content:
            # Convert newlines to paragraphs
            paragraphs = section.content.split("\n\n")
            for p in paragraphs:
                if p.strip():
                    parts.append(f"<p>{p.strip()}</p>")

        # Subsections
        for subsection in section.subsections:
            parts.extend(self._render_section_html(subsection))

        parts.append("</div>")
        return parts

    def save_document(
        self,
        document: Document,
        output_path: Path,
        format: DocumentFormat = DocumentFormat.MARKDOWN,
    ) -> Path:
        """
        Save document to file.

        Args:
            document: Document to save
            output_path: Path to save to
            format: Output format

        Returns:
            Path to saved file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        content = ""
        if format == DocumentFormat.MARKDOWN:
            content = self.render_markdown(document)
        elif format == DocumentFormat.HTML:
            content = self.render_html(document)
        elif format == DocumentFormat.PLAINTEXT:
            content = self._render_plaintext(document)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return output_path

    def _render_plaintext(self, document: Document) -> str:
        """Render document as plain text."""
        lines = []
        lines.append(document.title.upper())
        lines.append("=" * len(document.title))
        lines.append("")
        lines.append(f"Document Type: {document.document_type.value.title()}")
        lines.append(f"Date: {document.created_date.strftime('%B %d, %Y')}")
        lines.append(f"Version: {document.version}")
        lines.append("")

        for section in document.sections:
            lines.extend(self._render_section_plaintext(section))

        return "\n".join(lines)

    def _render_section_plaintext(self, section: DocumentSection) -> List[str]:
        """Render section as plain text."""
        lines = []
        indent = "  " * (section.level - 1)
        lines.append(f"{indent}{section.title}")
        lines.append(f"{indent}{'-' * len(section.title)}")
        if section.content:
            lines.append(f"{indent}{section.content}")
        lines.append("")

        for subsection in section.subsections:
            lines.extend(self._render_section_plaintext(subsection))

        return lines


# Convenience functions for common document types

def create_proposal(
    title: str,
    executive_summary: str,
    problem_statement: str,
    proposed_solution: str,
    timeline: str,
    pricing: str,
    terms: Optional[str] = None,
) -> Document:
    """
    Create a proposal document.

    Args:
        title: Proposal title
        executive_summary: Brief summary
        problem_statement: Problem being solved
        proposed_solution: The solution
        timeline: Project timeline
        pricing: Pricing details
        terms: Terms and conditions

    Returns:
        Document instance
    """
    builder = DocumentBuilder()

    sections = [
        builder.create_section("Executive Summary", executive_summary),
        builder.create_section("Problem Statement", problem_statement),
        builder.create_section("Proposed Solution", proposed_solution),
        builder.create_section("Timeline", timeline),
        builder.create_section("Pricing", pricing),
    ]

    if terms:
        sections.append(builder.create_section("Terms & Conditions", terms))

    return builder.build_document(
        title=title,
        document_type=DocumentType.PROPOSAL,
        sections=sections,
    )


def create_memo(
    title: str,
    to: List[str],
    from_: str,
    date: str,
    subject: str,
    body: str,
) -> Document:
    """
    Create a memo document.

    Args:
        title: Memo title
        to: List of recipients
        from_: Sender
        date: Memo date
        subject: Memo subject
        body: Memo content

    Returns:
        Document instance
    """
    builder = DocumentBuilder()

    header = f"To: {', '.join(to)}\nFrom: {from_}\nDate: {date}\nSubject: {subject}"

    sections = [
        builder.create_section("Header", header),
        builder.create_section("Content", body),
    ]

    return builder.build_document(
        title=title,
        document_type=DocumentType.MEMO,
        sections=sections,
        metadata={"To": ", ".join(to), "From": from_, "Subject": subject},
    )


if __name__ == "__main__":
    # Example: Create a proposal
    proposal = create_proposal(
        title="Website Redesign Proposal",
        executive_summary="This proposal outlines a comprehensive website redesign project that will modernize your online presence and improve user engagement.",
        problem_statement="The current website is outdated, not mobile-responsive, and has poor SEO performance.",
        proposed_solution="We propose a complete redesign using modern technologies with a focus on user experience and performance.",
        timeline="Phase 1: Discovery (2 weeks)\nPhase 2: Design (4 weeks)\nPhase 3: Development (8 weeks)\nPhase 4: Testing (2 weeks)",
        pricing="Total Investment: $50,000\nPayment Terms: 50% upfront, 50% on completion",
    )

    builder = DocumentBuilder()
    print(builder.render_markdown(proposal))