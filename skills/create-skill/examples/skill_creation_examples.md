# Create Skill Examples

## Example 1: Creating a Basic Utility Skill

### User Request
```
"Create a skill for converting units"
```

### Generated SKILL.md
```yaml
---
name: Unit Converter
description: This skill should be used when the user asks to "convert units", "convert to metric", "convert measurement", "temperature conversion", or mentions unit conversion, measurement conversion, or unit conversion.
version: 1.0.0
---

# Unit Converter

Convert between different units of measurement.

## Capabilities

- Convert length units (m, km, ft, mi)
- Convert weight units (kg, lb, oz)
- Convert temperature (C, F, K)
- Convert volume units (L, gal, qt)

## Process

1. **Identify Units**: Determine source and target units
2. **Get Value**: Extract the value to convert
3. **Apply Conversion**: Use appropriate conversion factor
4. **Return Result**: Provide converted value

## Guidelines

- Always specify the original and target units
- Round results to reasonable precision
- Handle edge cases (negative temperatures, etc.)
- Provide context for unusual units

## Python Scripts

The `scripts/` directory contains:
- `unit_converter.py` - Main conversion functions

## Usage Examples

See `examples/` directory for conversion examples.

## References

See `references/` directory for conversion factors.
```

---

## Example 2: Creating a Content Generation Skill

### User Request
```
"Make a skill for writing blog posts"
```

### Generated SKILL.md
```yaml
---
name: Blog Writer
description: This skill should be used when the user asks to "write a blog post", "create blog content", "blog article", "write an article", or mentions blog writing, article creation, or content writing.
version: 1.0.0
---

# Blog Writer

Generate engaging blog posts on various topics.

## Capabilities

- Generate blog post outlines
- Write full blog posts
- Apply SEO optimization
- Format for various platforms

## Process

1. **Understand Topic**: Identify the subject matter
2. **Research Context**: Gather relevant information
3. **Create Outline**: Structure the content
4. **Write Content**: Generate the post
5. **Optimize**: Apply SEO and formatting

## Guidelines

- Use engaging headlines
- Include relevant keywords
- Structure with clear sections
- Keep paragraphs short
- Include call-to-action

## Python Scripts

The `scripts/` directory contains:
- `blog_generator.py` - Generate blog content
- `seo_optimizer.py` - Optimize for search engines

## Usage Examples

See `examples/` directory for sample blog posts.

## References

See `references/` directory for writing guidelines.
```

---

## Example 3: Creating a Workflow Skill

### User Request
```
"Create a skill for managing projects"
```

### Generated SKILL.md
```yaml
---
name: Project Manager
description: This skill should be used when the user asks to "manage project", "create project plan", "track project", "project management", or mentions project planning, task tracking, or milestone management.
version: 1.0.0
---

# Project Manager

Manage projects with planning, tracking, and reporting.

## Capabilities

- Create project plans
- Track task progress
- Manage milestones
- Generate status reports
- Calculate timelines

## Process

1. **Define Scope**: Identify project boundaries
2. **Create Tasks**: Break down into tasks
3. **Assign Resources**: Allocate team members
4. **Set Milestones**: Define checkpoints
5. **Track Progress**: Monitor completion
6. **Report Status**: Generate updates

## Guidelines

- Use SMART goals for tasks
- Include buffer time for estimates
- Regular status updates are essential
- Document blockers immediately
- Celebrate milestone completions

## Python Scripts

The `scripts/` directory contains:
- `project_planner.py` - Create project plans
- `task_tracker.py` - Track task progress
- `milestone_manager.py` - Manage milestones
- `status_reporter.py` - Generate reports

## Usage Examples

See `examples/` directory for project templates.

## References

See `references/` directory for project management best practices.
```

---

## Example 4: Creating an Analysis Skill

### User Request
```
"Add a skill for analyzing data"
```

### Generated SKILL.md
```yaml
---
name: Data Analyzer
description: This skill should be used when the user asks to "analyze data", "perform analysis", "data insights", "analyze trends", or mentions data analysis, statistical analysis, or pattern detection.
version: 1.0.0
---

# Data Analyzer

Analyze data and extract meaningful insights.

## Capabilities

- Statistical analysis
- Trend detection
- Pattern recognition
- Data visualization
- Report generation

## Process

1. **Load Data**: Import data from source
2. **Clean Data**: Handle missing values, outliers
3. **Analyze**: Apply statistical methods
4. **Visualize**: Create charts and graphs
5. **Interpret**: Extract insights
6. **Report**: Generate analysis report

## Guidelines

- Always validate data quality first
- Document assumptions made
- Use appropriate statistical methods
- Visualize key findings
- Provide confidence intervals

## Python Scripts

The `scripts/` directory contains:
- `data_loader.py` - Load and validate data
- `statistics.py` - Statistical functions
- `visualizer.py` - Create visualizations
- `report_generator.py` - Generate reports

## Usage Examples

See `examples/` directory for analysis examples.

## References

See `references/` directory for statistical methods.
```

