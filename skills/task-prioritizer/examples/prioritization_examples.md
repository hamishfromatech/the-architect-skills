# Task Prioritization Examples

This document provides examples of task prioritization using different methodologies.

## Eisenhower Matrix Example

### Tasks to Prioritize
1. Fix critical production bug affecting customers
2. Review team pull requests
3. Plan next sprint
4. Update documentation
5. Respond to client emails
6. Research new technologies
7. Prepare presentation for next week
8. Attend optional training session

### Eisenhower Matrix Categorization

| | Urgent | Not Urgent |
|---|---|---|
| **Important** | **DO FIRST** | **SCHEDULE** |
| | Fix critical production bug | Plan next sprint |
| | Respond to client emails | Prepare presentation |
| | | Update documentation |
| **Not Important** | **DELEGATE** | **ELIMINATE** |
| | Review pull requests (delegate to senior dev) | Research new tech (backlog) |
| | | Attend optional training |

### Resulting Priority Order
1. **DO NOW**: Fix production bug
2. **DO TODAY**: Respond to client emails
3. **SCHEDULE**: Plan sprint, prepare presentation
4. **DELEGATE**: Review pull requests
5. **ELIMINATE/BACKLOG**: Research, optional training

---

## MoSCoW Prioritization Example

### Project: Website Redesign

#### MUST HAVE (Critical - Non-negotiable)
- Responsive design
- Fast load times (< 3 seconds)
- Secure payment processing
- Contact form functionality
- SEO basics

#### SHOULD HAVE (Important - But not critical)
- Newsletter signup
- Blog section
- Social media integration
- Customer testimonials
- Live chat widget

#### COULD HAVE (Nice to have)
- Dark mode toggle
- Advanced search
- Wishlist feature
- Multi-language support
- Interactive product demo

#### WON'T HAVE (Not this release)
- Mobile app
- Customer portal
- AI recommendations
- Voice search
- VR product preview

---

## Weighted Scoring Example

### Criteria and Weights
- **Business Impact**: 40% (How much value does this bring?)
- **Urgency**: 30% (How time-sensitive is this?)
- **Effort**: 20% (How much work is required? Lower = better)
- **Dependencies**: 10% (Does this unblock other work?)

### Task Scoring Matrix

| Task | Impact (0.4) | Urgency (0.3) | Effort (0.2) | Deps (0.1) | Total |
|------|-------------|---------------|--------------|------------|-------|
| Production Bug Fix | 10 | 10 | 8 | 5 | 0.88 |
| Client Presentation | 8 | 7 | 6 | 2 | 0.71 |
| Sprint Planning | 7 | 6 | 8 | 8 | 0.69 |
| Documentation Update | 5 | 3 | 4 | 1 | 0.41 |
| Research New Tech | 4 | 2 | 2 | 1 | 0.30 |

### Calculation Example: Production Bug Fix
- Impact: 10 × 0.4 = 4.0
- Urgency: 10 × 0.3 = 3.0
- Effort (inverted): (10-8)/10 × 0.2 = 0.04 (less effort = higher score)
- Dependencies: 5/10 × 0.1 = 0.05
- **Total: 0.88** (Scale to 0-1)

---

## Daily Planning Example

### Available Work Hours: 8 hours

### Prioritized Task List

#### Morning (Deep Work) - 3.5 hours
1. **Production Bug Fix** - 2 hours (Priority: Critical)
2. **Sprint Planning Prep** - 1.5 hours (Priority: High)

#### Afternoon (Meetings & Communications) - 3 hours
1. **Team Standup** - 15 min (Priority: High)
2. **Client Call** - 30 min (Priority: High)
3. **Pull Request Reviews** - 1 hour (Priority: Medium)
4. **Email Processing** - 30 min (Priority: Medium)
5. **Documentation Updates** - 45 min (Priority: Low)

#### End of Day (Review & Planning) - 1.5 hours
1. **Status Report Writing** - 45 min (Priority: Medium)
2. **Tomorrow's Task Prep** - 30 min (Priority: Medium)
3. **Team Slack Check** - 15 min (Priority: Low)

---

## ABCDE Method Example

### Task List

#### A Tasks (Must Do - Serious Consequences)
- **A1**: Fix production bug (customer impact)
- **A2**: Submit tax documents (legal requirement)

#### B Tasks (Should Do - Mild Consequences)
- **B1**: Review team code (delays team progress)
- **B2**: Prepare sprint planning materials

#### C Tasks (Nice to Do - No Consequences)
- **C1**: Organize desktop files
- **C2**: Update personal notes

#### D Tasks (Delegate)
- **D1**: Schedule team meeting (delegate to admin)
- **D2**: Update shared calendar (delegate to team)

#### E Tasks (Eliminate)
- **E1**: Check social media during work
- **E2**: Reorganize office layout

### Action
Start with A1, then A2. Never move to B until all A's are done.

---

## Sprint Backlog Prioritization

### Sprint Goal: Improve User Onboarding Experience

| Priority | Task | Story Points | Dependencies |
|----------|------|--------------|--------------|
| 1 | User registration flow redesign | 5 | None |
| 2 | Welcome email automation | 3 | None |
| 3 | Onboarding tutorial creation | 8 | Task 1 |
| 4 | Progress tracking implementation | 5 | Task 1, 3 |
| 5 | User feedback collection | 2 | None |
| 6 | Analytics dashboard update | 5 | Task 4 |

### Capacity: 21 story points
### Committed: 21 story points (Tasks 1, 2, 3, 5)

---

## Priority Communication Template

```markdown
# Weekly Priority Summary

## This Week's Focus
1. [Primary priority] - Why this matters
2. [Secondary priority] - Why this matters
3. [Tertiary priority] - Why this matters

## High Priority (Do Today)
| Task | Why | Deadline |
|------|-----|----------|
| [Task] | [Impact] | [Date] |

## Medium Priority (This Week)
| Task | Why | Deadline |
|------|-----|----------|
| [Task] | [Impact] | [Date] |

## Low Priority (Backlog)
| Task | Why | Notes |
|------|-----|-------|
| [Task] | [Impact] | [Notes] |

## Blocked
| Task | Blocker | Needs |
|------|---------|-------|
| [Task] | [What's blocking] | [What's needed] |
```