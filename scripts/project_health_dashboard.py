#!/usr/bin/env python3
"""Project Health Dashboard — portfolio RAG status across all active projects.

Usage:
    python project_health_dashboard.py projects.json

Input JSON format:
{
    "portfolio_name": "Q1 2026 Portfolio",
    "projects": [
        {
            "name": "Project Alpha",
            "planned_end": "2026-03-31",
            "forecast_end": "2026-04-07",
            "budget_approved": 150000,
            "budget_spent": 95000,
            "budget_forecast": 155000,
            "milestones_total": 8,
            "milestones_completed": 5,
            "milestones_on_track": 2,
            "open_risks": 3,
            "high_risks": 1,
            "team_utilization": 82,
            "scope_change_requests": 2,
            "notes": "Integration testing delayed by vendor"
        }
    ]
}
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def calculate_rag(project: dict) -> dict:
    """Calculate RAG status for a single project."""
    scores = {}

    # Schedule RAG
    planned = project.get("planned_end", "")
    forecast = project.get("forecast_end", "")
    if planned and forecast:
        try:
            p_date = datetime.strptime(planned, "%Y-%m-%d")
            f_date = datetime.strptime(forecast, "%Y-%m-%d")
            delay_days = (f_date - p_date).days
            if delay_days <= 0:
                scores["schedule"] = {"status": "GREEN", "detail": "On time"}
            elif delay_days <= 7:
                scores["schedule"] = {"status": "AMBER", "detail": f"{delay_days} days behind"}
            else:
                scores["schedule"] = {"status": "RED", "detail": f"{delay_days} days behind"}
        except ValueError:
            scores["schedule"] = {"status": "AMBER", "detail": "Date parse error"}
    else:
        scores["schedule"] = {"status": "AMBER", "detail": "No dates provided"}

    # Budget RAG
    approved = project.get("budget_approved", 0)
    forecast_budget = project.get("budget_forecast", project.get("budget_spent", 0))
    if approved > 0:
        variance = (forecast_budget - approved) / approved * 100
        if variance <= 0:
            scores["budget"] = {"status": "GREEN", "detail": f"Under budget ({variance:+.1f}%)"}
        elif variance <= 10:
            scores["budget"] = {"status": "AMBER", "detail": f"Over budget ({variance:+.1f}%)"}
        else:
            scores["budget"] = {"status": "RED", "detail": f"Over budget ({variance:+.1f}%)"}
    else:
        scores["budget"] = {"status": "GREEN", "detail": "No budget tracked"}

    # Risk RAG
    high_risks = project.get("high_risks", 0)
    open_risks = project.get("open_risks", 0)
    if high_risks >= 3:
        scores["risk"] = {"status": "RED", "detail": f"{high_risks} high risks"}
    elif high_risks >= 1 or open_risks >= 5:
        scores["risk"] = {"status": "AMBER", "detail": f"{open_risks} open ({high_risks} high)"}
    else:
        scores["risk"] = {"status": "GREEN", "detail": f"{open_risks} open risks"}

    # Scope RAG
    scope_changes = project.get("scope_change_requests", 0)
    if scope_changes >= 5:
        scores["scope"] = {"status": "RED", "detail": f"{scope_changes} change requests"}
    elif scope_changes >= 2:
        scores["scope"] = {"status": "AMBER", "detail": f"{scope_changes} change requests"}
    else:
        scores["scope"] = {"status": "GREEN", "detail": "Scope stable"}

    # Overall RAG (worst of all dimensions)
    statuses = [s["status"] for s in scores.values()]
    if "RED" in statuses:
        overall = "RED"
    elif "AMBER" in statuses:
        overall = "AMBER"
    else:
        overall = "GREEN"

    # Milestone progress
    total_ms = project.get("milestones_total", 0)
    completed_ms = project.get("milestones_completed", 0)
    progress = f"{completed_ms}/{total_ms}" if total_ms > 0 else "N/A"

    return {
        "name": project["name"],
        "overall": overall,
        "dimensions": scores,
        "milestone_progress": progress,
        "team_utilization": project.get("team_utilization", 0),
        "notes": project.get("notes", ""),
    }


def analyze_portfolio(data: dict) -> dict:
    """Analyze all projects in the portfolio."""
    projects = data.get("projects", [])
    portfolio_name = data.get("portfolio_name", "Portfolio")

    if not projects:
        return {"error": "No projects provided"}

    results = [calculate_rag(p) for p in projects]

    # Portfolio summary
    rag_counts = {"GREEN": 0, "AMBER": 0, "RED": 0}
    for r in results:
        rag_counts[r["overall"]] += 1

    avg_utilization = sum(r["team_utilization"] for r in results) / len(results)

    # Identify projects needing attention
    red_projects = [r["name"] for r in results if r["overall"] == "RED"]
    amber_projects = [r["name"] for r in results if r["overall"] == "AMBER"]

    return {
        "portfolio_name": portfolio_name,
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "project_count": len(projects),
        "summary": {
            "green": rag_counts["GREEN"],
            "amber": rag_counts["AMBER"],
            "red": rag_counts["RED"],
            "health_ratio": f"{rag_counts['GREEN']}/{len(projects)} healthy",
        },
        "average_utilization": round(avg_utilization, 1),
        "needs_attention": red_projects,
        "watch_list": amber_projects,
        "projects": results,
    }


def print_report(result: dict):
    """Print formatted portfolio dashboard."""
    if "error" in result:
        print(f"Error: {result['error']}")
        return

    rag_icons = {"GREEN": "🟢", "AMBER": "🟡", "RED": "🔴"}

    print(f"\n{'='*70}")
    print(f"PORTFOLIO HEALTH DASHBOARD — {result['portfolio_name']}")
    print(f"Report Date: {result['report_date']}")
    print(f"{'='*70}")

    s = result["summary"]
    print(f"\nSummary: {rag_icons['GREEN']} {s['green']} Green | {rag_icons['AMBER']} {s['amber']} Amber | {rag_icons['RED']} {s['red']} Red")
    print(f"Average Utilization: {result['average_utilization']}%")

    if result["needs_attention"]:
        print(f"\n⚠️  NEEDS ATTENTION: {', '.join(result['needs_attention'])}")

    print(f"\n{'─'*70}")
    print(f"{'Project':<20} {'Overall':>8} {'Schedule':>10} {'Budget':>10} {'Risk':>8} {'Scope':>8} {'Util':>6}")
    print(f"{'─'*70}")

    for p in result["projects"]:
        dims = p["dimensions"]
        print(
            f"{p['name']:<20} "
            f"{rag_icons[p['overall']]:>8} "
            f"{rag_icons[dims['schedule']['status']]:>10} "
            f"{rag_icons[dims['budget']['status']]:>10} "
            f"{rag_icons[dims['risk']['status']]:>8} "
            f"{rag_icons[dims['scope']['status']]:>8} "
            f"{p['team_utilization']:>5}%"
        )

    print(f"\n{'─'*70}")
    print("DETAILS")
    print(f"{'─'*70}")
    for p in result["projects"]:
        print(f"\n  {rag_icons[p['overall']]} {p['name']} (Milestones: {p['milestone_progress']})")
        for dim, info in p["dimensions"].items():
            print(f"    {dim.capitalize():<12} {rag_icons[info['status']]} {info['detail']}")
        if p["notes"]:
            print(f"    Notes: {p['notes']}")

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

    result = analyze_portfolio(data)
    print_report(result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
