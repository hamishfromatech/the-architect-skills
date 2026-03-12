# Meeting Summarizer

Transform raw meeting notes into structured, actionable summaries with clear action items and follow-ups.

## Overview

The Meeting Summarizer skill converts rough meeting notes into polished summaries, extracts action items, and identifies key decisions and outcomes.

## Quick Start

### Trigger Phrases

Use these phrases to activate the skill:
- "summarize a meeting"
- "create meeting notes"
- "write meeting minutes"
- "summarize discussion"
- "extract action items"
- "create a meeting summary"
- "process meeting notes"

## Capabilities

- Convert rough meeting notes to polished summaries
- Extract and assign action items
- Identify key decisions and outcomes
- Highlight risks and blockers
- Create follow-up task lists

## Output Formats

| Format | Description |
|--------|-------------|
| Full Summary | Complete meeting documentation |
| Executive Summary | One-paragraph overview |
| Action Items Only | Focused task list |
| Decision Log | Key decisions only |

## Summary Template

```markdown
# Meeting Summary: [Title]

**Date**: [Date]
**Attendees**: [Names]

## Key Decisions
| Decision | Made By | Date |
|----------|---------|------|
| [Decision] | [Person] | [Date] |

## Action Items
| Task | Owner | Due Date | Status |
|------|-------|----------|--------|
| [Task] | [Name] | [Date] | Pending |

## Risks & Blockers
- [Risk/Blocker]

## Next Steps
1. [Next step]
```

## Examples

See [examples/meeting_templates.md](examples/meeting_templates.md) for various meeting type templates.

## Python Scripts

- `meeting_parser.py` - Parse raw meeting notes
- `action_extractor.py` - Extract action items automatically
- `summary_formatter.py` - Format summaries in various styles
- `attendee_tracker.py` - Track attendee participation

## License

MIT License - Part of The Architect Skills project.