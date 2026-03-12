# Skill Development Guide

## Overview

This guide explains how to develop new skills for The Architect. Skills extend The Architect's capabilities by providing specialized knowledge and tools for specific tasks.

## Skill Architecture

### Directory Structure

```
skills/
└── skill-name/
    ├── SKILL.md           # Main skill definition (required)
    ├── scripts/           # Python scripts (optional)
    │   ├── main.py
    │   └── utils.py
    ├── references/        # Reference documentation (optional)
    │   └── guide.md
    └── examples/          # Example files (optional)
        └── examples.md
```

### SKILL.md Structure

```markdown
---
name: Skill Name
description: This skill should be used when the user asks to "trigger 1", "trigger 2", "trigger 3", or mentions related context.
version: 1.0.0
---

# Skill Name

Brief description of the skill.

## Capabilities
- What this skill can do
- Key functionalities

## Process
1. Step 1
2. Step 2
3. Step 3

## Guidelines
- Guideline 1
- Guideline 2

## Python Scripts
Description of scripts in scripts/

## Usage Examples
See examples/ directory.

## References
See references/ directory.
```

---

## Creating a New Skill

### Step-by-Step Process

1. **Identify the Need**
   - What problem does this skill solve?
   - When should it be triggered?
   - What outputs does it produce?

2. **Choose a Name**
   - Use kebab-case: `my-skill-name`
   - Be descriptive but concise
   - Avoid special characters

3. **Create the Directory**
   ```bash
   mkdir -p skills/my-skill-name/{scripts,references,examples}
   ```

4. **Write SKILL.md**
   - Define frontmatter with triggers
   - Describe capabilities
   - Document process steps

5. **Create Python Scripts** (if needed)
   - Pure Python, minimal dependencies
   - Include docstrings
   - Add example usage

6. **Add References**
   - Detailed guides
   - Best practices
   - Technical documentation

7. **Create Examples**
   - Sample use cases
   - Common scenarios
   - Code examples

8. **Validate**
   - Run validation script
   - Test trigger phrases
   - Verify functionality

---

## Frontmatter Guidelines

### Name Field
- Use title case
- Be descriptive
- Keep it under 50 characters

```yaml
name: Email Composer
name: Task Prioritizer
name: Create Skill
```

### Description Field

**✅ Good Descriptions:**
```yaml
description: This skill should be used when the user asks to "write an email", "compose an email", "draft an email", or mentions email composition.
description: This skill should be used when the user asks to "prioritize tasks", "organize my work", "rank priorities", or mentions task management.
```

**❌ Bad Descriptions:**
```yaml
description: Use this skill for emails.
description: Helps with task prioritization.
description: Skill for creating things.
```

### Version Field
- Follow semantic versioning: MAJOR.MINOR.PATCH
- Start at 1.0.0 for new skills
- Increment appropriately for updates

---

## Content Guidelines

### Capabilities Section
List what the skill can do:
```markdown
## Capabilities

- Compose professional emails
- Apply appropriate tone
- Generate email templates
- Validate email structure
```

### Process Section
Document the workflow:
```markdown
## Process

1. **Understand Context**: Identify purpose and audience
2. **Generate Content**: Create email content
3. **Apply Tone**: Adjust formality level
4. **Review**: Validate structure and content
```

### Guidelines Section
Provide best practices:
```markdown
## Guidelines

- Keep emails concise (under 200 words when possible)
- Use appropriate salutations for the audience
- Include clear call-to-action
- Proofread before sending
```

---

## Python Script Guidelines

### Structure
```python
"""
Module Name - Brief description.

This module provides utilities for [purpose].
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class MyEnum(Enum):
    """Description."""
    VALUE1 = "value1"


@dataclass
class MyDataClass:
    """Description."""
    field1: str
    field2: Optional[str] = None


class MainClass:
    """Main class description."""

    def __init__(self, param: str):
        """Initialize with param."""
        self.param = param

    def process(self, input_data: str) -> dict:
        """
        Process the input data.

        Args:
            input_data: Input to process

        Returns:
            Dictionary with results
        """
        # Implementation
        return {"status": "success"}


if __name__ == "__main__":
    # Example usage
    instance = MainClass("example")
    result = instance.process("test input")
    print(result)
```

### Best Practices

1. **Use Type Hints**
   ```python
   def process(self, data: str) -> List[str]:
       return data.split(",")
   ```

2. **Include Docstrings**
   ```python
   def calculate(self, value: int) -> int:
       """
       Calculate the result.

       Args:
           value: Input value

       Returns:
           Calculated result
       """
       return value * 2
   ```

3. **Handle Errors Gracefully**
   ```python
   def process(self, data: str) -> dict:
       try:
           result = self._internal_process(data)
           return {"status": "success", "result": result}
       except ValueError as e:
           return {"status": "error", "message": str(e)}
   ```

4. **Keep It Simple**
   - Prefer pure Python
   - Minimize external dependencies
   - Make scripts testable

---

## Validation Checklist

### SKILL.md
- [ ] Has frontmatter with ---
- [ ] Contains name field
- [ ] Contains description with trigger phrases
- [ ] Contains version field
- [ ] Has capabilities section
- [ ] Has process section
- [ ] Has guidelines section
- [ ] Content is 1,500-2,000 words
- [ ] Uses imperative voice

### Scripts
- [ ] Has module docstring
- [ ] Uses type hints
- [ ] Has example usage
- [ ] Handles errors
- [ ] Follows PEP 8

### References
- [ ] Starts with heading
- [ ] Has sufficient content
- [ ] Provides value

### Examples
- [ ] Includes code examples
- [ ] Covers common scenarios
- [ ] Is clear and runnable

---

## Testing Your Skill

### Manual Testing

1. **Test Trigger Phrases**
   ```
   "write an email"          # Should trigger email-composer
   "prioritize my tasks"     # Should trigger task-prioritizer
   "create a new skill"      # Should trigger create-skill
   ```

2. **Verify Output**
   - Check generated content quality
   - Ensure Python scripts run
   - Validate references are helpful

### Automated Testing

```python
# test_skill.py
from pathlib import Path
from skills.create_skill.scripts.validator import SkillValidator

def test_skill():
    validator = SkillValidator(Path("skills/my-skill"))
    result = validator.validate_all()

    assert result.valid, f"Validation failed: {result.errors}"
    print("Skill validation passed!")
```

---

## Common Issues

### Issue: Skill not triggering
**Cause:** Description doesn't have proper trigger phrases
**Fix:** Add specific phrases in third-person format

### Issue: Scripts don't run
**Cause:** Missing dependencies or syntax errors
**Fix:** Test scripts independently, add requirements

### Issue: Content too long
**Cause:** Too much detail in main file
**Fix:** Move details to references/

### Issue: Missing frontmatter
**Cause:** Forgot to add YAML header
**Fix:** Always start SKILL.md with --- and metadata