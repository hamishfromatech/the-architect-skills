---
name: Meeting Summarizer
description: This skill should be used when the user asks to "summarize a meeting", "create meeting notes", "write meeting minutes", "summarize discussion", "extract action items", "create a meeting summary", "process meeting notes", or mentions meeting documentation, action items, or follow-ups.
version: 1.0.0
---

# Meeting Summarizer Skill

Transform raw meeting notes into structured, actionable summaries with clear action items and follow-ups.

## Capabilities

- Convert rough meeting notes to polished summaries
- Extract and assign action items
- Identify key decisions and outcomes
- Highlight risks and blockers
- Create follow-up task lists

## Process

1. **Parse Notes**: Read and understand raw meeting notes
2. **Identify Key Elements**: Extract topics, decisions, action items
3. **Structure Summary**: Organize into standardized format
4. **Assign Ownership**: Link action items to responsible parties
5. **Set Deadlines**: Add due dates where specified or needed

## Summary Template

```markdown
# Meeting Summary: [Meeting Title]

**Date**: [Date]
**Time**: [Start Time] - [End Time]
**Location/Platform**: [Location or virtual platform]
**Organizer**: [Name]

## Attendees
- [Name 1] - [Role]
- [Name 2] - [Role]
- ...

## Agenda Items

### 1. [Topic Title]
- Discussion points
- Key insights
- Outcome/Decision

### 2. [Topic Title]
- ...

## Key Decisions
| Decision | Made By | Date |
|----------|---------|------|
| [Decision 1] | [Person] | [Date] |

## Action Items
| Task | Owner | Due Date | Status |
|------|-------|----------|--------|
| [Task 1] | [Name] | [Date] | Pending |
| [Task 2] | [Name] | [Date] | Pending |

## Risks & Blockers
- [Risk/Blocker 1]
- [Risk/Blocker 2]

## Next Steps
1. [Next step 1]
2. [Next step 2]

## Next Meeting
**Date**: [Date]
**Agenda**: [Brief agenda preview]
```

## Action Item Extraction

### Patterns to Identify
- "X will do Y"
- "X to follow up on Z"
- "Action: X to..."
- "Next steps: X..."
- "X responsible for Y"

### Priority Classification
| Priority | Criteria | Action |
|----------|----------|--------|
| Critical | Blocking other work | Immediate follow-up |
| High | Time-sensitive | Track closely |
| Medium | Standard priority | Monitor progress |
| Low | Nice-to-have | Review weekly |

## Output Formats

- **Full Summary**: Complete meeting documentation
- **Executive Summary**: One-paragraph overview
- **Action Items Only**: Focused task list
- **Decision Log**: Key decisions only

## Python Scripts

The `scripts/` directory contains:
- `meeting_parser.py` - Parse raw meeting notes
- `action_extractor.py` - Extract action items automatically
- `summary_formatter.py` - Format summaries in various styles
- `attendee_tracker.py` - Track attendee participation

## Usage Examples

See `examples/` directory for:
- Raw notes to summary examples
- Various meeting type templates
- Action item formats

## References

See `references/` directory for:
- Meeting facilitation best practices
- Documentation standards
- Follow-up communication templates