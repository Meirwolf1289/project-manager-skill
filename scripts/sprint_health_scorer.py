#!/usr/bin/env python3
"""Sprint Health Scorer — multi-dimensional sprint health assessment (0-100).

Usage:
    python sprint_health_scorer.py sprint_data.json

Input JSON format:
{
    "sprint_name": "Sprint 23",
    "committed_points": 40,
    "completed_points": 35,
    "committed_stories": 10,
    "completed_stories": 8,
    "carry_over_stories": 2,
    "bugs_found": 3,
    "bugs_resolved": 2,
    "scope_changes": 1,
    "team_size": 5,
    "sprint_goal_met": true,
    "average_velocity": 38,
    "previous_health_score": 72,
    "blockers_count": 1,
    "blockers_resolved": 1,
    "morale_rating": 4
}

morale_rating: 1-5 scale (optional, defaults to 3)
"""

import json
import sys
from pathlib import Path


def score_velocity(data: dict) -> tuple[float, str]:
    """Score velocity dimension (0-25)."""
    committed = data.get("committed_points", 0)
    completed = data.get("completed_points", 0)
    avg_velocity = data.get("average_velocity", committed)

    if committed == 0:
        return 12.5, "No points committed"

    completion_rate = completed / committed
    velocity_stability = 1 - abs(completed - avg_velocity) / max(avg_velocity, 1)

    score = (completion_rate * 15) + (max(0, velocity_stability) * 10)
    score = max(0, min(25, score))

    if completion_rate >= 0.9:
        note = f"Strong: {completion_rate:.0%} completion rate"
    elif completion_rate >= 0.7:
        note = f"Acceptable: {completion_rate:.0%} completion rate"
    else:
        note = f"Low: {completion_rate:.0%} completion rate — investigate causes"

    return round(score, 1), note


def score_scope(data: dict) -> tuple[float, str]:
    """Score scope stability dimension (0-25)."""
    committed = data.get("committed_stories", 0)
    scope_changes = data.get("scope_changes", 0)
    carry_overs = data.get("carry_over_stories", 0)
    goal_met = data.get("sprint_goal_met", False)

    if committed == 0:
        return 12.5, "No stories committed"

    change_rate = scope_changes / max(committed, 1)
    carry_over_rate = carry_overs / max(committed, 1)

    score = 25.0
    score -= change_rate * 30  # penalize scope changes
    score -= carry_over_rate * 20  # penalize carry-overs
    if not goal_met:
        score -= 8  # significant penalty for missing sprint goal

    score = max(0, min(25, score))

    notes = []
    if change_rate > 0.1:
        notes.append(f"Scope change rate {change_rate:.0%} exceeds 10% target")
    if carry_over_rate > 0.05:
        notes.append(f"Carry-over rate {carry_over_rate:.0%} exceeds 5% target")
    if not goal_met:
        notes.append("Sprint goal NOT met")
    if not notes:
        notes.append("Scope stable, goal achieved")

    return round(score, 1), "; ".join(notes)


def score_quality(data: dict) -> tuple[float, str]:
    """Score quality dimension (0-25)."""
    bugs_found = data.get("bugs_found", 0)
    bugs_resolved = data.get("bugs_resolved", 0)
    completed_stories = data.get("completed_stories", 1)

    bug_rate = bugs_found / max(completed_stories, 1)
    resolution_rate = bugs_resolved / max(bugs_found, 1) if bugs_found > 0 else 1.0

    score = 25.0
    score -= bug_rate * 15  # penalize high bug rates
    score += (resolution_rate - 0.5) * 10  # reward high resolution rate

    score = max(0, min(25, score))

    if bugs_found == 0:
        note = "No bugs found this sprint"
    elif resolution_rate >= 0.9:
        note = f"{bugs_found} bugs found, {resolution_rate:.0%} resolved"
    else:
        note = f"{bugs_found} bugs found, only {resolution_rate:.0%} resolved — quality risk"

    return round(score, 1), note


