---
name: project-manager
description: Project management skill for sprint planning, Jira/Confluence workflows, Scrum ceremonies, retrospectives, portfolio health monitoring, and stakeholder reporting. Use this skill whenever the user asks about sprint planning, velocity analysis, backlog grooming, Jira setup, Confluence templates, retrospectives, resource capacity, project health dashboards, risk analysis, or any agile/scrum project management topic. Also trigger when the user mentions standups, sprint reviews, burndown charts, WSJF prioritization, or team health checks.
---

# Project Manager Skill

A comprehensive project management skill for agile teams. Covers the full project lifecycle: from initial setup (Jira project creation, workflow design, Confluence spaces) through execution (sprint planning, daily standups, velocity tracking) to reflection (retrospectives, continuous improvement, executive reporting).

## Capabilities

This skill provides guidance, templates, and analysis tools for:

- **Sprint Planning & Execution** — velocity-based capacity planning, backlog prioritization, sprint goal setting
- **Portfolio Health** — RAG dashboards, risk analysis, resource utilization
- **Retrospectives & Improvement** — structured retro formats, theme extraction, action tracking
- **Jira Administration** — workflows, automation rules, JQL queries, dashboards
- **Confluence Setup** — space hierarchy, page templates, meeting notes, decision logs
- **Stakeholder Reporting** — executive summaries, KPI tracking, milestone updates

## Quick Reference

### Analysis Scripts

The skill includes Python scripts for data-driven project management. Run them with sample JSON data files.

| Script | Purpose | Usage |
|--------|---------|-------|
| `sprint_health_scorer.py` | Sprint health score (0-100) across scope, velocity, quality, morale | `python <skill>/scripts/sprint_health_scorer.py sprint_data.json` |
| `velocity_analyzer.py` | Historical velocity with rolling averages and forecasting | `python <skill>/scripts/velocity_analyzer.py sprint_history.json` |
| `retrospective_analyzer.py` | Theme extraction and action item tracking from retro notes | `python <skill>/scripts/retrospective_analyzer.py retro_notes.json` |
| `project_health_dashboard.py` | Portfolio RAG status, schedule/budget variance | `python <skill>/scripts/project_health_dashboard.py projects.json` |
| `risk_matrix_analyzer.py` | Risk scoring with probability-impact matrix and EMV | `python <skill>/scripts/risk_matrix_analyzer.py risks.json` |
| `resource_capacity_planner.py` | Team allocation, over-utilization detection, capacity forecast | `python <skill>/scripts/resource_capacity_planner.py team.json` |

Replace `<skill>` with the path to this skill directory.

## Workflows

### 1. Sprint Planning

When a user needs to plan a sprint, follow these steps:

1. **Analyze velocity** — review past sprint data to set realistic capacity. If the user has historical data, run `velocity_analyzer.py`. Otherwise, ask about team size, typical velocity, and sprint length.

2. **Check capacity** — account for PTO, holidays, shared resources. Run `resource_capacity_planner.py` if data is available, or walk through capacity manually. Set sprint capacity at ~80% of average velocity to buffer for unknowns.

3. **Prioritize backlog** — apply WSJF (Weighted Shortest Job First) or priority-based selection. See `references/prioritization-models.md` for frameworks. Every committed item should contribute to 1-2 sprint goals. Reserve 10-15% capacity for bugs and operational work.

4. **Document the plan** — create a sprint plan using the template in `assets/sprint_plan_template.md`. Include sprint goal, committed stories, capacity breakdown, and risks.

5. **Set up tracking** — recommend burndown/burnup dashboard, daily standup reminders, and scope change alerts.

### 2. Portfolio Health Review

When a user needs a portfolio-level view across projects:

1. **Collect project data** — schedule performance, budget consumption, scope changes, quality metrics
2. **Generate dashboard** — run `project_health_dashboard.py` for RAG status per project
3. **Analyze risks** — run `risk_matrix_analyzer.py` for EMV and top risks
4. **Check resources** — run `resource_capacity_planner.py` for cross-project allocation
5. **Prepare report** — use `assets/executive_report_template.md` with RAG summary, risk heatmap, and leadership decisions needed

### 3. Retrospective

When facilitating or documenting a retrospective:

1. **Gather metrics** — run `sprint_health_scorer.py` for quantitative context
2. **Select format** — see `references/retro-formats.md` for options:
   - **Start/Stop/Continue** — general-purpose, good for new teams
   - **4Ls** (Liked/Learned/Lacked/Longed For) — learning-focused
   - **Sailboat** — visual metaphor for blockers and accelerators
   - **Mad/Sad/Glad** — emotion-focused, good for morale issues
   - **Starfish** — five categories for nuanced feedback
3. **Analyze output** — run `retrospective_analyzer.py` to extract themes and track action items
4. **Create action items** — limit to 2-3 per sprint, assign owners and due dates
5. **Document** — use `assets/sprint_report_template.md`

### 4. Jira/Confluence Setup for New Teams

When setting up an Atlassian environment:

1. **Define process** — Scrum vs Kanban vs Scrumban, issue types, custom fields
2. **Design workflows** — see `references/jira-workflows.md` for state diagrams, transitions, validators
3. **Configure automation** — see `references/jira-automation.md` for rule templates
4. **Set up Confluence** — see `references/confluence-templates.md` for space hierarchy
5. **Build dashboards** — see `references/jql-patterns.md` for useful queries
6. **Onboard team** — document workflow rules, create quick-reference guide

## Success Metrics

These benchmarks help teams assess their agile maturity:

| Area | Metric | Target |
|------|--------|--------|
| Sprint | Velocity stability (stddev) | <15% of average over 6 sprints |
| Sprint | Goal achievement | >85% fully met |
| Sprint | Scope change rate | <10% mid-sprint |
| Sprint | Carry-over rate | <5% of committed stories |
| Portfolio | On-time delivery | >80% within 1 week of target |
| Portfolio | Budget variance | <10% deviation |
| Portfolio | Risk mitigation | >90% risks have owners + plans |
| Portfolio | Resource utilization | 75-85% (avoid burnout) |
| Process | Retro action completion | >80% within 2 sprints |
| Process | Cycle time reduction | 15%+ over 6 months |
| Reporting | Report cadence | 100% on-time |
| Reporting | Decision turnaround | <3 days from escalation |

## Bundled Resources

For detailed reference material, read these files as needed:

- `references/prioritization-models.md` — WSJF, MoSCoW, Cost of Delay, portfolio scoring
- `references/retro-formats.md` — detailed retro format guides with facilitation tips
- `references/jira-workflows.md` — workflow design patterns, transitions, validators
- `references/jira-automation.md` — automation rule templates for common scenarios
- `references/jql-patterns.md` — JQL query examples for reporting and backlog management
- `references/confluence-templates.md` — page templates and space hierarchy patterns
- `references/risk-management.md` — risk identification, analysis, response strategies
- `references/team-dynamics.md` — Tuckman stages, psychological safety, conflict resolution

Templates (copy and fill in):
- `assets/sprint_plan_template.md`
- `assets/sprint_report_template.md`
- `assets/executive_report_template.md`
- `assets/project_charter_template.md`
- `assets/raci_matrix_template.md`
- `assets/team_health_check_template.md`
