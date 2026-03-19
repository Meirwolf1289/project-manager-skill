#!/usr/bin/env python3
"""Resource Capacity Planner — team allocation and capacity forecasting.

Usage:
    python resource_capacity_planner.py team.json

Input JSON format:
{
    "team_name": "Team Alpha",
    "sprint_days": 10,
    "members": [
        {
            "name": "Alice",
            "role": "Developer",
            "available_days": 10,
            "pto_days": 0,
            "story_points_capacity": 8,
            "projects": [
                {"name": "Project Alpha", "allocation_percent": 80},
                {"name": "Project Beta", "allocation_percent": 20}
            ]
        },
        {
            "name": "Bob",
            "role": "Developer",
            "available_days": 8,
            "pto_days": 2,
            "story_points_capacity": 6,
            "projects": [
                {"name": "Project Alpha", "allocation_percent": 100}
            ]
        }
    ]
}
"""

import json
import sys
from collections import defaultdict
from pathlib import Path


def analyze_capacity(data: dict) -> dict:
    """Analyze team capacity and allocation."""
    members = data.get("members", [])
    team_name = data.get("team_name", "Unknown Team")
    sprint_days = data.get("sprint_days", 10)

    if not members:
        return {"error": "No team members provided"}

    member_analysis = []
    project_allocation = defaultdict(lambda: {"allocated_percent": 0, "members": [], "capacity_points": 0})
    total_capacity = 0
    total_available_days = 0
    over_allocated = []
    under_allocated = []

    for member in members:
        name = member.get("name", "Unknown")
        available = member.get("available_days", sprint_days)
        pto = member.get("pto_days", 0)
        effective_days = available - pto
        capacity = member.get("story_points_capacity", 0)

        # Check allocation
        projects = member.get("projects", [])
        total_alloc = sum(p.get("allocation_percent", 0) for p in projects)

        status = "OK"
        if total_alloc > 100:
            status = "OVER-ALLOCATED"
            over_allocated.append({"name": name, "allocation": total_alloc})
        elif total_alloc < 50:
            status = "UNDER-UTILIZED"
            under_allocated.append({"name": name, "allocation": total_alloc})

        # Effective capacity adjusted for allocation
        adjusted_capacity = round(capacity * (effective_days / sprint_days), 1)
        total_capacity += adjusted_capacity
        total_available_days += effective_days

        # Track project allocations
        for proj in projects:
            proj_name = proj.get("name", "Unknown")
            alloc_pct = proj.get("allocation_percent", 0)
            proj_capacity = round(adjusted_capacity * alloc_pct / 100, 1)
            project_allocation[proj_name]["allocated_percent"] += alloc_pct
            project_allocation[proj_name]["members"].append(name)
            project_allocation[proj_name]["capacity_points"] += proj_capacity

        member_analysis.append({
            "name": name,
            "role": member.get("role", ""),
            "sprint_days": sprint_days,
            "available_days": effective_days,
            "pto_days": pto,
            "story_points_capacity": capacity,
            "adjusted_capacity": adjusted_capacity,
            "total_allocation": f"{total_alloc}%",
            "status": status,
            "projects": [
                {"name": p.get("name"), "allocation": f"{p.get('allocation_percent', 0)}%"}
                for p in projects
            ],
        })

    # Team utilization
    max_possible_days = sprint_days * len(members)
    utilization = (total_available_days / max_possible_days * 100) if max_possible_days > 0 else 0

    # Recommended sprint capacity (85% of total for buffer)
    recommended_capacity = round(total_capacity * 0.85, 1)

    return {
        "team_name": team_name,
        "sprint_days": sprint_days,
        "team_size": len(members),
        "summary": {
            "total_capacity_points": round(total_capacity, 1),
            "recommended_commitment": recommended_capacity,
            "total_available_days": total_available_days,
            "max_possible_days": max_possible_days,
            "utilization": f"{utilization:.0f}%",
            "utilization_status": (
                "Optimal" if 75 <= utilization <= 85
                else "High (burnout risk)" if utilization > 85
                else "Low (underutilized)" if utilization < 60
                else "Acceptable"
            ),
        },
        "members": member_analysis,
        "project_allocation": {
            name: {
                "total_allocation_percent": info["allocated_percent"],
                "capacity_points": round(info["capacity_points"], 1),
                "members": info["members"],
            }
            for name, info in project_allocation.items()
        },
        "alerts": {
            "over_allocated": over_allocated,
            "under_utilized": under_allocated,
        },
    }


def print_report(result: dict):
    """Print formatted capacity report."""
    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print(f"\n{'='*65}")
    print(f"RESOURCE CAPACITY REPORT — {result['team_name']}")
    print(f"{'='*65}")

    s = result["summary"]
    print(f"\nTeam Size: {result['team_size']} | Sprint: {result['sprint_days']} days")
    print(f"Total Capacity: {s['total_capacity_points']} story points")
    print(f"Recommended Commitment: {s['recommended_commitment']} story points (85% buffer)")
    print(f"Utilization: {s['utilization']} ({s['utilization_status']})")

    print(f"\n{'─'*65}")
    print("TEAM MEMBERS")
    print(f"{'─'*65}")
    print(f"  {'Name':<15} {'Role':<12} {'Days':>5} {'PTO':>4} {'Capacity':>9} {'Alloc':>7} {'Status':<15}")
    for m in result["members"]:
        status_icon = "⚠️" if m["status"] != "OK" else "✅"
        print(
            f"  {m['name']:<15} {m['role']:<12} "
            f"{m['available_days']:>5} {m['pto_days']:>4} "
            f"{m['adjusted_capacity']:>8.1f} {m['total_allocation']:>7} "
            f"{status_icon} {m['status']}"
        )

    if result["project_allocation"]:
        print(f"\n{'─'*65}")
        print("PROJECT ALLOCATION")
        print(f"{'─'*65}")
        for proj, info in result["project_allocation"].items():
            print(f"\n  {proj}")
            print(f"    Capacity: {info['capacity_points']} pts | Members: {', '.join(info['members'])}")

    alerts = result["alerts"]
    if alerts["over_allocated"] or alerts["under_utilized"]:
        print(f"\n{'─'*65}")
        print("⚠️  ALERTS")
        print(f"{'─'*65}")
        for oa in alerts["over_allocated"]:
            print(f"  🔴 {oa['name']} is over-allocated at {oa['allocation']}%")
        for ua in alerts["under_utilized"]:
            print(f"  🟡 {ua['name']} is under-utilized at {ua['allocation']}%")

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

    result = analyze_capacity(data)
    print_report(result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
