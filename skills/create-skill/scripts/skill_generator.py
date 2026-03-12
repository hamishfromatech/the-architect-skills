"""
Skill Generator - Generate skill directory structure and files.

This module provides utilities for creating new skills with proper
structure, templates, and validation.
"""

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum


class SkillType(Enum):
    """Types of skills that can be created."""
    UTILITY = "utility"      # General utility functions
    DOMAIN = "domain"        # Domain-specific functionality
    WORKFLOW = "workflow"   # Process/workflow automation
    CONTENT = "content"     # Content generation
    ANALYSIS = "analysis"   # Analysis and insights
    COMMUNICATION = "communication"  # Email, messaging, etc.


@dataclass
class SkillConfig:
    """Configuration for a new skill."""
    name: str
    description: str
    trigger_phrases: List[str]
    skill_type: SkillType = SkillType.UTILITY
    needs_scripts: bool = True
    needs_references: bool = True
    needs_examples: bool = True
    version: str = "1.0.0"


@dataclass
class GeneratedSkill:
    """Result of skill generation."""
    path: Path
    files_created: List[str]
    directories_created: List[str]


class SkillGenerator:
    """Generate new skills for The Architect."""

    # Directory structure template
    DIRECTORIES = ["scripts", "references", "examples"]

    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize the skill generator.

        Args:
            base_path: Base path for skills directory
        """
        self.base_path = base_path or Path("skills")

    def create_skill(self, config: SkillConfig) -> GeneratedSkill:
        """
        Create a new skill with complete structure.

        Args:
            config: Skill configuration

        Returns:
            GeneratedSkill with created paths
        """
        # Normalize skill name to kebab-case
        skill_name = self._normalize_name(config.name)
        skill_path = self.base_path / skill_name

        files_created = []
        directories_created = []

        # Create directories
        directories_created.append(str(skill_path))
        skill_path.mkdir(parents=True, exist_ok=True)

        for subdir in self.DIRECTORIES:
            dir_path = skill_path / subdir
            dir_path.mkdir(exist_ok=True)
            directories_created.append(str(dir_path))

        # Create SKILL.md
        skill_md_content = self._generate_skill_md(config)
        skill_md_path = skill_path / "SKILL.md"
        skill_md_path.write_text(skill_md_content, encoding="utf-8")
        files_created.append(str(skill_md_path))

        # Create Python script if needed
        if config.needs_scripts:
            script_content = self._generate_python_script(config)
            script_path = skill_path / "scripts" / f"{skill_name.replace('-', '_')}.py"
            script_path.write_text(script_content, encoding="utf-8")
            files_created.append(str(script_path))

        # Create references if needed
        if config.needs_references:
            ref_content = self._generate_reference(config)
            ref_path = skill_path / "references" / f"{skill_name.replace('-', '_')}_guide.md"
            ref_path.write_text(ref_content, encoding="utf-8")
            files_created.append(str(ref_path))

        # Create examples if needed
        if config.needs_examples:
            example_content = self._generate_example(config)
            example_path = skill_path / "examples" / f"{skill_name.replace('-', '_')}_examples.md"
            example_path.write_text(example_content, encoding="utf-8")
            files_created.append(str(example_path))

        return GeneratedSkill(
            path=skill_path,
            files_created=files_created,
            directories_created=directories_created,
        )

    def _normalize_name(self, name: str) -> str:
        """
        Normalize skill name to kebab-case.

        Args:
            name: Raw skill name

        Returns:
            Normalized kebab-case name
        """
        # Replace spaces and underscores with hyphens
        name = name.replace(" ", "-").replace("_", "-")
        # Remove special characters
        name = "".join(c for c in name if c.isalnum() or c == "-")
        # Lowercase
        name = name.lower()
        # Remove consecutive hyphens
        while "--" in name:
            name = name.replace("--", "-")
        # Remove leading/trailing hyphens
        name = name.strip("-")
        return name

    def _generate_skill_md(self, config: SkillConfig) -> str:
        """
        Generate SKILL.md content.

        Args:
            config: Skill configuration

        Returns:
            SKILL.md content
        """
        # Build trigger phrases
        trigger_str = ", ".join(f'"{phrase}"' for phrase in config.trigger_phrases)

        # Generate description
        description = f'This skill should be used when the user asks to {trigger_str}, or mentions {config.name.lower()} related tasks.'

        content = f'''---
name: {config.name.title().replace("-", " ")}
description: {description}
version: {config.version}
---

# {config.name.title().replace("-", " ")}

[One-line description of what this skill does]

## Capabilities

- [Capability 1]
- [Capability 2]
- [Capability 3]

## Process

1. **Step 1**: [Description]
2. **Step 2**: [Description]
3. **Step 3**: [Description]

## Guidelines

- [Guideline 1]
- [Guideline 2]
- [Guideline 3]

## Python Scripts

The `scripts/` directory contains Python utilities for [purpose].

## Usage Examples

See `examples/` directory for sample use cases.

## References

See `references/` directory for detailed guides.
'''
        return content

    def _generate_python_script(self, config: SkillConfig) -> str:
        """
        Generate Python script content.

        Args:
            config: Skill configuration

        Returns:
            Python script content
        """
        module_name = config.name.replace("-", "_")
        class_name = "".join(word.title() for word in config.name.split("-"))

        content = f'''"""
{config.name.title().replace("-", " ")} - [Brief description]

This module provides utilities for [purpose].
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum


class {class_name}Type(Enum):
    """Types for {config.name}."""
    TYPE1 = "type1"
    TYPE2 = "type2"


@dataclass
class {class_name}Config:
    """Configuration for {config.name}."""
    name: str
    value: Optional[str] = None


