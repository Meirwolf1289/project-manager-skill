#!/usr/bin/env python3
"""Risk Matrix Analyzer — probability-impact analysis with EMV calculation.

Usage:
    python risk_matrix_analyzer.py risks.json

Input JSON format:
{
    "project": "Project Alpha",
    "risks": [
        {
            "id": "R1",
            "description": "Key developer leaves mid-project",
            "category": "resource",
            "probability": 3,
            "impact": 4,
            "impact_cost": 120000,
            "response": "mitigate",
            "mitigation": "Cross-train team members, document critical knowledge",
            "owner": "PM",
            "status": "open"
        }
    ]
}

probability: 1 (Rare) to 5 (Almost Certain)
impact: 1 (Minimal) to 5 (Critical)
impact_cost: optional, in dollars (for EMV calculation)
response: avoid | mitigate | transfer | accept
status: open | mitigated | closed | accepted
"""

import json
import sys
from collections import Counter
from pathlib import Path


PROB_LABELS = {1: "Rare", 2: "Unlikely", 3: "Possible", 4: "Likely", 5: "Almost Certain"}
IMPACT_LABELS = {1: "Minimal", 2: "Low", 3: "Moderate", 4: "High", 5: "Critical"}
PROB_PERCENTAGES = {1: 0.05, 2: 0.15, 3: 0.35, 4: 0.65, 5: 0.90}


def risk_zone(score: int) -> str:
    """Determine risk zone from probability * impact score."""
    if score >= 13:
        return "RED"
    elif score >= 6:
        return "AMBER"
    else:
        return "GREEN"


def analyze_risks(data: dict) -> dict:
    """Analyze risk register."""
    risks = data.get("risks", [])
    project = data.get("project", "Unknown")

    if not risks:
        return {"error": "No risks provided"}

    analyzed = []
    total_emv = 0

    for risk in risks:
        prob = risk.get("probability", 3)
        impact = risk.get("impact", 3)
        score = prob * impact
        zone = risk_zone(score)

        impact_cost = risk.get("impact_cost", 0)
        prob_pct = PROB_PERCENTAGES.get(prob, 0.35)
        emv = round(impact_cost * prob_pct)
        total_emv += emv

        analyzed.append({
            "id": risk.get("id", "?"),
            "description": risk.get("description", ""),
            "category": risk.get("category", "general"),
            "probability": f"{prob} ({PROB_LABELS.get(prob, '?')})",
            "impact": f"{impact} ({IMPACT_LABELS.get(impact, '?')})",
            "score": score,
            "zone": zone,
            "emv": emv,
            "response": risk.get("response", "unknown"),
            "mitigation": risk.get("mitigation", ""),
            "owner": risk.get("owner", "Unassigned"),
            "status": risk.get("status", "open"),
        })

    # Sort by score descending
    analyzed.sort(key=lambda x: x["score"], reverse=True)

    # Summary stats
    zone_counts = Counter(r["zone"] for r in analyzed)
    category_counts = Counter(r["category"] for r in analyzed if r["status"] == "open")
    unowned = [r for r in analyzed if r["owner"] in ("Unassigned", "", None) and r["status"] == "open"]
    no_mitigation = [r for r in analyzed if not r["mitigation"] and r["status"] == "open" and r["response"] != "accept"]

    return {
        "project": project,
        "total_risks": len(risks),
        "open_risks": sum(1 for r in analyzed if r["status"] == "open"),
        "risk_zones": {
            "red": zone_counts.get("RED", 0),
            "amber": zone_counts.get("AMBER", 0),
            "green": zone_counts.get("GREEN", 0),
        },
        "total_emv": total_emv,
        "categories": dict(category_counts),
        "top_risks": analyzed[:5],
        "all_risks": analyzed,
        "issues": {
            "unowned_risks": [{"id": r["id"], "description": r["description"]} for r in unowned],
            "no_mitigation": [{"id": r["id"], "description": r["description"]} for r in no_mitigation],
        },
    }


def print_report(result: dict):
    """Print formatted risk analysis."""
    if "error" in result:
        print(f"Error: {result['error']}")
        return

    zone_icons = {"RED": "🔴", "AMBER": "🟡", "GREEN": "🟢"}

    print(f"\n{'='*70}")
    print(f"RISK ANALYSIS — {result['project']}")
    print(f"{'='*70}")

    z = result["risk_zones"]
    print(f"\nTotal Risks: {result['total_risks']} (Open: {result['open_risks']})")
    print(f"Zones: 🔴 {z['red']} Red | 🟡 {z['amber']} Amber | 🟢 {z['green']} Green")
    print(f"Total EMV (Contingency Reserve): ${result['total_emv']:,}")

    print(f"\n{'─'*70}")
    print("RISK HEAT MAP")
    print(f"{'─'*70}")
    print(f"  {'':12} Impact→  1(Min)  2(Low)  3(Mod)  4(High) 5(Crit)")

    # Build heat map
    matrix = {}
    for r in result["all_risks"]:
        prob = int(r["probability"].split()[0])
        impact = int(r["impact"].split()[0])
        key = (prob, impact)
        matrix[key] = matrix.get(key, 0) + 1

    for prob in range(5, 0, -1):
        row = f"  P={prob}({PROB_LABELS[prob]:>14}) "
        for impact in range(1, 6):
            count = matrix.get((prob, impact), 0)
            score = prob * impact
            zone = risk_zone(score)
            cell = f"  [{count}]  " if count > 0 else "   .   "
            row += cell
        print(row)

    print(f"\n{'─'*70}")
    print("TOP RISKS (by score)")
    print(f"{'─'*70}")
    for r in result["top_risks"]:
        icon = zone_icons[r["zone"]]
        print(f"\n  {icon} {r['id']}: {r['description']}")
        print(f"    Score: {r['score']} | Prob: {r['probability']} | Impact: {r['impact']}")
        print(f"    EMV: ${r['emv']:,} | Response: {r['response']} | Owner: {r['owner']}")
        if r["mitigation"]:
            print(f"    Mitigation: {r['mitigation']}")

    issues = result["issues"]
    if issues["unowned_risks"] or issues["no_mitigation"]:
        print(f"\n{'─'*70}")
        print("⚠️  ISSUES")
        print(f"{'─'*70}")
        if issues["unowned_risks"]:
            print("  Risks without owners:")
            for r in issues["unowned_risks"]:
                print(f"    - {r['id']}: {r['description']}")
        if issues["no_mitigation"]:
            print("  Risks without mitigation plan:")
            for r in issues["no_mitigation"]:
                print(f"    - {r['id']}: {r['description']}")

    print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    with open(input_path) as f:
        data = json.load(f)

    result = analyze_risks(data)
    print_report(result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
