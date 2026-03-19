# Project Manager Skill for Claude Code

A comprehensive project management skill for AI coding assistants. Provides sprint planning, Jira/Confluence workflows, Scrum ceremonies, retrospectives, portfolio health monitoring, and stakeholder reporting capabilities.

## Installation

### Claude Code (Plugin — recommended)
```bash
claude marketplace add https://github.com/Meirwolf1289/project-manager-skill.git
claude plugin install project-manager
```

### Claude Code (Manual)
```bash
git clone https://github.com/Meirwolf1289/project-manager-skill.git /tmp/pm-skill
cp -r /tmp/pm-skill/.claude/skills/project-manager ~/.claude/skills/
```

### Cowork / Claude.ai
```bash
claude marketplace add https://github.com/Meirwolf1289/project-manager-skill.git
claude plugin install project-manager
```
Or add the `SKILL.md` contents to your project knowledge.

## What's Included

### Analysis Scripts (Python)

| Script | Purpose |
|--------|---------|
| `sprint_health_scorer.py` | Multi-dimensional sprint health score (0-100) |
| `velocity_analyzer.py` | Historical velocity analysis with forecasting |
| `retrospective_analyzer.py` | Theme extraction and action item tracking |
| `project_health_dashboard.py` | Portfolio RAG status dashboard |
| `risk_matrix_analyzer.py` | Probability-impact matrix with EMV calculation |
| `resource_capacity_planner.py` | Team allocation and capacity forecasting |

### Reference Guides

| File | Content |
|------|---------|
| `prioritization-models.md` | WSJF, MoSCoW, Cost of Delay frameworks |
| `retro-formats.md` | 5 retrospective formats with facilitation tips |
| `jira-workflows.md` | Workflow design patterns and transition rules |
| `jira-automation.md` | Automation rule templates |
| `jql-patterns.md` | JQL query examples for reporting |
| `confluence-templates.md` | Page templates and space hierarchy |
| `risk-management.md` | Risk identification, analysis, response strategies |
| `team-dynamics.md` | Tuckman stages, psychological safety, conflict resolution |

### Templates

- Sprint Plan
- Sprint Report
- Executive Status Report
- Project Charter
- RACI Matrix
- Team Health Check (Spotify model)

## Usage Examples

### Sprint Health Check
```bash
python scripts/sprint_health_scorer.py sprint_data.json
```

### Velocity Analysis
```bash
python scripts/velocity_analyzer.py sprint_history.json
```

### Portfolio Dashboard
```bash
python scripts/project_health_dashboard.py projects.json
```

See each script's docstring for the expected JSON input format.

## Structure

```
project-manager/
├── SKILL.md              # Skill definition (triggers and workflows)
├── scripts/              # Python analysis tools
├── references/           # Detailed reference material
└── assets/               # Copy-and-fill templates
```

## License

MIT
