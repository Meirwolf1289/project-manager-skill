# Jira Workflow Design Patterns

## Standard Scrum Workflow

```
Backlog → Ready → In Progress → In Review → QA → Done
```

### State Definitions

| State | Entry Criteria | Exit Criteria |
|-------|---------------|---------------|
| Backlog | Created, not yet refined | Refined, estimated, acceptance criteria written |
| Ready | Refined and estimated | Picked up by developer |
| In Progress | Developer assigned and working | Code complete, PR created |
| In Review | PR submitted | PR approved |
| QA | Code merged to staging | Tests pass, QA sign-off |
| Done | QA approved | N/A |

### Transition Rules

**Backlog → Ready:**
- Validator: Story points must be set
- Validator: Description is not empty
- Condition: User has "Developer" role

**Ready → In Progress:**
- Validator: Assignee must be set
- Post-function: Set "Start Date" to current date
- Post-function: Add comment "Work started"

**In Progress → In Review:**
- Validator: At least one linked PR or branch
- Post-function: Notify code reviewers

**In Review → QA:**
- Condition: All linked PRs are merged
- Post-function: Transition linked sub-tasks

**QA → Done:**
- Validator: All sub-tasks must be Done
- Post-function: Set "Resolution" to "Done"
- Post-function: Set "End Date" to current date

---

## Kanban Workflow

```
To Do → In Progress → Done
```

Simpler, with WIP limits instead of sprints:

| State | WIP Limit | Notes |
|-------|-----------|-------|
| To Do | No limit | Prioritized backlog |
| In Progress | 3 per person | Pull-based, not push-based |
| Done | No limit | Archive after 30 days |

---

## Bug Workflow

```
Open → Triaged → In Progress → Fixed → Verified → Closed
                                  ↓
                              Won't Fix → Closed
```

### Triage Fields
- **Severity**: Critical / Major / Minor / Trivial
- **Priority**: Blocker / High / Medium / Low
- **Affected Version**: which release has the bug
- **Environment**: production / staging / development

### SLA Targets by Severity

| Severity | Response Time | Resolution Time |
|----------|--------------|-----------------|
| Critical | 1 hour | 4 hours |
| Major | 4 hours | 24 hours |
| Minor | 1 business day | 1 sprint |
| Trivial | 3 business days | Best effort |

---

## Workflow Best Practices

1. **Keep it simple** — 5-7 states maximum. Every state should represent a meaningful stage where work waits or changes hands.

2. **One way forward** — avoid bidirectional transitions (e.g., Done → In Progress). If rework happens, create a new ticket or sub-task.

3. **Make WIP visible** — even in Scrum, consider WIP limits on "In Progress" and "In Review" to prevent bottlenecks.

4. **Automate transitions** — use Jira automation to move tickets when events happen (branch created, PR merged, build passes).

5. **Separate "Ready" from "Backlog"** — "Ready" means refined, estimated, and committable. This prevents pulling unrefined work into sprints.

6. **Use sub-tasks for breakdown** — parent stories track value delivery, sub-tasks track technical work.

7. **Resolution matters** — always set Resolution on completion. Useful for reporting: Done vs Won't Fix vs Duplicate.
