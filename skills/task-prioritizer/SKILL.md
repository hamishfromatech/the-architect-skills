---
name: Task Prioritizer
description: This skill should be used when the user asks to "prioritize tasks", "organize tasks", "create a task list", "sort priorities", "manage workload", "plan my day", "organize my work", "rank tasks", or mentions task management, priority setting, or workload organization.
version: 1.0.0
---

# Task Prioritizer Skill

Organize and prioritize tasks using proven methodologies to maximize productivity and ensure critical work gets done.

## Prioritization Frameworks

### 1. Eisenhower Matrix
Categorize tasks by urgency and importance:

| | Urgent | Not Urgent |
|---|---|---|
| **Important** | Do First | Schedule |
| **Not Important** | Delegate | Eliminate |

### 2. MoSCoW Method
- **M**ust Have: Critical, non-negotiable
- **S**hould Have: Important but not critical
- **C**ould Have: Nice to have if time permits
- **W**on't Have: Not prioritized this cycle

### 3. Weighted Scoring
Score tasks based on weighted criteria:
```
Priority Score = (Impact × 0.4) + (Urgency × 0.3) + (Effort × 0.2) + (Dependencies × 0.1)
```

### 4. ABCDE Method
- **A**: Must do - serious consequences if not done
- **B**: Should do - mild consequences
- **C**: Nice to do - no consequences
- **D**: Delegate - someone else can do it
- **E**: Eliminate - no value

## Process

1. **List All Tasks**: Gather complete task inventory
2. **Apply Framework**: Choose appropriate prioritization method
3. **Score/Rank**: Assign priority levels
4. **Consider Context**: Account for deadlines, dependencies, resources
5. **Create Schedule**: Assign tasks to time blocks
6. **Review Regularly**: Adjust priorities as needed

## Task Assessment Questions

- What is the deadline?
- What happens if this isn't done?
- Who is waiting for this?
- What other tasks depend on this?
- How long will this take?
- What resources are needed?
- Does this align with current goals?

## Output Formats

### Priority List
```markdown
# Priority Task List

## High Priority (Do Today)
1. [Task] - Due: [Date] - Est: [Time]
2. [Task] - Due: [Date] - Est: [Time]

## Medium Priority (This Week)
1. [Task] - Due: [Date] - Est: [Time]

## Low Priority (Backlog)
1. [Task] - No deadline - Est: [Time]
```

### Daily Plan
```markdown
# Daily Plan - [Date]

## Morning (Deep Work)
- [ ] [Task 1] - 2 hours
- [ ] [Task 2] - 1 hour

## Afternoon (Meetings & Communications)
- [ ] [Task 3] - 30 min
- [ ] [Task 4] - 45 min

## End of Day
- [ ] Review tomorrow's priorities
- [ ] Update task status
```

## Python Scripts

The `scripts/` directory contains:
- `priority_scorer.py` - Calculate priority scores
- `task_scheduler.py` - Generate daily/weekly schedules
- `workload_analyzer.py` - Analyze capacity and distribution
- `dependency_mapper.py` - Map task dependencies

## Usage Examples

See `examples/` directory for:
- Eisenhower matrix examples
- Weighted scoring templates
- Daily planning formats

## References

See `references/` directory for:
- Time management methodologies
- Productivity research
- Prioritization case studies