def score_team(data: dict) -> tuple[float, str]:
    """Score team health dimension (0-25)."""
    morale = data.get("morale_rating", 3)  # 1-5 scale
    blockers = data.get("blockers_count", 0)
    blockers_resolved = data.get("blockers_resolved", 0)

    morale_score = (morale / 5) * 15
    blocker_resolution = blockers_resolved / max(blockers, 1) if blockers > 0 else 1.0
    blocker_score = blocker_resolution * 10

    score = morale_score + blocker_score
    score = max(0, min(25, score))

    notes = []
    if morale >= 4:
        notes.append(f"Morale good ({morale}/5)")
    elif morale >= 3:
        notes.append(f"Morale neutral ({morale}/5)")
    else:
        notes.append(f"Morale low ({morale}/5) — needs attention")

    if blockers > 0 and blocker_resolution < 1.0:
        notes.append(f"{blockers - blockers_resolved} unresolved blockers")

    return round(score, 1), "; ".join(notes)


def calculate_health(data: dict) -> dict:
    """Calculate overall sprint health score."""
    vel_score, vel_note = score_velocity(data)
    scope_score, scope_note = score_scope(data)
    qual_score, qual_note = score_quality(data)
    team_score, team_note = score_team(data)

    total = vel_score + scope_score + qual_score + team_score
    total = round(total, 1)

    previous = data.get("previous_health_score")
    trend = None
    if previous is not None:
        diff = total - previous
        if diff > 5:
            trend = f"Improving (+{diff:.1f})"
        elif diff < -5:
            trend = f"Declining ({diff:.1f})"
        else:
            trend = f"Stable ({diff:+.1f})"

    if total >= 80:
        rating = "Excellent"
    elif total >= 65:
        rating = "Good"
    elif total >= 50:
        rating = "Fair"
    elif total >= 35:
        rating = "Concerning"
    else:
        rating = "Critical"

    recommendations = []
    if vel_score < 15:
        recommendations.append("Review estimation accuracy and capacity planning")
    if scope_score < 15:
        recommendations.append("Strengthen sprint commitment process and protect scope")
    if qual_score < 15:
        recommendations.append("Invest in testing practices and code review")
    if team_score < 15:
        recommendations.append("Address team blockers and morale — consider a focused retro")

    return {
        "sprint_name": data.get("sprint_name", "Unknown"),
        "total_score": total,
        "rating": rating,
        "trend": trend,
        "dimensions": {
            "velocity": {"score": vel_score, "max": 25, "note": vel_note},
            "scope": {"score": scope_score, "max": 25, "note": scope_note},
            "quality": {"score": qual_score, "max": 25, "note": qual_note},
            "team": {"score": team_score, "max": 25, "note": team_note},
        },
        "recommendations": recommendations,
    }


def print_report(result: dict):
    """Print a formatted health report."""
    print(f"\n{'='*60}")
    print(f"SPRINT HEALTH REPORT — {result['sprint_name']}")
    print(f"{'='*60}")
    print(f"\nOverall Score: {result['total_score']}/100 ({result['rating']})")
    if result["trend"]:
        print(f"Trend: {result['trend']}")

    print(f"\n{'─'*60}")
    print("DIMENSION SCORES")
    print(f"{'─'*60}")
    for dim, info in result["dimensions"].items():
        bar = "█" * int(info["score"]) + "░" * (25 - int(info["score"]))
        print(f"  {dim.capitalize():12s} {bar} {info['score']}/{info['max']}")
        print(f"  {'':12s} {info['note']}")

    if result["recommendations"]:
        print(f"\n{'─'*60}")
        print("RECOMMENDATIONS")
        print(f"{'─'*60}")
        for i, rec in enumerate(result["recommendations"], 1):
            print(f"  {i}. {rec}")

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

    result = calculate_health(data)
    print_report(result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
