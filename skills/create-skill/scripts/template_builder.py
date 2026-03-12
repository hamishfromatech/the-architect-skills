"""
Template Builder - Build skill templates from configurations.

This module provides utilities for generating skill templates
with customizable content.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Callable
from enum import Enum
import json


class TemplateType(Enum):
    """Types of templates."""
    BASIC = "basic"
    PYTHON_HEAVY = "python_heavy"
    DOCUMENTATION = "documentation"
    WORKFLOW = "workflow"
    MINIMAL = "minimal"


@dataclass
class SkillTemplate:
    """A skill template with customizable sections."""
    name: str
    description_template: str
    capabilities: List[str] = field(default_factory=list)
    process_steps: List[str] = field(default_factory=list)
    guidelines: List[str] = field(default_factory=list)
    has_scripts: bool = True
    has_references: bool = True
    has_examples: bool = True
    custom_sections: Dict[str, str] = field(default_factory=dict)


# Predefined templates for common skill types
TEMPLATE_LIBRARY: Dict[str, SkillTemplate] = {
    "utility": SkillTemplate(
        name="Utility Skill",
        description_template='This skill should be used when the user asks to "{triggers}", or needs {purpose} functionality.',
        capabilities=[
            "Perform utility operation",
            "Process input data",
            "Generate output",
        ],
        process_steps=[
            "Receive input",
            "Process data",
            "Return result",
        ],
        guidelines=[
            "Validate all inputs",
            "Handle errors gracefully",
            "Provide clear output",
        ],
        has_scripts=True,
        has_references=True,
        has_examples=True,
    ),
    "content": SkillTemplate(
        name="Content Generation Skill",
        description_template='This skill should be used when the user asks to "{triggers}", "generate {content_type}", or mentions {content_type} creation.',
        capabilities=[
            "Generate content",
            "Format output",
            "Apply templates",
        ],
        process_steps=[
            "Gather requirements",
            "Generate content",
            "Review and format",
        ],
        guidelines=[
            "Follow style guidelines",
            "Ensure consistency",
            "Validate output quality",
        ],
        has_scripts=True,
        has_references=True,
        has_examples=True,
    ),
    "workflow": SkillTemplate(
        name="Workflow Skill",
        description_template='This skill should be used when the user asks to "{triggers}", or needs to execute {workflow_name} workflow.',
        capabilities=[
            "Execute workflow steps",
            "Track progress",
            "Handle transitions",
        ],
        process_steps=[
            "Initialize workflow",
            "Execute steps in order",
            "Validate completion",
        ],
        guidelines=[
            "Track state carefully",
            "Handle failures gracefully",
            "Log all transitions",
        ],
        has_scripts=True,
        has_references=True,
        has_examples=True,
    ),
    "analysis": SkillTemplate(
        name="Analysis Skill",
        description_template='This skill should be used when the user asks to "{triggers}", "analyze {subject}", or mentions {subject} analysis.',
        capabilities=[
            "Analyze input data",
            "Extract insights",
            "Generate reports",
        ],
        process_steps=[
            "Collect data",
            "Perform analysis",
            "Present findings",
        ],
        guidelines=[
            "Use appropriate methods",
            "Document assumptions",
            "Validate results",
        ],
        has_scripts=True,
        has_references=True,
        has_examples=True,
    ),
    "communication": SkillTemplate(
        name="Communication Skill",
        description_template='This skill should be used when the user asks to "{triggers}", or mentions {communication_type} composition or formatting.',
        capabilities=[
            "Compose communications",
            "Format messages",
            "Apply appropriate tone",
        ],
        process_steps=[
            "Understand context",
            "Draft content",
            "Review and refine",
        ],
        guidelines=[
            "Match tone to audience",
            "Be clear and concise",
            "Include call to action",
        ],
        has_scripts=True,
        has_references=True,
        has_examples=True,
    ),
}


class TemplateBuilder:
    """Build skill templates with customization."""

    def __init__(self):
        """Initialize the template builder."""
        self.templates = TEMPLATE_LIBRARY.copy()

    def get_template(self, template_type: str) -> Optional[SkillTemplate]:
        """
        Get a template by type.

        Args:
            template_type: Type of template to get

        Returns:
            SkillTemplate if found, None otherwise
        """
        return self.templates.get(template_type)

    def list_templates(self) -> List[str]:
        """
        List available template types.

        Returns:
            List of template type names
        """
        return list(self.templates.keys())

    def customize_template(
        self,
        template_type: str,
        name: str,
        trigger_phrases: List[str],
        **customizations,
    ) -> SkillTemplate:
        """
        Customize a template for a specific skill.

        Args:
            template_type: Base template type
            name: Name for the new skill
            trigger_phrases: List of trigger phrases
            **customizations: Additional customizations

        Returns:
            Customized SkillTemplate
        """
        base = self.templates.get(template_type)
        if not base:
            base = self.templates["utility"]

        # Build trigger phrase string
        triggers_str = ", ".join(f'"{t}"' for t in trigger_phrases[:-1])
        if len(trigger_phrases) > 1:
            triggers_str += f', or "{trigger_phrases[-1]}"'
        elif trigger_phrases:
            triggers_str = f'"{trigger_phrases[0]}"'

        # Build description
        description = base.description_template.format(
            triggers=triggers_str,
            purpose=name.lower(),
            content_type=customizations.get("content_type", "content"),
            workflow_name=customizations.get("workflow_name", "the"),
            subject=customizations.get("subject", "data"),
            communication_type=customizations.get("communication_type", "message"),
        )

        # Create customized template
        return SkillTemplate(
            name=name,
            description_template=description,
            capabilities=customizations.get("capabilities", base.capabilities.copy()),
            process_steps=customizations.get("process_steps", base.process_steps.copy()),
            guidelines=customizations.get("guidelines", base.guidelines.copy()),
            has_scripts=customizations.get("has_scripts", base.has_scripts),
            has_references=customizations.get("has_references", base.has_references),
            has_examples=customizations.get("has_examples", base.has_examples),
            custom_sections=customizations.get("custom_sections", {}),
        )

    def build_skill_md(
        self,
        name: str,
        description: str,
        capabilities: List[str],
        process_steps: List[str],
        guidelines: List[str],
        custom_sections: Dict[str, str] = None,
        version: str = "1.0.0",
    ) -> str:
        """
        Build complete SKILL.md content.

        Args:
            name: Skill name
            description: Skill description
            capabilities: List of capabilities
            process_steps: List of process steps
            guidelines: List of guidelines
            custom_sections: Additional sections
            version: Skill version

        Returns:
            Complete SKILL.md content
        """
        sections = []

        # Frontmatter
        sections.append("---")
        sections.append(f'name: {name}')
        sections.append(f'description: {description}')
        sections.append(f'version: {version}')
        sections.append("---")
        sections.append("")

        # Title
        sections.append(f"# {name}")
        sections.append("")

        # Capabilities
        sections.append("## Capabilities")
        sections.append("")
        for cap in capabilities:
            sections.append(f"- {cap}")
        sections.append("")

        # Process
        sections.append("## Process")
        sections.append("")
        for i, step in enumerate(process_steps, 1):
            sections.append(f"{i}. **{step}**")
        sections.append("")

        # Guidelines
        sections.append("## Guidelines")
        sections.append("")
        for guide in guidelines:
            sections.append(f"- {guide}")
        sections.append("")

        # Custom sections
        if custom_sections:
            for title, content in custom_sections.items():
                sections.append(f"## {title}")
                sections.append("")
                sections.append(content)
                sections.append("")

        # Standard footer sections
        sections.append("## Python Scripts")
        sections.append("")
        sections.append("The `scripts/` directory contains Python utilities for this skill.")
        sections.append("")

        sections.append("## Usage Examples")
        sections.append("")
        sections.append("See `examples/` directory for sample use cases.")
        sections.append("")

        sections.append("## References")
        sections.append("")
        sections.append("See `references/` directory for detailed guides.")
        sections.append("")

        return "\n".join(sections)

    def register_template(
        self,
        template_type: str,
        template: SkillTemplate,
    ) -> None:
        """
        Register a new template type.

        Args:
            template_type: Type name for the template
            template: SkillTemplate to register
        """
        self.templates[template_type] = template

    def export_template(self, template: SkillTemplate) -> str:
        """
        Export a template to JSON for storage.

        Args:
            template: SkillTemplate to export

        Returns:
            JSON string
        """
        return json.dumps({
            "name": template.name,
            "description_template": template.description_template,
            "capabilities": template.capabilities,
            "process_steps": template.process_steps,
            "guidelines": template.guidelines,
            "has_scripts": template.has_scripts,
            "has_references": template.has_references,
            "has_examples": template.has_examples,
            "custom_sections": template.custom_sections,
        }, indent=2)

    def import_template(self, json_str: str) -> SkillTemplate:
        """
        Import a template from JSON.

        Args:
            json_str: JSON string

        Returns:
            SkillTemplate
        """
        data = json.loads(json_str)
        return SkillTemplate(
            name=data["name"],
            description_template=data["description_template"],
            capabilities=data["capabilities"],
            process_steps=data["process_steps"],
            guidelines=data["guidelines"],
            has_scripts=data["has_scripts"],
            has_references=data["has_references"],
            has_examples=data["has_examples"],
            custom_sections=data.get("custom_sections", {}),
        )


class SkillBuilder:
    """High-level skill building from templates."""

    def __init__(self, output_path: Path):
        """
        Initialize skill builder.

        Args:
            output_path: Base path for skill output
        """
        self.output_path = output_path
        self.template_builder = TemplateBuilder()

    def build_from_template(
        self,
        skill_name: str,
        template_type: str,
        trigger_phrases: List[str],
        **customizations,
    ) -> Path:
        """
        Build a complete skill from a template.

        Args:
            skill_name: Name for the skill
            template_type: Type of template to use
            trigger_phrases: List of trigger phrases
            **customizations: Additional customizations

        Returns:
            Path to created skill
        """
        # Customize template
        template = self.template_builder.customize_template(
            template_type,
            skill_name,
            trigger_phrases,
            **customizations,
        )

        # Build SKILL.md content
        skill_md = self.template_builder.build_skill_md(
            name=skill_name,
            description=template.description_template,
            capabilities=template.capabilities,
            process_steps=template.process_steps,
            guidelines=template.guidelines,
            custom_sections=template.custom_sections,
        )

        # Create skill directory
        skill_path = self.output_path / skill_name.lower().replace(" ", "-")
        skill_path.mkdir(parents=True, exist_ok=True)

        # Write SKILL.md
        (skill_path / "SKILL.md").write_text(skill_md, encoding="utf-8")

        # Create subdirectories
        if template.has_scripts:
            (skill_path / "scripts").mkdir(exist_ok=True)
        if template.has_references:
            (skill_path / "references").mkdir(exist_ok=True)
        if template.has_examples:
            (skill_path / "examples").mkdir(exist_ok=True)

        return skill_path


if __name__ == "__main__":
    # Example usage
    builder = TemplateBuilder()

    print("Available templates:", builder.list_templates())

    # Customize a template
    template = builder.customize_template(
        "content",
        name="Blog Writer",
        trigger_phrases=[
            "write a blog post",
            "create blog content",
            "blog article",
        ],
        content_type="blog post",
        capabilities=[
            "Generate blog post content",
            "Apply SEO optimization",
            "Format for publishing",
        ],
    )

    print(f"\nTemplate name: {template.name}")
    print(f"Description: {template.description_template}")
    print(f"Capabilities: {template.capabilities}")