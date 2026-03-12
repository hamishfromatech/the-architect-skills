# The Architect

A modular skill-based system for business productivity and automation.

**Maintained and managed by [The A-Tech Corporation PTY LTD](https://theatechcorporation.com)**

## Overview

The Architect is a collection of specialized skills designed to assist with everyday business tasks. Each skill is self-contained with its own documentation, Python scripts, and examples.

## Skills

### Core Business Skills

| Skill | Purpose | Key Features |
|-------|---------|--------------|
| [Email Composer](skills/email-composer/SKILL.md) | Professional email composition | Tone analysis, templates, formatting |
| [Document Generator](skills/document-generator/SKILL.md) | Business document creation | Proposals, contracts, memos, letters |
| [Meeting Summarizer](skills/meeting-summarizer/SKILL.md) | Meeting notes processing | Action item extraction, formatting |
| [Task Prioritizer](skills/task-prioritizer/SKILL.md) | Task organization | Eisenhower matrix, MoSCoW, weighted scoring |
| [Report Writer](skills/report-writer/SKILL.md) | Business report generation | Status reports, progress reports, executive summaries |

### Meta Skill

| Skill | Purpose | Key Features |
|-------|---------|--------------|
| [Create Skill](skills/create-skill/SKILL.md) | Self-evolution capability | Generate, validate, and template new skills |

## Quick Start

### Skill Structure

Each skill follows a consistent structure:

```
skills/
└── skill-name/
    ├── SKILL.md           # Skill definition and triggers
    ├── scripts/           # Python utilities
    │   └── module.py
    ├── references/        # Documentation and guides
    │   └── guide.md
    └── examples/          # Usage examples
        └── examples.md
```

### Using Skills

Skills are triggered by specific phrases. For example:

- **Email Composer**: "write an email", "compose an email", "draft an email"
- **Document Generator**: "create a proposal", "write a contract", "generate a memo"
- **Meeting Summarizer**: "summarize the meeting", "create meeting notes", "extract action items"
- **Task Prioritizer**: "prioritize my tasks", "organize my work", "rank priorities"
- **Report Writer**: "write a report", "create a status report", "generate an executive summary"

### Creating New Skills

Use the `create-skill` skill to extend The Architect:

```python
from skills.create_skill.scripts.skill_generator import SkillGenerator, SkillConfig, SkillType

generator = SkillGenerator()

config = SkillConfig(
    name="my-new-skill",
    description="Description of what this skill does",
    trigger_phrases=[
        "trigger phrase 1",
        "trigger phrase 2",
        "trigger phrase 3",
    ],
    skill_type=SkillType.UTILITY,
)

result = generator.create_skill(config)
print(f"Created: {result.path}")
```

## Skill Details

### Email Composer

Composes professional emails with appropriate tone and structure.

**Capabilities:**
- Formal, semi-formal, and casual tone support
- Email template management
- Structure validation
- Tone analysis

**Python Modules:**
- `email_formatter.py` - Format and validate email structure
- `template_manager.py` - Manage email templates
- `tone_analyzer.py` - Analyze email tone

---

### Document Generator

Generates business documents from templates.

**Capabilities:**
- Proposals, contracts, reports
- Memos, letters, agreements
- Markdown and HTML output
- Custom templates

**Python Modules:**
- `document_builder.py` - Build documents from templates

---

### Meeting Summarizer

Transforms raw meeting notes into structured summaries.

**Capabilities:**
- Parse unstructured notes
- Extract action items
- Identify decisions
- Format summaries

**Python Modules:**
- `meeting_parser.py` - Parse and structure meeting notes

---

### Task Prioritizer

Organizes and prioritizes tasks using proven methodologies.

**Capabilities:**
- Eisenhower Matrix
- MoSCoW prioritization
- Weighted scoring
- Daily planning

**Python Modules:**
- `priority_scorer.py` - Calculate priority scores

---

### Report Writer

Creates professional business reports.

**Capabilities:**
- Status reports
- Progress reports
- Executive summaries
- Analysis reports

**Python Modules:**
- `report_generator.py` - Generate reports from templates

---

### Create Skill

Meta-skill for creating new skills and extending The Architect.

**Capabilities:**
- Generate skill structure
- Build from templates
- Validate skill quality
- Self-evolution support

**Python Modules:**
- `skill_generator.py` - Generate skill directory structure
- `template_builder.py` - Build from predefined templates
- `validator.py` - Validate skill structure and content

## Architecture

### Skill Definition (SKILL.md)

Each skill is defined in a `SKILL.md` file with:

```yaml
---
name: Skill Name
description: This skill should be used when the user asks to "trigger 1", "trigger 2", "trigger 3", or mentions related context.
version: 1.0.0
---

# Skill content...
```

### Python Scripts

All scripts are pure Python with minimal dependencies:

- Type hints for clarity
- Docstrings for documentation
- Example usage in `if __name__ == "__main__"`
- Graceful error handling

### Validation

Validate any skill using:

```python
from skills.create_skill.scripts.validator import SkillValidator
from pathlib import Path

validator = SkillValidator(Path("skills/my-skill"))
result = validator.validate_all()

if result.valid:
    print("✓ Skill is valid")
else:
    for error in result.errors:
        print(f"✗ {error}")
```

## Contributing

### Adding a New Skill

1. Use `create-skill` to generate the structure
2. Edit `SKILL.md` with your skill definition
3. Add Python scripts to `scripts/`
4. Document in `references/`
5. Provide examples in `examples/`
6. Validate with `validator.py`

### Skill Guidelines

- **Keep SKILL.md concise** (1,500-2,000 words)
- **Use specific trigger phrases** in descriptions
- **Write pure Python** with minimal dependencies
- **Include example usage** in scripts
- **Provide comprehensive references**
- **Add practical examples**

### Validation Checklist

- [ ] SKILL.md has proper frontmatter
- [ ] Description includes trigger phrases
- [ ] Capabilities section present
- [ ] Process steps documented
- [ ] Python scripts have docstrings
- [ ] Examples are runnable
- [ ] References are complete

## About

This repository is **open source** and contains the skill definitions, scripts, and documentation for The Architect.

**Note:** The Architect application itself is proprietary software and will be available soon. This repository provides the skill framework and content that powers The Architect's capabilities.

## About

This repository contains the open-source skills for The Architect. The skills are freely available for use, modification, and distribution under the MIT License.

**Note:** The Architect application itself is proprietary software and is not open source. The app will be available soon. For updates and announcements, visit [The A-Tech Corporation](https://theatechcorporation.com).

## Maintainer

**The A-Tech Corporation PTY LTD**

Maintained and managed by [The A-Tech Corporation PTY LTD](https://theatechcorporation.com)

## License

MIT License - See LICENSE file for details.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-12-03 | Initial release with 6 core skills |

---

**The Architect** - Evolving business productivity, one skill at a time.
