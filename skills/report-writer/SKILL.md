---
name: Report Writer
description: This skill should be used when the user asks to "write a report", "create a report", "generate a report", "write a business report", "create a status report", "make a progress report", "write an executive summary", "create an analysis report", or mentions report writing, business reporting, or status updates.
version: 1.0.0
---

# Report Writer Skill

Create professional business reports with proper structure, data presentation, and actionable insights.

## Report Types

| Type | Purpose | Audience | Key Focus |
|------|---------|----------|-----------|
| Status Report | Track progress | Stakeholders | Completion, blockers |
| Progress Report | Update on milestones | Management | Timeline, achievements |
| Analysis Report | Examine data/issue | Decision-makers | Insights, recommendations |
| Executive Summary | High-level overview | Executives | Key points, decisions |
| Investigation Report | Document findings | Various | Facts, conclusions |
| Incident Report | Record events | Management | Details, actions taken |

## Standard Report Structure

```markdown
# [Report Title]

## Executive Summary
Brief overview of key findings and recommendations (1-2 paragraphs).

## Introduction
- Purpose of the report
- Scope and limitations
- Methodology (if applicable)

## Key Findings / Status
[Main content - varies by report type]

### [Section 1]
[Content]

### [Section 2]
[Content]

## Analysis
Interpretation of findings, patterns, trends.

## Recommendations
Actionable next steps with owners and timelines.

## Appendix
Supporting data, charts, detailed information.
```

## Writing Principles

1. **Clarity**: Use simple, direct language
2. **Conciseness**: Get to the point quickly
3. **Accuracy**: Verify all facts and figures
4. **Objectivity**: Present facts without bias
5. **Actionability**: Include clear recommendations

## Data Presentation

### Tables
Use for comparing discrete items:
```markdown
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| [Item] | [Value] | [Value] | ✓/✗ |
```

### Lists
Use for sequential or grouped items:
```markdown
- **Finding 1**: Description
  - Supporting detail
  - Impact
```

### Metrics Dashboard
```markdown
## Key Metrics

| Metric | Value | Trend |
|--------|-------|-------|
| [Name] | [Value] | ↑/↓/→ |
```

## Status Report Template

```markdown
# Status Report: [Project/Task Name]

**Period**: [Start Date] - [End Date]
**Author**: [Name]
**Status**: 🟢 On Track / 🟡 At Risk / 🔴 Off Track

## Summary
[2-3 sentence status overview]

## Completed This Period
- ✅ [Task 1]
- ✅ [Task 2]

## In Progress
- 🔄 [Task 3] - [Progress]%

## Upcoming
- 📋 [Task 4] - Start: [Date]
- 📋 [Task 5] - Start: [Date]

## Blockers & Risks
| Issue | Impact | Mitigation | Owner |
|-------|--------|------------|-------|
| [Issue] | [Impact] | [Plan] | [Name] |

## Next Steps
1. [Action 1]
2. [Action 2]
```

## Python Scripts

The `scripts/` directory contains:
- `report_generator.py` - Generate reports from templates
- `data_formatter.py` - Format data for reports
- `chart_creator.py` - Create charts and visualizations
- `executive_summarizer.py` - Create executive summaries

## Usage Examples

See `examples/` directory for:
- Status report examples
- Analysis report templates
- Executive summary samples

## References

See `references/` directory for:
- Report writing best practices
- Data visualization guidelines
- Industry-specific report formats