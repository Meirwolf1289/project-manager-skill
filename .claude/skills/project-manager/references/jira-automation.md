# Jira Automation Rules

## Auto-Transition Rules

### Move to "In Progress" when branch is created
```
Trigger: Branch created
Condition: Issue status = "Ready" OR "Backlog"
Action: Transition issue to "In Progress"
Action: Set assignee to branch creator (if unassigned)
```

### Move to "In Review" when PR is created
```
Trigger: Pull request created
Condition: Issue status = "In Progress"
Action: Transition issue to "In Review"
Action: Add comment "PR created: {{pullRequest.url}}"
```

### Move to "Done" when PR is merged
```
Trigger: Pull request merged
Condition: Issue status = "In Review"
Action: Transition issue to "Done"
Action: Set resolution to "Done"
```

### Auto-close parent when all sub-tasks done
```
Trigger: Sub-task transitioned to "Done"
Condition: All sub-tasks are "Done"
Action: Transition parent to "Done"
```

---

## Assignment & Notification Rules

### Round-robin assignment
```
Trigger: Issue created
Condition: Issue type = "Bug" AND Priority = "Critical"
Action: Assign to next person in rotation list
Action: Send Slack message to #critical-bugs
```

### Notify on blocked items
```
Trigger: Issue flagged
Condition: Flag = "Impediment"
Action: Send email to Scrum Master
Action: Send Slack message to team channel
Action: Add comment "This item has been flagged as blocked"
```

### Remind on stale items
```
Trigger: Scheduled (daily at 9 AM)
Condition: Status = "In Progress" AND updated < -3d
Action: Add comment "This item hasn't been updated in 3 days. @assignee please update."
Action: Send Slack notification to assignee
```

---

## Sprint Management Rules

### Sprint scope change alert
```
Trigger: Issue added to active sprint
Condition: Sprint has started
Action: Send Slack message: "Scope change: {{issue.key}} added to sprint {{sprint.name}}"
Action: Add label "mid-sprint-add"
```

### Auto-move incomplete items
```
Trigger: Sprint completed
Condition: Issue status != "Done"
Action: Move to next sprint
Action: Add label "carry-over"
Action: Add comment "Carried over from {{sprint.name}}"
```

### Sprint start checklist
```
Trigger: Sprint started
Action: Create "Sprint Health Check" task
Action: Send team notification with sprint goal and committed items
```

---

## Cleanup & Hygiene Rules

### Auto-close stale items
```
Trigger: Scheduled (weekly)
Condition: Status = "Backlog" AND updated < -90d
Action: Add comment "Closing due to inactivity (90 days). Reopen if still relevant."
Action: Transition to "Closed"
Action: Set resolution to "Won't Do"
```

### Enforce estimation before sprint
```
Trigger: Issue added to sprint
Condition: Story points is empty AND issue type = "Story"
Action: Block transition (validator)
Action: Add comment "Story points required before adding to sprint"
```

### Link duplicate detection
```
Trigger: Issue created
Condition: Summary similarity > 80% with existing open issue
Action: Add comment "Possible duplicate: {{similar.issue.key}}"
Action: Add label "possible-duplicate"
```

---

## SLA Tracking Rules

### SLA breach warning
```
Trigger: Scheduled (hourly)
Condition: Priority = "Critical" AND status != "Done" AND created > -4h
Action: Send escalation email to team lead
Action: Add comment "SLA breach warning: Critical issue approaching 4-hour resolution target"
```

### First response SLA
```
Trigger: Issue created
Condition: Issue type = "Bug" AND source = "Customer"
Action: Start SLA timer
Action: Send notification to support team
```
