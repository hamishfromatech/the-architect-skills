# Create Skill

Meta-skill for creating new skills to extend The Architect's capabilities.

## Overview

The Create Skill skill enables The Architect to evolve itself by creating new skills. It provides templates, validation, and structure for skill development.

## Quick Start

### Trigger Phrases

Use these phrases to activate the skill:
- "create a new skill"
- "make a skill"
- "add a skill"
- "build a skill"
- "generate a skill"
- "create-skill"

## Capabilities

- Generate skill directory structure
- Build from predefined templates
- Validate skill structure and content
- Support self-evolution of The Architect

## Skill Creation Process

1. **Identify Skill Need** - Confirm the functionality is truly new
2. **Define Metadata** - Create frontmatter with name, description, version
3. **Create Directory Structure** - Set up required folders
4. **Write SKILL.md** - Document capabilities, process, and guidelines
5. **Create Supporting Files** - Add scripts, examples, references

## Directory Structure

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

## SKILL.md Template

```markdown
---
name: [Skill Name]
description: This skill should be used when the user asks to "[trigger 1]", "[trigger 2]", "[trigger 3]".
version: 1.0.0
---

# [Skill Name]

[One-line description]

## Capabilities

- [Capability 1]
- [Capability 2]

## Process

1. **[Step 1]**: [Description]
2. **[Step 2]**: [Description]

## Guidelines

- [Guideline 1]
- [Guideline 2]
```

## Validation Checklist

Before finalizing a new skill:
- [ ] SKILL.md has proper frontmatter
- [ ] Description includes specific trigger phrases
- [ ] Capabilities section present
- [ ] Process steps documented
- [ ] Python scripts have docstrings
- [ ] Examples are runnable
- [ ] References are complete

## Examples

See [examples/skill_creation_examples.md](examples/skill_creation_examples.md) for complete skill examples.

## Python Scripts

- `skill_generator.py` - Generate skill directory structure
- `template_builder.py` - Build from predefined templates
- `validator.py` - Validate skill structure and content

## References

See [references/skill_development_guide.md](references/skill_development_guide.md) for detailed guidelines.

## License

MIT License - Part of The Architect Skills project.