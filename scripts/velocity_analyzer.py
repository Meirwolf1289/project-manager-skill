#!/usr/bin/env python3
"""Velocity Analyzer — historical velocity analysis with forecasting.

Usage:
    python velocity_analyzer.py sprint_history.json

Input JSON format:
{
    "team": "Team Alpha",
    "sprints": [
        {"name": "Sprint 18", "committed": 35, "completed": 32, "sprint_days": 10},
        {"name": "Sprint 19", "committed": 38, "completed": 36, "sprint_days": 10},
        {"name": "Sprint 20", "committed": 40, "completed": 34, "sprint_days": 10},
        {"name": "Sprint 21", "committed": 37, "completed": 37, "sprint_days": 10},
        {"name": "Sprint 22", "committed": 42, "completed": 38, "sprint_days": 10},
        {"name": "Sprint 23", "committed": 40, "completed": 35, "sprint_days": 10}
    ]
}
"""

import json
import sys
import math
from pathlib import Path


def analyze_velocity(data: dict) -> dict:
    """Analyze velocity trends and generate forecast."""
    sprints = data.get("sprints", [])
    team = data.get("team", "Unknown Team")

    if not sprints:
        return {"error": "No sprint data provided"}

    completed = [s["completed"] for s in sprints]
    committed = [s["committed"] for s in sprints]

    # Basic stats
    avg_velocity = sum(completed) / len(completed)
    std_dev = math.sqrt(sum((v - avg_velocity) ** 2 for v in completed) / len(completed))
    coefficient_of_variation = (std_dev / avg_velocity * 100) if avg_velocity > 0 else 0

    # Rolling average (last 3 sprints)
    recent = completed[-3:] if len(completed) >= 3 else completed
    rolling_avg = sum(recent) / len(recent)

    # Completion rates
    completion_rates = [
        c / max(co, 1) for c, co in zip(completed, committed)
    ]
    avg_completion_rate = sum(completion_rates) / len(completion_rates)

    # Trend detection
    if len(completed) >= 3:
        first_half = completed[: len(completed) // 2]
        second_half = completed[len(completed) // 2 :]
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        trend_pct = ((second_avg - first_avg) / first_avg * 100) if first_avg > 0 else 0

        if trend_pct > 10:
            trend = "Accelerating"
        elif trend_pct < -10:
            trend = "Decelerating"
        else:
            trend = "Stable"
    else:
        trend = "Insufficient data"
        trend_pct = 0

    # Forecast with confidence intervals
    forecast = {
        "optimistic": round(avg_velocity + std_dev, 1),
        "expected": round(rolling_avg, 1),
        "conservative": round(max(0, avg_velocity - std_dev), 1),
        "recommended_commitment": round(rolling_avg * 0.85, 1),  # 85% of rolling avg
    }

    # Sprint-by-sprint breakdown
    sprint_details = []
    for i, s in enumerate(sprints):
        rate = s["completed"] / max(s["committed"], 1)
        sprint_details.append({
            "name": s["name"],
            "committed": s["committed"],
            "completed": s["completed"],
            "completion_rate": f"{rate:.0%}",
            "delta_from_avg": round(s["completed"] - avg_velocity, 1),
        })

    # Stability assessment
    if coefficient_of_variation < 15:
        stability = "High — predictable delivery"
    elif coefficient_of_variation < 25:
        stability = "Moderate — some variability"
    else:
        stability = "Low — unpredictable, investigate causes"

    return {
        "team": team,
        "sprint_count": len(sprints),
        "statistics": {
            "average_velocity": round(avg_velocity, 1),
            "rolling_average_3sprint": round(rolling_avg, 1),
            "standard_deviation": round(std_dev, 1),
            "coefficient_of_variation": f"{coefficient_of_variation:.1f}%",
            "min_velocity": min(completed),
            "max_velocity": max(completed),
            "average_completion_rate": f"{avg_completion_rate:.0%}",
        },
        "trend": {
            "direction": trend,
            "change_percentage": f"{trend_pct:+.1f}%",
        },
        "stability": stability,
        "forecast": forecast,
        "sprint_details": sprint_details,
    }


def print_report(result: dict):
    """Print formatted velocity report."""
    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print(f"\n{'='*60}")
    print(f"VELOCITY REPORT — {result['team']}")
    print(f"{'='*60}")

    stats = result["statistics"]
    print(f"\nAverage Velocity:     {stats['average_velocity']} pts/sprint")
    print(f"Rolling Avg (3 spr):  {stats['rolling_average_3sprint']} pts/sprint")
    print(f"Std Deviation:        {stats['standard_deviation']}")
    print(f"Variability:          {stats['coefficient_of_variation']}")
    print(f"Range:                {stats['min_velocity']} — {stats['max_velocity']}")
    print(f"Avg Completion Rate:  {stats['average_completion_rate']}")
    print(f"Stability:            {result['stability']}")

    print(f"\n{'─'*60}")
    print("TREND")
    print(f"{'─'*60}")
    print(f"  Direction: {result['trend']['direction']} ({result['trend']['change_percentage']})")

    print(f"\n{'─'*60}")
    print("SPRINT HISTORY")
    print(f"{'─'*60}")
    print(f"  {'Sprint':<15} {'Committed':>10} {'Completed':>10} {'Rate':>8} {'vs Avg':>8}")
    for s in result["sprint_details"]:
        print(f"  {s['name']:<15} {s['committed']:>10} {s['completed']:>10} {s['completion_rate']:>8} {s['delta_from_avg']:>+8.1f}")

    print(f"\n{'─'*60}")
    print("FORECAST (Next Sprint)")
    print(f"{'─'*60}")
    fc = result["forecast"]
    print(f"  Optimistic:              {fc['optimistic']} pts")
    print(f"  Expected:                {fc['expected']} pts")
    print(f"  Conservative:            {fc['conservative']} pts")
    print(f"  Recommended Commitment:  {fc['recommended_commitment']} pts (85% of rolling avg)")
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

    result = analyze_velocity(data)
    print_report(result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