class {class_name}:
    """Main class for {config.name} functionality."""

    def __init__(self):
        """Initialize the {config.name}."""
        pass

    def process(self, input_data: str) -> Dict[str, Any]:
        """
        Process the input data.

        Args:
            input_data: Input to process

        Returns:
            Processed result
        """
        # TODO: Implement processing logic
        return {{
            "status": "success",
            "input": input_data,
            "output": None,
        }}

    def validate(self, data: Any) -> bool:
        """
        Validate input data.

        Args:
            data: Data to validate

        Returns:
            True if valid, False otherwise
        """
        # TODO: Implement validation logic
        return data is not None


if __name__ == "__main__":
    # Example usage
    {module_name} = {class_name}()
    result = {module_name}.process("example input")
    print(result)
'''
        return content

    def _generate_reference(self, config: SkillConfig) -> str:
        """
        Generate reference documentation content.

        Args:
            config: Skill configuration

        Returns:
            Reference markdown content
        """
        content = f'''# {config.name.title().replace("-", " ")} Reference Guide

## Overview

This guide provides detailed information about {config.name}.

## Key Concepts

### Concept 1
[Description of concept]

### Concept 2
[Description of concept]

## Best Practices

1. **Practice 1**: [Description]
2. **Practice 2**: [Description]
3. **Practice 3**: [Description]

## Common Patterns

### Pattern 1
[Description and example]

### Pattern 2
[Description and example]

## Troubleshooting

### Issue 1
**Problem**: [Description]
**Solution**: [How to fix]

### Issue 2
**Problem**: [Description]
**Solution**: [How to fix]

## Related Resources

- [Resource 1]
- [Resource 2]
- [Resource 3]
'''
        return content

    def _generate_example(self, config: SkillConfig) -> str:
        """
        Generate example content.

        Args:
            config: Skill configuration

        Returns:
            Example markdown content
        """
        content = f'''# {config.name.title().replace("-", " ")} Examples

## Example 1: Basic Usage

```python
from scripts.{config.name.replace("-", "_")} import {"".join(w.title() for w in config.name.split("-"))}

# Create instance
instance = {"".join(w.title() for w in config.name.split("-"))}()

# Process data
result = instance.process("input data")
print(result)
```

## Example 2: Advanced Usage

```python
# TODO: Add advanced example
pass
```

## Example 3: Integration

```python
# TODO: Add integration example
pass
```

## Common Use Cases

### Use Case 1
[Description and example]

### Use Case 2
[Description and example]

### Use Case 3
[Description and example]

## Tips

- Tip 1: [Description]
- Tip 2: [Description]
- Tip 3: [Description]
'''
        return content

    def list_existing_skills(self) -> List[str]:
        """
        List all existing skills.

        Returns:
            List of skill names
        """
        skills = []
        if self.base_path.exists():
            for item in self.base_path.iterdir():
                if item.is_dir() and (item / "SKILL.md").exists():
                    skills.append(item.name)
        return sorted(skills)

    def skill_exists(self, name: str) -> bool:
        """
        Check if a skill already exists.

        Args:
            name: Skill name to check

        Returns:
            True if skill exists
        """
        skill_name = self._normalize_name(name)
        skill_path = self.base_path / skill_name
        return (skill_path / "SKILL.md").exists()


class SkillValidator:
    """Validate skill structure and content."""

    REQUIRED_FILES = ["SKILL.md"]
    REQUIRED_DIRS = []

    def __init__(self, skill_path: Path):
        """
        Initialize validator.

        Args:
            skill_path: Path to skill directory
        """
        self.skill_path = skill_path

    def validate(self) -> Dict[str, any]:
        """
        Validate the skill.

        Returns:
            Dictionary with validation results
        """
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        # Check required files
        for file_name in self.REQUIRED_FILES:
            file_path = self.skill_path / file_name
            if not file_path.exists():
                results["errors"].append(f"Missing required file: {file_name}")
                results["valid"] = False

        # Check SKILL.md content
        skill_md = self.skill_path / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text(encoding="utf-8")

            # Check frontmatter
            if not content.startswith("---"):
                results["errors"].append("SKILL.md missing frontmatter")
                results["valid"] = False
            else:
                # Check required frontmatter fields
                if "name:" not in content[:500]:
                    results["warnings"].append("SKILL.md frontmatter should include 'name'")
                if "description:" not in content[:500]:
                    results["warnings"].append("SKILL.md frontmatter should include 'description'")
                if "version:" not in content[:500]:
                    results["warnings"].append("SKILL.md frontmatter should include 'version'")

            # Check description has trigger phrases
            if '"This skill should be used when' not in content:
                results["warnings"].append(
                    "Description should include specific trigger phrases in third-person format"
                )

        # Check for Python scripts
        scripts_dir = self.skill_path / "scripts"
        if scripts_dir.exists():
            py_files = list(scripts_dir.glob("*.py"))
            for py_file in py_files:
                file_content = py_file.read_text(encoding="utf-8")
                if '"""' not in file_content:
                    results["warnings"].append(f"{py_file.name} missing docstring")

        return results


if __name__ == "__main__":
    # Example usage
    generator = SkillGenerator()

    # Check existing skills
    print("Existing skills:", generator.list_existing_skills())

    # Create a new skill
    config = SkillConfig(
        name="example-skill",
        description="An example skill for demonstration",
        trigger_phrases=[
            "do example",
            "run example",
            "example task",
        ],
        skill_type=SkillType.UTILITY,
    )

    result = generator.create_skill(config)
    print(f"Created skill at: {result.path}")
    print(f"Files created: {result.files_created}")

    # Validate
    validator = SkillValidator(result.path)
    validation = validator.validate()
    print(f"Validation: {validation}")