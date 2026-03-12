"""
Skill Validator - Validate skill structure and content.

This module provides utilities for validating skill files,
ensuring they follow proper structure and conventions.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum


class Severity(Enum):
    """Validation issue severity."""
    ERROR = "error"      # Must be fixed
    WARNING = "warning"  # Should be fixed
    INFO = "info"        # Suggestion


@dataclass
class ValidationResult:
    """Result of skill validation."""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add an error message."""
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)

    def add_info(self, message: str) -> None:
        """Add an info message."""
        self.info.append(message)

    def merge(self, other: "ValidationResult") -> None:
        """Merge another result into this one."""
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.info.extend(other.info)
        if other.errors:
            self.valid = False


@dataclass
class FileValidation:
    """Validation result for a single file."""
    path: Path
    result: ValidationResult


class SkillValidator:
    """Validate skill structure and content."""

    # Required frontmatter fields
    REQUIRED_FRONTMATTER = ["name", "description", "version"]
    RECOMMENDED_FRONTMATTER = []

    # Required sections in SKILL.md
    RECOMMENDED_SECTIONS = ["Capabilities", "Process", "Guidelines"]

    # Python script requirements
    REQUIRED_PYTHON_ELEMENTS = ["docstring", "class or function"]

    def __init__(self, skill_path: Path):
        """
        Initialize validator.

        Args:
            skill_path: Path to skill directory
        """
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.name

    def validate_all(self) -> ValidationResult:
        """
        Run all validations.

        Returns:
            Combined validation result
        """
        result = ValidationResult(valid=True)

        # Validate structure
        result.merge(self.validate_structure())

        # Validate SKILL.md
        skill_md = self.skill_path / "SKILL.md"
        if skill_md.exists():
            result.merge(self.validate_skill_md(skill_md))

        # Validate Python scripts
        scripts_dir = self.skill_path / "scripts"
        if scripts_dir.exists():
            for py_file in scripts_dir.glob("*.py"):
                result.merge(self.validate_python_script(py_file))

        # Validate references
        references_dir = self.skill_path / "references"
        if references_dir.exists():
            for ref_file in references_dir.glob("*.md"):
                result.merge(self.validate_reference(ref_file))

        # Validate examples
        examples_dir = self.skill_path / "examples"
        if examples_dir.exists():
            for example_file in examples_dir.glob("*.md"):
                result.merge(self.validate_example(example_file))

        return result

    def validate_structure(self) -> ValidationResult:
        """
        Validate directory structure.

        Returns:
            ValidationResult
        """
        result = ValidationResult(valid=True)

        # Check SKILL.md exists
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            result.add_error("Missing SKILL.md file")

        # Check directory name format
        if not re.match(r'^[a-z0-9-]+$', self.skill_name):
            result.add_warning(
                f"Skill directory name '{self.skill_name}' should use lowercase and hyphens"
            )

        # Check for recommended directories
        for subdir in ["scripts", "references", "examples"]:
            dir_path = self.skill_path / subdir
            if not dir_path.exists():
                result.add_info(f"Consider adding a '{subdir}' directory")

        return result

    def validate_skill_md(self, file_path: Path) -> ValidationResult:
        """
        Validate SKILL.md content.

        Args:
            file_path: Path to SKILL.md

        Returns:
            ValidationResult
        """
        result = ValidationResult(valid=True)

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            result.add_error(f"Cannot read file: {e}")
            return result

        # Validate frontmatter
        result.merge(self._validate_frontmatter(content))

        # Validate content sections
        result.merge(self._validate_sections(content))

        # Validate description quality
        result.merge(self._validate_description(content))

        return result

    def _validate_frontmatter(self, content: str) -> ValidationResult:
        """Validate frontmatter."""
        result = ValidationResult(valid=True)

        # Check frontmatter exists
        if not content.startswith("---"):
            result.add_error("SKILL.md must start with frontmatter (---)")
            return result

        # Extract frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            result.add_error("Invalid frontmatter format")
            return result

        frontmatter = frontmatter_match.group(1)

        # Check required fields
        for field in self.REQUIRED_FRONTMATTER:
            if not re.search(rf'^{field}:', frontmatter, re.MULTILINE):
                result.add_error(f"Missing required frontmatter field: {field}")

        # Validate name format
        name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
        if name_match:
            name = name_match.group(1).strip()
            # Remove quotes if present
            name = name.strip('"\'')
            if not name:
                result.add_error("Name field cannot be empty")
            elif len(name) > 100:
                result.add_warning("Name is very long (consider shorter name)")

        # Validate version format
        version_match = re.search(r'^version:\s*(.+)$', frontmatter, re.MULTILINE)
        if version_match:
            version = version_match.group(1).strip().strip('"\'')
            if not re.match(r'^\d+\.\d+\.\d+$', version):
                result.add_warning(f"Version '{version}' should follow semver (x.y.z)")

        return result

    def _validate_sections(self, content: str) -> ValidationResult:
        """Validate content sections."""
        result = ValidationResult(valid=True)

        # Remove frontmatter
        body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # Check for recommended sections
        for section in self.RECOMMENDED_SECTIONS:
            pattern = rf'^##\s+{section}'
            if not re.search(pattern, body, re.MULTILINE | re.IGNORECASE):
                result.add_warning(f"Missing recommended section: {section}")

        # Check content length
        word_count = len(body.split())
        if word_count < 100:
            result.add_warning("SKILL.md content seems too short")
        elif word_count > 5000:
            result.add_warning("SKILL.md is very long; consider splitting content")

        return result

    def _validate_description(self, content: str) -> ValidationResult:
        """Validate description quality."""
        result = ValidationResult(valid=True)

        # Find description in frontmatter
        desc_match = re.search(r'^description:\s*(.+?)(?:\n|$)', content, re.MULTILINE)
        if not desc_match:
            return result

        description = desc_match.group(1).strip()

        # Check for trigger phrases (should have quoted phrases)
        if '"' not in description and "'" not in description:
            result.add_warning(
                "Description should include specific trigger phrases in quotes"
            )

        # Check for third-person format
        if not re.search(r'this skill should be used', description, re.IGNORECASE):
            result.add_info(
                "Description should use third-person format "
                "(e.g., 'This skill should be used when...')"
            )

        # Check description length
        if len(description) < 50:
            result.add_warning("Description is too short; be more specific")
        elif len(description) > 500:
            result.add_warning("Description is too long; keep it concise")

        return result

    def validate_python_script(self, file_path: Path) -> ValidationResult:
        """
        Validate Python script.

        Args:
            file_path: Path to Python file

        Returns:
            ValidationResult
        """
        result = ValidationResult(valid=True)

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            result.add_error(f"Cannot read file: {e}")
            return result

        # Check for module docstring
        if not re.search(r'^"""[\s\S]*?"""', content.strip()):
            result.add_warning(f"{file_path.name} missing module docstring")

        # Check for type hints
        if "def " in content and ":" not in content.split("def ")[1].split("\n")[0]:
            result.add_info(f"{file_path.name} could use type hints")

        # Check for example usage
        if 'if __name__ == "__main__"' not in content:
            result.add_info(f"{file_path.name} could include example usage")

        # Check for common issues
        if "print(" in content and "def " not in content:
            result.add_warning(f"{file_path.name} only contains print statements")

        return result

    def validate_reference(self, file_path: Path) -> ValidationResult:
        """
        Validate reference markdown file.

        Args:
            file_path: Path to reference file

        Returns:
            ValidationResult
        """
        result = ValidationResult(valid=True)

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            result.add_error(f"Cannot read file: {e}")
            return result

        # Check for title
        if not content.strip().startswith("#"):
            result.add_warning(f"{file_path.name} should start with a heading")

        # Check minimum content
        if len(content.split("\n")) < 10:
            result.add_info(f"{file_path.name} seems sparse; add more content")

        return result

    def validate_example(self, file_path: Path) -> ValidationResult:
        """
        Validate example markdown file.

        Args:
            file_path: Path to example file

        Returns:
            ValidationResult
        """
        result = ValidationResult(valid=True)

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            result.add_error(f"Cannot read file: {e}")
            return result

        # Check for code examples
        if "```" not in content:
            result.add_info(f"{file_path.name} could include code examples")

        return result


