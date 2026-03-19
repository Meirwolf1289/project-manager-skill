# Risk Management Framework

## Risk Identification

### Common Risk Categories

| Category | Examples |
|----------|----------|
| **Technical** | New technology, integration complexity, performance requirements |
| **Resource** | Key person dependency, skill gaps, team turnover |
| **Schedule** | Dependencies on external teams, regulatory deadlines, holiday periods |
| **Scope** | Unclear requirements, stakeholder changes, feature creep |
| **Budget** | Vendor cost increases, infrastructure scaling, unplanned hiring |
| **External** | Vendor reliability, market changes, regulatory changes |

### Risk Identification Techniques
- **Brainstorming** — team session to identify risks
- **Checklists** — review common risk categories
- **Expert interviews** — consult subject matter experts
- **Historical analysis** — review past project post-mortems
- **SWOT analysis** — Strengths, Weaknesses, Opportunities, Threats

## Risk Analysis

### Probability-Impact Matrix

Score each risk on two dimensions (1-5 scale):

| | Impact 1 (Minimal) | Impact 2 (Low) | Impact 3 (Moderate) | Impact 4 (High) | Impact 5 (Critical) |
|---|---|---|---|---|---|
| **Prob 5 (Almost Certain)** | 5 | 10 | 15 | 20 | 25 |
| **Prob 4 (Likely)** | 4 | 8 | 12 | 16 | 20 |
| **Prob 3 (Possible)** | 3 | 6 | 9 | 12 | 15 |
| **Prob 2 (Unlikely)** | 2 | 4 | 6 | 8 | 10 |
| **Prob 1 (Rare)** | 1 | 2 | 3 | 4 | 5 |

**Risk zones:**
- **Green (1-5):** Accept — monitor only
- **Amber (6-12):** Mitigate — create mitigation plan
- **Red (13-25):** Escalate — requires immediate action and leadership awareness

### Expected Monetary Value (EMV)

```
EMV = Probability (%) x Impact ($)
```

Use EMV to compare risks quantitatively and calculate contingency reserves.

**Example:**
| Risk | Probability | Impact | EMV |
|------|------------|--------|-----|
| Vendor delay | 30% | $50,000 | $15,000 |
| Key developer leaves | 15% | $120,000 | $18,000 |
| Scope expansion | 40% | $30,000 | $12,000 |
| **Total EMV (contingency reserve)** | | | **$45,000** |

## Risk Response Strategies

### For Threats (Negative Risks)

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| **Avoid** | Change plan to eliminate risk | High probability + high impact |
| **Mitigate** | Reduce probability or impact | Risk is manageable with action |
| **Transfer** | Shift risk to third party (insurance, contracts) | Financial or liability risks |
| **Accept** | Acknowledge and prepare contingency | Low impact or cost of mitigation exceeds impact |

### For Opportunities (Positive Risks)

| Strategy | Description |
|----------|-------------|
| **Exploit** | Ensure the opportunity is realized |
| **Enhance** | Increase probability or impact |
| **Share** | Partner with someone who can capitalize on it |
| **Accept** | Be ready to take advantage if it occurs |

## Risk Register Template

| ID | Risk | Category | Probability | Impact | Score | Response | Owner | Mitigation Plan | Status |
|----|------|----------|-------------|--------|-------|----------|-------|-----------------|--------|
| R1 | [Description] | Technical | 3 | 4 | 12 | Mitigate | [Name] | [Plan] | Open |

## Risk Review Cadence

- **Weekly:** Review top-5 risks in standup or team sync
- **Sprint:** Full risk register review during planning
- **Monthly:** Portfolio-level risk review with leadership
- **Quarterly:** Risk appetite and tolerance review with PMO
