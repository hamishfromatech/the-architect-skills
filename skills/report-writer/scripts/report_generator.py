"""
Report Generator - Generate business reports from templates.

This module provides utilities for creating various types of
business reports with proper structure and formatting.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Dict, List, Optional, Any
from pathlib import Path


class ReportType(Enum):
    """Types of business reports."""
    STATUS = "status"
    PROGRESS = "progress"
    ANALYSIS = "analysis"
    EXECUTIVE_SUMMARY = "executive_summary"
    INCIDENT = "incident"
    INVESTIGATION = "investigation"
    FINANCIAL = "financial"
    PERFORMANCE = "performance"


class ReportFormat(Enum):
    """Output formats for reports."""
    MARKDOWN = "markdown"
    HTML = "html"
    PLAINTEXT = "plaintext"


@dataclass
class Metric:
    """A report metric with value and trend."""
    name: str
    value: Any
    target: Optional[Any] = None
    unit: Optional[str] = None
    trend: Optional[str] = None  # "up", "down", "stable"


@dataclass
class Section:
    """A report section."""
    title: str
    content: str
    subsections: List["Section"] = field(default_factory=list)
    metrics: List[Metric] = field(default_factory=list)


@dataclass
class ActionItem:
    """An action item from the report."""
    task: str
    owner: Optional[str] = None
    due_date: Optional[date] = None
    status: str = "pending"


@dataclass
class Report:
    """A complete report structure."""
    title: str
    report_type: ReportType
    author: str
    date: date
    status: str = "On Track"  # On Track, At Risk, Off Track
    summary: str = ""
    sections: List[Section] = field(default_factory=list)
    metrics: List[Metric] = field(default_factory=list)
    action_items: List[ActionItem] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ReportGenerator:
    """Generate business reports."""

    def __init__(self):
        """Initialize the report generator."""
        pass

    def create_status_report(
        self,
        title: str,
        author: str,
        period: str,
        completed: List[str],
        in_progress: List[str],
        upcoming: List[str],
        blockers: List[str] = None,
        next_steps: List[str] = None,
        status: str = "On Track",
    ) -> Report:
        """
        Create a status report.

        Args:
            title: Report title
            author: Author name
            period: Reporting period
            completed: Items completed
            in_progress: Items in progress
            upcoming: Upcoming items
            blockers: Current blockers
            next_steps: Next steps
            status: Overall status

        Returns:
            Report instance
        """
        sections = [
            Section(
                title="Completed This Period",
                content="\n".join(f"- ✅ {item}" for item in completed),
            ),
            Section(
                title="In Progress",
                content="\n".join(f"- 🔄 {item}" for item in in_progress),
            ),
            Section(
                title="Upcoming",
                content="\n".join(f"- 📋 {item}" for item in upcoming),
            ),
        ]

        if blockers:
            sections.append(Section(
                title="Blockers & Risks",
                content="\n".join(f"- ⚠️ {item}" for item in blockers),
            ))

        return Report(
            title=f"Status Report: {title}",
            report_type=ReportType.STATUS,
            author=author,
            date=date.today(),
            status=status,
            summary=f"Status report for {period}",
            sections=sections,
            risks=blockers or [],
            next_steps=next_steps or [],
            metadata={"period": period},
        )

    def create_progress_report(
        self,
        title: str,
        author: str,
        project_name: str,
        milestones: List[Dict[str, Any]],
        overall_progress: float,
        status: str = "On Track",
    ) -> Report:
        """
        Create a progress report.

        Args:
            title: Report title
            author: Author name
            project_name: Project name
            milestones: List of milestone dicts with name, status, progress
            overall_progress: Overall completion percentage
            status: Project status

        Returns:
            Report instance
        """
        # Build milestones content
        milestone_content = []
        for m in milestones:
            status_icon = "✅" if m.get("status") == "completed" else "🔄"
            progress = m.get("progress", 0)
            milestone_content.append(
                f"- {status_icon} **{m['name']}**: {progress}%"
            )

        sections = [
            Section(
                title="Project Overview",
                content=f"Project: {project_name}\nOverall Progress: {overall_progress}%",
            ),
            Section(
                title="Milestones",
                content="\n".join(milestone_content),
            ),
        ]

        metrics = [
            Metric(
                name="Overall Progress",
                value=overall_progress,
                unit="%",
                target=100,
            ),
        ]

        return Report(
            title=title,
            report_type=ReportType.PROGRESS,
            author=author,
            date=date.today(),
            status=status,
            summary=f"Progress report for {project_name}",
            sections=sections,
            metrics=metrics,
            metadata={"project": project_name},
        )

    def create_executive_summary(
        self,
        title: str,
        author: str,
        key_points: List[str],
        metrics: List[Metric] = None,
        recommendations: List[str] = None,
        decisions_needed: List[str] = None,
    ) -> Report:
        """
        Create an executive summary.

        Args:
            title: Summary title
            author: Author name
            key_points: Key points to highlight
            metrics: Key metrics
            recommendations: Recommendations
            decisions_needed: Decisions needed

        Returns:
            Report instance
        """
        sections = [
            Section(
                title="Key Points",
                content="\n".join(f"- {point}" for point in key_points),
            ),
        ]

        if recommendations:
            sections.append(Section(
                title="Recommendations",
                content="\n".join(f"- {rec}" for rec in recommendations),
            ))

        if decisions_needed:
            sections.append(Section(
                title="Decisions Needed",
                content="\n".join(f"- ❓ {d}" for d in decisions_needed),
            ))

        return Report(
            title=f"Executive Summary: {title}",
            report_type=ReportType.EXECUTIVE_SUMMARY,
            author=author,
            date=date.today(),
            summary="\n".join(key_points[:3]),  # First 3 points as summary
            sections=sections,
            metrics=metrics or [],
            next_steps=decisions_needed or [],
        )

    def render_markdown(self, report: Report) -> str:
        """
        Render report as Markdown.

        Args:
            report: Report to render

        Returns:
            Markdown formatted string
        """
        lines = []

        # Title and header
        status_emoji = {
            "On Track": "🟢",
            "At Risk": "🟡",
            "Off Track": "🔴",
        }
        status_icon = status_emoji.get(report.status, "⚪")

        lines.append(f"# {report.title}")
        lines.append("")
        lines.append(f"**Date:** {report.date.strftime('%B %d, %Y')}")
        lines.append(f"**Author:** {report.author}")
        lines.append(f"**Status:** {status_icon} {report.status}")
        lines.append("")

        # Executive summary
        if report.summary:
            lines.append("## Executive Summary")
            lines.append("")
            lines.append(report.summary)
            lines.append("")

        # Metrics
        if report.metrics:
            lines.append("## Key Metrics")
            lines.append("")
            lines.append("| Metric | Value | Target | Trend |")
            lines.append("|--------|-------|--------|-------|")
            for m in report.metrics:
                trend_icon = {"up": "📈", "down": "📉", "stable": "➡️"}.get(m.trend, "")
                lines.append(
                    f"| {m.name} | {m.value}{m.unit or ''} | "
                    f"{m.target}{m.unit or '' if m.target else ''} | {trend_icon} |"
                )
            lines.append("")

        # Sections
        for section in report.sections:
            lines.extend(self._render_section_markdown(section, level=2))

        # Risks
        if report.risks:
            lines.append("## Risks & Blockers")
            lines.append("")
            for risk in report.risks:
                lines.append(f"- ⚠️ {risk}")
            lines.append("")

        # Action items
        if report.action_items:
            lines.append("## Action Items")
            lines.append("")
            lines.append("| Task | Owner | Due Date | Status |")
            lines.append("|------|--------|----------|--------|")
            for item in report.action_items:
                due = item.due_date.strftime("%Y-%m-%d") if item.due_date else "TBD"
                lines.append(
                    f"| {item.task} | {item.owner or 'TBD'} | {due} | {item.status} |"
                )
            lines.append("")

        # Next steps
        if report.next_steps:
            lines.append("## Next Steps")
            lines.append("")
            for i, step in enumerate(report.next_steps, 1):
                lines.append(f"{i}. {step}")
            lines.append("")

        return "\n".join(lines)

    def _render_section_markdown(
        self,
        section: Section,
        level: int = 2,
    ) -> List[str]:
        """Render a section as Markdown."""
        lines = []
        heading = "#" * level
        lines.append(f"{heading} {section.title}")
        lines.append("")
        if section.content:
            lines.append(section.content)
            lines.append("")

        if section.metrics:
            for m in section.metrics:
                trend = {"up": "📈", "down": "📉", "stable": "➡️"}.get(m.trend, "")
                lines.append(f"- **{m.name}:** {m.value}{m.unit or ''} {trend}")
            lines.append("")

        for subsection in section.subsections:
            lines.extend(self._render_section_markdown(subsection, level + 1))

        return lines

    def render_html(self, report: Report) -> str:
        """
        Render report as HTML.

        Args:
            report: Report to render

        Returns:
            HTML formatted string
        """
        status_colors = {
            "On Track": "#28a745",
            "At Risk": "#ffc107",
            "Off Track": "#dc3545",
        }
        status_color = status_colors.get(report.status, "#6c757d")

        html = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            f"<title>{report.title}</title>",
            "<style>",
            "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px auto; max-width: 800px; }",
            "h1 { color: #1a1a1a; border-bottom: 2px solid #007bff; padding-bottom: 10px; }",
            "h2 { color: #333; margin-top: 30px; }",
            ".status { display: inline-block; padding: 4px 12px; border-radius: 4px; color: white; }",
            ".metadata { color: #666; margin-bottom: 20px; }",
            "table { border-collapse: collapse; width: 100%; margin: 20px 0; }",
            "th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }",
            "th { background-color: #f8f9fa; }",
            ".metric-trend { font-size: 1.2em; }",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{report.title}</h1>",
            f"<div class='metadata'>",
            f"<p><strong>Date:</strong> {report.date.strftime('%B %d, %Y')}</p>",
            f"<p><strong>Author:</strong> {report.author}</p>",
            f"<p><strong>Status:</strong> <span class='status' style='background-color: {status_color}'>{report.status}</span></p>",
            "</div>",
        ]

        # Executive summary
        if report.summary:
            html.extend([
                "<h2>Executive Summary</h2>",
                f"<p>{report.summary}</p>",
            ])

        # Metrics
        if report.metrics:
            html.extend([
                "<h2>Key Metrics</h2>",
                "<table>",
                "<tr><th>Metric</th><th>Value</th><th>Target</th><th>Trend</th></tr>",
            ])
            for m in report.metrics:
                trend_icon = {"up": "📈", "down": "📉", "stable": "➡️"}.get(m.trend, "")
                html.append(
                    f"<tr><td>{m.name}</td><td>{m.value}{m.unit or ''}</td>"
                    f"<td>{m.target}{m.unit or '' if m.target else ''}</td>"
                    f"<td class='metric-trend'>{trend_icon}</td></tr>"
                )
            html.append("</table>")

        # Sections
        for section in report.sections:
            html.extend(self._render_section_html(section))

        # Risks
        if report.risks:
            html.append("<h2>Risks & Blockers</h2><ul>")
            for risk in report.risks:
                html.append(f"<li>⚠️ {risk}</li>")
            html.append("</ul>")

        # Action items
        if report.action_items:
            html.extend([
                "<h2>Action Items</h2>",
                "<table>",
                "<tr><th>Task</th><th>Owner</th><th>Due Date</th><th>Status</th></tr>",
            ])
            for item in report.action_items:
                due = item.due_date.strftime("%Y-%m-%d") if item.due_date else "TBD"
                html.append(
                    f"<tr><td>{item.task}</td><td>{item.owner or 'TBD'}</td>"
                    f"<td>{due}</td><td>{item.status}</td></tr>"
                )
            html.append("</table>")

        # Next steps
        if report.next_steps:
            html.append("<h2>Next Steps</h2><ol>")
            for step in report.next_steps:
                html.append(f"<li>{step}</li>")
            html.append("</ol>")

        html.extend(["</body>", "</html>"])
        return "\n".join(html)

    def _render_section_html(self, section: Section) -> List[str]:
        """Render a section as HTML."""
        html = [
            f"<h2>{section.title}</h2>",
            f"<p>{section.content.replace(chr(10), '</p><p>')}</p>",
        ]

        if section.metrics:
            html.append("<ul>")
            for m in section.metrics:
                trend = {"up": "📈", "down": "📉", "stable": "➡️"}.get(m.trend, "")
                html.append(f"<li><strong>{m.name}:</strong> {m.value}{m.unit or ''} {trend}</li>")
            html.append("</ul>")

        for subsection in section.subsections:
            html.extend(self._render_section_html(subsection))

        return html

    def save_report(
        self,
        report: Report,
        output_path: Path,
        format: ReportFormat = ReportFormat.MARKDOWN,
    ) -> Path:
        """
        Save report to file.

        Args:
            report: Report to save
            output_path: Output file path
            format: Output format

        Returns:
            Path to saved file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        content = ""
        if format == ReportFormat.MARKDOWN:
            content = self.render_markdown(report)
        elif format == ReportFormat.HTML:
            content = self.render_html(report)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return output_path


if __name__ == "__main__":
    # Example: Create a status report
    generator = ReportGenerator()

    report = generator.create_status_report(
        title="Q4 Project Update",
        author="John Smith",
        period="Week of January 15, 2024",
        completed=[
            "Completed API integration",
            "Deployed staging environment",
            "User testing phase 1",
        ],
        in_progress=[
            "Performance optimization",
            "Documentation updates",
        ],
        upcoming=[
            "Production deployment",
            "Security audit",
            "User training",
        ],
        blockers=[
            "Waiting on third-party API credentials",
        ],
        next_steps=[
            "Schedule security audit",
            "Prepare user training materials",
        ],
    )

    print(generator.render_markdown(report))