class SkillRegistryValidator:
    """Validate multiple skills in a registry."""

    def __init__(self, skills_path: Path):
        """
        Initialize registry validator.

        Args:
            skills_path: Path to skills directory
        """
        self.skills_path = Path(skills_path)

    def validate_all_skills(self) -> Dict[str, ValidationResult]:
        """
        Validate all skills in the registry.

        Returns:
            Dictionary of skill name to validation result
        """
        results = {}

        for skill_dir in self.skills_path.iterdir():
            if skill_dir.is_dir():
                validator = SkillValidator(skill_dir)
                results[skill_dir.name] = validator.validate_all()

        return results

    def get_summary(self) -> Dict:
        """
        Get validation summary.

        Returns:
            Summary dictionary
        """
        results = self.validate_all_skills()

        summary = {
            "total_skills": len(results),
            "valid_skills": sum(1 for r in results.values() if r.valid),
            "invalid_skills": sum(1 for r in results.values() if not r.valid),
            "total_errors": sum(len(r.errors) for r in results.values()),
            "total_warnings": sum(len(r.warnings) for r in results.values()),
        }

        return summary


def print_validation_report(results: Dict[str, ValidationResult]) -> None:
    """
    Print a validation report.

    Args:
        results: Dictionary of skill name to validation result
    """
    print("\n" + "=" * 60)
    print("SKILL VALIDATION REPORT")
    print("=" * 60)

    for skill_name, result in results.items():
        status = "✓ VALID" if result.valid else "✗ INVALID"
        print(f"\n{skill_name}: {status}")

        if result.errors:
            print("  Errors:")
            for error in result.errors:
                print(f"    - {error}")

        if result.warnings:
            print("  Warnings:")
            for warning in result.warnings:
                print(f"    - {warning}")

        if result.info:
            print("  Info:")
            for info in result.info:
                print(f"    - {info}")

    # Summary
    valid_count = sum(1 for r in results.values() if r.valid)
    print("\n" + "=" * 60)
    print(f"SUMMARY: {valid_count}/{len(results)} skills valid")
    print("=" * 60)


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        skill_path = Path(sys.argv[1])
        validator = SkillValidator(skill_path)
        result = validator.validate_all()
        print_validation_report({skill_path.name: result})
    else:
        # Validate all skills in current directory
        current_path = Path(".")
        registry_validator = SkillRegistryValidator(current_path)
        results = registry_validator.validate_all_skills()
        print_validation_report(results)