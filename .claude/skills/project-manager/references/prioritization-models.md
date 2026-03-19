# Prioritization Models

## WSJF (Weighted Shortest Job First)

WSJF is the gold standard for agile prioritization. It calculates priority as:

```
WSJF = Cost of Delay / Job Duration
```

**Cost of Delay** combines three factors (each scored 1-10):
- **User/Business Value** — how much value does this deliver?
- **Time Criticality** — does value decrease if delayed?
- **Risk Reduction / Opportunity Enablement** — does this reduce risk or unlock future value?

**Job Duration** = estimated effort (story points or t-shirt size mapped to numbers)

### Example

| Feature | Business Value | Time Criticality | Risk Reduction | CoD Total | Duration | WSJF |
|---------|---------------|-------------------|----------------|-----------|----------|------|
| SSO Login | 8 | 3 | 9 | 20 | 5 | 4.0 |
| Dashboard v2 | 7 | 7 | 2 | 16 | 8 | 2.0 |
| Bug Fix Pack | 3 | 9 | 5 | 17 | 2 | 8.5 |

Priority order: Bug Fix Pack (8.5) > SSO Login (4.0) > Dashboard v2 (2.0)

### When to use WSJF
- Sprint planning with competing features
- PI (Program Increment) planning in SAFe
- Any situation where you need to maximize value delivery per unit time

## MoSCoW

Simple four-category classification:

- **Must have** — non-negotiable for this release (the system doesn't work without it)
- **Should have** — important but not critical (workaround exists)
- **Could have** — nice-to-have (include if time permits)
- **Won't have** — explicitly out of scope (but acknowledged for future)

### Guidelines
- Must-haves should be ~60% of sprint capacity
- Should-haves ~20%
- Could-haves ~20%
- If you can't fit all Must-haves, the scope is too large — split the release

### When to use MoSCoW
- Release planning with stakeholders
- MVP definition
- When stakeholders struggle with numerical scoring

## Cost of Delay

Standalone framework focused on the economic impact of not delivering:

### Delay Profiles

1. **Standard** — linear value loss over time (most features)
2. **Urgent** — exponential value loss (security fixes, compliance deadlines)
3. **Fixed Date** — cliff-edge value loss (seasonal features, regulatory deadlines)
4. **Intangible** — hard to quantify but strategically important (tech debt, platform work)

### Calculating Cost of Delay

```
Weekly CoD = (Expected Revenue or Savings) / Time to Market
```

For features without direct revenue impact, use proxy metrics:
- Customer churn prevented
- Support tickets avoided
- Developer productivity gained

## Portfolio Scoring Matrix

For portfolio-level decisions across multiple projects:

| Criterion | Weight | Score (1-5) | Weighted Score |
|-----------|--------|-------------|----------------|
| Strategic alignment | 25% | | |
| Revenue potential | 20% | | |
| Customer impact | 20% | | |
| Technical feasibility | 15% | | |
| Resource availability | 10% | | |
| Risk level (inverse) | 10% | | |
| **Total** | **100%** | | |

Score each project, multiply by weight, rank by total weighted score.
