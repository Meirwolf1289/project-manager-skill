# JQL Query Patterns

## Sprint Management

### Current sprint items by status
```jql
sprint in openSprints() AND project = "PROJ" ORDER BY status ASC, priority DESC
```

### Carry-over items (not completed in previous sprint)
```jql
sprint in closedSprints() AND status != Done AND project = "PROJ" ORDER BY updated DESC
```

### Sprint scope changes (added mid-sprint)
```jql
labels = "mid-sprint-add" AND sprint in openSprints()
```

### Items without estimates in upcoming sprint
```jql
sprint in futureSprints() AND "Story Points" is EMPTY AND issuetype = Story
```

---

## Backlog Grooming

### Unrefined items (no story points, no acceptance criteria)
```jql
project = "PROJ" AND status = Backlog AND ("Story Points" is EMPTY OR description is EMPTY)
ORDER BY priority DESC, created ASC
```

### Epics without child stories
```jql
issuetype = Epic AND project = "PROJ" AND issueFunction not in hasLinks("is Epic of")
```

### Stories without acceptance criteria
```jql
issuetype = Story AND project = "PROJ" AND description !~ "acceptance criteria"
AND status in (Backlog, Ready) ORDER BY priority DESC
```

### Aged backlog items (>6 months, never started)
```jql
project = "PROJ" AND status = Backlog AND created <= -180d ORDER BY created ASC
```

---

## Bug Tracking

### Open bugs by severity
```jql
issuetype = Bug AND project = "PROJ" AND status != Done
ORDER BY priority DESC, severity DESC, created ASC
```

### Bugs with no assignee
```jql
issuetype = Bug AND project = "PROJ" AND assignee is EMPTY AND status != Done
```

### Bugs created this sprint
```jql
issuetype = Bug AND project = "PROJ" AND sprint in openSprints() AND created >= startOfSprint()
```

### Bug escape rate (bugs found in production)
```jql
issuetype = Bug AND project = "PROJ" AND environment = "production"
AND created >= startOfMonth() AND created <= endOfMonth()
```

---

## Team Performance

### My open items
```jql
assignee = currentUser() AND status != Done ORDER BY priority DESC
```

### Team workload (items per person)
```jql
project = "PROJ" AND status in ("In Progress", "In Review") AND sprint in openSprints()
ORDER BY assignee ASC
```

### Blocked items
```jql
project = "PROJ" AND (flagged = Impediment OR labels = "blocked") AND status != Done
```

### Items updated today
```jql
project = "PROJ" AND updated >= startOfDay() ORDER BY updated DESC
```

---

## Reporting Queries

### Velocity data (completed story points per sprint)
```jql
project = "PROJ" AND issuetype = Story AND status = Done AND sprint in closedSprints()
ORDER BY resolved DESC
```

### Cycle time analysis (time from In Progress to Done)
```jql
project = "PROJ" AND status changed to "Done" AFTER startOfMonth()
AND status was "In Progress" ORDER BY resolved DESC
```

### Release readiness
```jql
fixVersion = "v2.1" AND status != Done ORDER BY priority DESC
```

### Items completed this week
```jql
project = "PROJ" AND status changed to Done DURING (startOfWeek(), endOfWeek())
ORDER BY resolved DESC
```

---

## Dashboard Gadget Queries

### Sprint burndown filter
```jql
sprint in openSprints() AND project = "PROJ"
```

### Epic progress
```jql
issuetype = Epic AND project = "PROJ" AND status != Done ORDER BY rank ASC
```

### Recently resolved
```jql
project = "PROJ" AND resolved >= -7d ORDER BY resolved DESC
```

### Upcoming deadlines
```jql
project = "PROJ" AND duedate <= 7d AND duedate >= 0d AND status != Done
ORDER BY duedate ASC
```