---

## Example 5: Creating a Communication Skill

### User Request
```
"Create a skill for writing newsletters"
```

### Generated SKILL.md
```yaml
---
name: Newsletter Writer
description: This skill should be used when the user asks to "write newsletter", "create newsletter", "newsletter content", "email newsletter", or mentions newsletter creation, email campaign, or subscriber communication.
version: 1.0.0
---

# Newsletter Writer

Create engaging newsletters for various audiences.

## Capabilities

- Generate newsletter content
- Format for email clients
- Apply brand templates
- Include calls-to-action
- Optimize for engagement

## Process

1. **Understand Audience**: Identify subscriber demographics
2. **Choose Topics**: Select relevant content
3. **Write Content**: Generate engaging copy
4. **Format**: Apply styling and structure
5. **Review**: Check links and rendering
6. **Schedule**: Plan send timing

## Guidelines

- Keep subject lines under 50 characters
- Lead with most important content
- Include clear CTA
- Test on mobile devices
- Maintain consistent branding

## Python Scripts

The `scripts/` directory contains:
- `newsletter_generator.py` - Generate content
- `template_manager.py` - Manage templates
- `engagement_analyzer.py` - Track metrics

## Usage Examples

See `examples/` directory for newsletter templates.

## References

See `references/` directory for newsletter best practices.
```

---

## Using the Skill Generator Script

### Python Example

```python
from skills.create_skill.scripts.skill_generator import SkillGenerator, SkillConfig, SkillType

# Create generator
generator = SkillGenerator()

# Define new skill
config = SkillConfig(
    name="text-summarizer",
    description="Summarize text content",
    trigger_phrases=[
        "summarize this",
        "create a summary",
        "text summary",
        "condense this",
    ],
    skill_type=SkillType.UTILITY,
    needs_scripts=True,
    needs_references=True,
    needs_examples=True,
)

# Generate skill
result = generator.create_skill(config)
print(f"Created skill at: {result.path}")
print(f"Files created: {len(result.files_created)}")
```

### Output
```
Created skill at: skills/text-summarizer
Files created: 4
Directories created: 4
```

---

## Validating a New Skill

```python
from skills.create_skill.scripts.validator import SkillValidator
from pathlib import Path

# Validate the skill
validator = SkillValidator(Path("skills/text-summarizer"))
result = validator.validate_all()

# Check results
if result.valid:
    print("✓ Skill is valid!")
else:
    print("✗ Validation failed:")
    for error in result.errors:
        print(f"  - {error}")

if result.warnings:
    print("Warnings:")
    for warning in result.warnings:
        print(f"  - {warning}")
```

### Output
```
✓ Skill is valid!
Warnings:
  - SKILL.md content seems too short
```

---

## Complete Workflow Example

```python
# Full skill creation workflow

from skills.create_skill.scripts.skill_generator import SkillGenerator, SkillConfig, SkillType
from skills.create_skill.scripts.validator import SkillValidator, print_validation_report
from pathlib import Path

# 1. Create the skill
generator = SkillGenerator()
config = SkillConfig(
    name="calendar-manager",
    description="Manage calendar events and schedules",
    trigger_phrases=[
        "schedule event",
        "add to calendar",
        "manage my calendar",
        "create event",
    ],
    skill_type=SkillType.WORKFLOW,
)

result = generator.create_skill(config)
print(f"Created: {result.path}")

# 2. Validate the skill
validator = SkillValidator(result.path)
validation = validator.validate_all()
print_validation_report({result.path.name: validation})

# 3. Check for improvements
if validation.warnings:
    print("\nSuggested improvements:")
    for warning in validation.warnings:
        print(f"  - {warning}")

# 4. List all skills
all_skills = generator.list_existing_skills()
print(f"\nTotal skills: {len(all_skills)}")
for skill in all_skills:
    print(f"  - {skill}")
```