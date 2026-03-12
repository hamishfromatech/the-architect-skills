---
name: Create Skill
description: This skill should be used when the user asks to "create a new skill", "make a skill", "add a skill", "build a skill", "generate a skill", "create-skill", or mentions skill creation, skill development, extending capabilities, or adding new functionality to The Architect.
version: 1.0.0
---

# Create Skill

Meta-skill for creating new skills to extend The Architect's capabilities.

## Purpose

This skill enables The Architect to evolve itself by creating new skills. When a need is identified for new functionality, this skill guides the creation of properly structured skills that integrate seamlessly with the existing skill system.

## Skill Creation Process

### Step 1: Identify Skill Need

Before creating a skill, confirm:
1. **Is this functionality truly new?** - Check if existing skills already cover it
2. **Is it reusable?** - Will this be used multiple times?
3. **Is it domain-specific?** - Does it warrant a dedicated skill?
4. **Are there clear triggers?** - Can you define when this skill should activate?

### Step 2: Define Skill Metadata

Create the frontmatter with:

```yaml
---
name: Skill Name
description: This skill should be used when the user asks to "specific phrase 1", "specific phrase 2", "specific phrase 3". Include exact phrases users would say that should trigger this skill. Be concrete and specific.
version: 1.0.0
---
```

**Critical Rules for Descriptions:**
- Use third-person format ("This skill should be used when...")
- Include 3-5 specific trigger phrases users would actually say
- Be concrete, not vague
- Avoid generic phrases like "Use this skill when working with X"

### Step 3: Create Directory Structure

```
skills/
└── skill-name/
    ├── SKILL.md           # Main skill file (required)
    ├── scripts/           # Python scripts (optional)
    │   └── module.py
    ├── references/        # Reference documentation (optional)
    │   └── guide.md
    └── examples/          # Example files (optional)
        └── examples.md
```

### Step 4: Write SKILL.md Content

Structure the content with:

```markdown
# Skill Name

Brief one-line description.

## Capabilities

- What this skill can do
- Key functionalities
- Main features

## Process

1. **Step 1**: Description
2. **Step 2**: Description
3. **Step 3**: Description

## Guidelines

- Keep content lean (1,500-2,000 words)
- Use imperative form ("Create the file", not "You should create")
- Reference supporting files for details

## Python Scripts

The `scripts/` directory contains:
- `script_name.py` - Brief description

## Usage Examples

See `examples/` directory for sample use cases.

## References

See `references/` directory for detailed guides.
```

### Step 5: Create Supporting Files

#### Python Scripts (`scripts/`)
- Use pure Python (no external dependencies unless necessary)
- Include docstrings and type hints
- Make scripts importable and testable
- Follow PEP 8 style guidelines

#### References (`references/`)
- Detailed guides and best practices
- Industry standards
- Technical documentation

#### Examples (`examples/`)
- Concrete usage examples
- Sample inputs and outputs
- Common scenarios

## Skill Templates

### Basic Skill Template

```markdown
---
name: [Skill Name]
description: This skill should be used when the user asks to "[trigger 1]", "[trigger 2]", "[trigger 3]", or mentions [related context].
version: 1.0.0
---

# [Skill Name]

[One-line description of what this skill does]

## Capabilities

- [Capability 1]
- [Capability 2]
- [Capability 3]

## Process

1. **[Step 1]**: [Description]
2. **[Step 2]**: [Description]
3. **[Step 3]**: [Description]

## Guidelines

- [Guideline 1]
- [Guideline 2]

## Python Scripts

The `scripts/` directory contains Python utilities for [purpose].

## Usage Examples

See `examples/` directory for sample use cases.

## References

See `references/` directory for detailed guides.
```

### Python Script Template

```python
"""
[Module Name] - [Brief description]

This module provides utilities for [purpose].
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class [EnumName](Enum):
    """[Description]."""
    VALUE1 = "value1"
    VALUE2 = "value2"


@dataclass
class [DataClassName]:
    """[Description]."""
    field1: str
    field2: Optional[str] = None


class [MainClass]:
    """[Description]."""

    def __init__(self, param: str):
        """Initialize with param."""
        self.param = param

    def process(self, input_data: str) -> str:
        """
        Process the input data.

        Args:
            input_data: Input to process

        Returns:
            Processed result
        """
        # Implementation
        return input_data


if __name__ == "__main__":
    # Example usage
    pass
```

## Best Practices

### Writing Descriptions
✅ Good: "This skill should be used when the user asks to 'create a proposal', 'write a proposal', or 'draft a business proposal'."

❌ Bad: "Use this skill when working with proposals."

### Content Organization
- Lead with the most important information
- Use clear section headers
- Reference supporting files instead of duplicating content
- Keep the main SKILL.md concise

### Python Scripts
- Make scripts standalone when possible
- Include example usage in `if __name__ == "__main__"`
- Use type hints for better IDE support
- Handle edge cases gracefully

### Naming Conventions
- Use kebab-case for directories: `skill-name/`
- Use snake_case for Python files: `script_name.py`
- Use PascalCase for classes: `MyClass`
- Use UPPER_CASE for constants: `MAX_ITEMS`

## Validation Checklist

Before finalizing a new skill:

- [ ] SKILL.md has proper frontmatter
- [ ] Description includes specific trigger phrases
- [ ] Name is descriptive and unique
- [ ] Content follows the standard structure
- [ ] Python scripts have docstrings
- [ ] Examples cover common use cases
- [ ] References provide detailed guidance
- [ ] All files use consistent formatting

## Integration

After creating a skill:

1. Test trigger phrases work correctly
2. Verify scripts run without errors
3. Check examples are accurate
4. Ensure references are complete
5. Document any dependencies

## Python Scripts

The `scripts/` directory contains:
- `skill_generator.py` - Generate skill directory structure
- `template_builder.py` - Build skill templates
- `validator.py` - Validate skill structure

## Usage Examples

See `examples/` directory for:
- Complete skill examples
- Various skill types (utility, domain, workflow)
- Before/after improvements

## References

See `references/` directory for:
- Skill system architecture
- Trigger phrase patterns
- Python style guidelines
- Integration testing