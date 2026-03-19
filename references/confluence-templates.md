# Confluence Space & Page Templates

## Recommended Space Hierarchy

```
Team Space Home
├── Getting Started (onboarding guide)
├── Sprint Plans/
│   ├── Sprint 1 - [Goal]
│   ├── Sprint 2 - [Goal]
│   └── ...
├── Meeting Notes/
│   ├── Daily Standups/
│   ├── Sprint Planning/
│   ├── Sprint Reviews/
│   └── Retrospectives/
├── Decision Log/
│   ├── ADR-001: [Decision Title]
│   └── ...
├── Runbooks/
│   ├── Deployment Guide
│   ├── Incident Response
│   └── On-call Procedures
├── Architecture/
│   ├── System Overview
│   ├── API Documentation
│   └── Data Models
└── Team Info/
    ├── Team Charter
    ├── RACI Matrix
    └── Contact & Escalation
```

## Page Templates

### Sprint Plan Page

```markdown
# Sprint [N] Plan — [Sprint Goal]

**Dates:** [Start] — [End]
**Sprint Goal:** [One-sentence goal]
**Capacity:** [X] story points ([Y]% of average velocity)

## Committed Items

| Key | Title | Points | Assignee | Priority |
|-----|-------|--------|----------|----------|
| PROJ-123 | [Title] | 5 | [Name] | High |

**Total committed:** [X] points
**Buffer:** [Y] points reserved for bugs/ops

## Capacity Breakdown

| Team Member | Available Days | Capacity (pts) | Notes |
|-------------|---------------|-----------------|-------|
| [Name] | 9/10 | 8 | PTO Friday |

## Risks & Dependencies

- [ ] [Risk/dependency description] — Owner: [Name]

## Sprint Board
[Link to Jira sprint board]
```

### Meeting Notes Page

```markdown
# [Meeting Type] — [Date]

**Attendees:** [Names]
**Duration:** [X] minutes

## Agenda
1. [Topic]
2. [Topic]

## Discussion Notes
### [Topic 1]
- [Key point]
- [Decision made]

### [Topic 2]
- [Key point]

## Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Action] | [Name] | [Date] | [ ] |

## Decisions Made
- [Decision]: [Rationale]
```

### Decision Log (ADR Format)

```markdown
# ADR-[N]: [Decision Title]

**Date:** [Date]
**Status:** [Proposed | Accepted | Deprecated | Superseded]
**Deciders:** [Names]

## Context
[What is the situation that requires a decision?]

## Decision
[What was decided?]

## Alternatives Considered
1. **[Option A]** — [Pros/Cons]
2. **[Option B]** — [Pros/Cons]

## Consequences
- **Positive:** [Expected benefits]
- **Negative:** [Known drawbacks or risks]
- **Neutral:** [Other impacts]

## Follow-up
- [ ] [Action needed to implement this decision]
```

### Retrospective Page

```markdown
# Sprint [N] Retrospective — [Date]

**Format:** [Start/Stop/Continue | 4Ls | Sailboat | etc.]
**Facilitator:** [Name]
**Sprint Health Score:** [X/100]

## Sprint Metrics
- **Velocity:** [X] points (average: [Y])
- **Goal Achievement:** [Met | Partially Met | Not Met]
- **Carry-over:** [X] items
- **Bugs Found:** [X]

## Discussion

### [Category 1 — e.g., "Start"]
- [Item] (votes: X)
- [Item] (votes: X)

### [Category 2 — e.g., "Stop"]
- [Item] (votes: X)

### [Category 3 — e.g., "Continue"]
- [Item] (votes: X)

## Action Items
| Action | Owner | Due | Sprint | Status |
|--------|-------|-----|--------|--------|
| [Action] | [Name] | [Date] | Sprint N+1 | [ ] |

## Previous Action Item Status
| Action | Owner | Status | Notes |
|--------|-------|--------|-------|
| [From last retro] | [Name] | [Done/Not Done] | [Why] |
```
