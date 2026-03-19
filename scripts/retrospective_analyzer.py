#!/usr/bin/env python3
"""Retrospective Analyzer — theme extraction and action item tracking.

Usage:
    python retrospective_analyzer.py retro_notes.json

Input JSON format:
{
    "sprint_name": "Sprint 23",
    "format": "start-stop-continue",
    "items": [
        {"category": "start", "text": "Pair programming on complex features", "votes": 5},
        {"category": "start", "text": "Writing tests before code", "votes": 3},
        {"category": "stop", "text": "Skipping code review for small changes", "votes": 7},
        {"category": "stop", "text": "Working on weekends to meet deadlines", "votes": 6},
        {"category": "continue", "text": "Daily standups at 9:30", "votes": 4},
        {"category": "continue", "text": "Mob programming sessions on Fridays", "votes": 8}
    ],
    "previous_actions": [
        {"action": "Set up automated testing pipeline", "owner": "Alice", "status": "done"},
        {"action": "Create runbook for deployments", "owner": "Bob", "status": "in_progress"},
        {"action": "Reduce meeting load by 20%", "owner": "Carol", "status": "not_started"}
    ]
}
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


# Theme keywords for clustering
THEME_KEYWORDS = {
    "quality": ["test", "bug", "review", "quality", "code review", "coverage", "defect"],
    "process": ["standup", "meeting", "ceremony", "process", "workflow", "sprint", "planning"],
    "collaboration": ["pair", "mob", "team", "communication", "knowledge", "sharing", "help"],
    "workload": ["overtime", "weekend", "burnout", "deadline", "pressure", "capacity", "rush"],
    "technical": ["tech debt", "refactor", "architecture", "performance", "deploy", "CI/CD", "pipeline"],
    "learning": ["learn", "training", "skill", "workshop", "mentor", "growth"],
}


def classify_theme(text: str) -> str:
    """Classify an item into a theme based on keywords."""
    text_lower = text.lower()
    scores = {}
    for theme, keywords in THEME_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[theme] = score
    return max(scores, key=scores.get) if scores else "general"


def analyze_sentiment(items: list) -> dict:
    """Analyze sentiment distribution across categories."""
    positive_categories = {"continue", "liked", "glad", "keep_doing", "more_of", "wind"}
    negative_categories = {"stop", "lacked", "mad", "sad", "less_of", "anchor"}
    neutral_categories = {"start", "learned", "longed_for", "rocks"}

    positive = sum(1 for i in items if i.get("category", "").lower() in positive_categories)
    negative = sum(1 for i in items if i.get("category", "").lower() in negative_categories)
    neutral = len(items) - positive - negative

    total = len(items)
    return {
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "ratio": f"{positive}:{negative}:{neutral}",
        "overall": (
            "Positive" if positive > negative * 1.5
            else "Negative" if negative > positive * 1.5
            else "Balanced"
        ),
    }


def analyze_retro(data: dict) -> dict:
    """Analyze retrospective notes."""
    items = data.get("items", [])
    previous_actions = data.get("previous_actions", [])

    if not items:
        return {"error": "No retrospective items provided"}

    # Sort by votes
    sorted_items = sorted(items, key=lambda x: x.get("votes", 0), reverse=True)

    # Group by category
    by_category = defaultdict(list)
    for item in sorted_items:
        by_category[item.get("category", "uncategorized")].append(item)

    # Theme clustering
    themes = defaultdict(list)
    for item in items:
        theme = classify_theme(item.get("text", ""))
        themes[theme].append({
            "text": item["text"],
            "category": item.get("category", ""),
            "votes": item.get("votes", 0),
        })

    # Sort themes by total votes
    theme_summary = []
    for theme, theme_items in sorted(themes.items(), key=lambda x: sum(i["votes"] for i in x[1]), reverse=True):
        total_votes = sum(i["votes"] for i in theme_items)
        theme_summary.append({
            "theme": theme,
            "total_votes": total_votes,
            "item_count": len(theme_items),
            "top_items": [i["text"] for i in sorted(theme_items, key=lambda x: x["votes"], reverse=True)[:3]],
        })

    # Previous action item tracking
    action_stats = {"done": 0, "in_progress": 0, "not_started": 0}
    for action in previous_actions:
        status = action.get("status", "not_started")
        action_stats[status] = action_stats.get(status, 0) + 1

    total_actions = len(previous_actions)
    completion_rate = action_stats["done"] / max(total_actions, 1)

    # Sentiment
    sentiment = analyze_sentiment(items)

    # Suggested action items (top voted non-positive items)
    suggested_actions = []
    for item in sorted_items[:5]:
        cat = item.get("category", "").lower()
        if cat not in {"continue", "liked", "glad", "keep_doing", "wind"}:
            suggested_actions.append({
                "based_on": item["text"],
                "votes": item.get("votes", 0),
                "theme": classify_theme(item["text"]),
            })

    return {
        "sprint_name": data.get("sprint_name", "Unknown"),
        "format": data.get("format", "Unknown"),
        "total_items": len(items),
        "sentiment": sentiment,
        "top_items": [
            {"text": i["text"], "category": i.get("category"), "votes": i.get("votes", 0)}
            for i in sorted_items[:5]
        ],
        "themes": theme_summary,
        "by_category": {
            cat: [{"text": i["text"], "votes": i.get("votes", 0)} for i in cat_items]
            for cat, cat_items in by_category.items()
        },
        "previous_actions": {
            "total": total_actions,
            "completion_rate": f"{completion_rate:.0%}",
            "breakdown": action_stats,
            "target": ">80%",
            "on_target": completion_rate >= 0.8,
        },
        "suggested_actions": suggested_actions[:3],
    }


def print_report(result: dict):
    """Print formatted retrospective analysis."""
    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print(f"\n{'='*60}")
    print(f"RETROSPECTIVE ANALYSIS — {result['sprint_name']}")
    print(f"{'='*60}")
    print(f"Format: {result['format']} | Items: {result['total_items']} | Sentiment: {result['sentiment']['overall']}")

    print(f"\n{'─'*60}")
    print("TOP VOTED ITEMS")
    print(f"{'─'*60}")
    for i, item in enumerate(result["top_items"], 1):
        print(f"  {i}. [{item['category']}] {item['text']} ({item['votes']} votes)")

    print(f"\n{'─'*60}")
    print("THEMES")
    print(f"{'─'*60}")
    for theme in result["themes"]:
        print(f"\n  {theme['theme'].upper()} ({theme['total_votes']} total votes, {theme['item_count']} items)")
        for item_text in theme["top_items"]:
            print(f"    - {item_text}")

    if result["previous_actions"]["total"] > 0:
        print(f"\n{'─'*60}")
        print("PREVIOUS ACTION ITEMS")
        print(f"{'─'*60}")
        pa = result["previous_actions"]
        status = "ON TARGET" if pa["on_target"] else "BELOW TARGET"
        print(f"  Completion: {pa['completion_rate']} ({status}, target: {pa['target']})")
        print(f"  Done: {pa['breakdown']['done']} | In Progress: {pa['breakdown']['in_progress']} | Not Started: {pa['breakdown']['not_started']}")

    if result["suggested_actions"]:
        print(f"\n{'─'*60}")
        print("SUGGESTED ACTION ITEMS")
        print(f"{'─'*60}")
        for i, action in enumerate(result["suggested_actions"], 1):
            print(f"  {i}. {action['based_on']}")
            print(f"     Theme: {action['theme']} | Votes: {action['votes']}")

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

    result = analyze_retro(data)
    print_report(result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
