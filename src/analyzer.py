"""Analyze parsed log entries: detect problems and compute stats."""

from collections import Counter

# Simple keyword rules to classify problems
PROBLEM_RULES = {
    "DNS_FAILURE": ["dns", "name resolution", "resolve"],
    "CONNECTION_TIMEOUT": ["timeout", "timed out"],
    "AUTH_FAILURE": ["auth", "authentication", "unauthorized", "403", "401"],
    "CONNECTION_REFUSED": ["refused", "connection refused", "econnrefused"],
}


def detect_problem(message: str) -> str:
    """Classify an error/warn message into a problem type using keywords."""
    lower = message.lower()
    for problem_type, keywords in PROBLEM_RULES.items():
        if any(kw in lower for kw in keywords):
            return problem_type
    return "UNKNOWN"


def compute_stats(entries: list[dict]) -> dict:
    """Compute basic stats: total lines, level counts, top problem type."""
    level_counts = Counter(e["level"] for e in entries)
    problems = [
        detect_problem(e["message"])
        for e in entries
        if e["level"] in ("ERROR", "WARN")
    ]
    problem_counts = Counter(problems)
    top_problem = problem_counts.most_common(1)[0] if problem_counts else ("NONE", 0)

    return {
        "total": len(entries),
        "info": level_counts.get("INFO", 0),
        "warn": level_counts.get("WARN", 0),
        "error": level_counts.get("ERROR", 0),
        "top_problem": top_problem[0],
        "top_problem_count": top_problem[1],
        "problem_breakdown": dict(problem_counts),
    }


def get_error_lines(entries: list[dict]) -> list[str]:
    """Extract raw text of ERROR-level entries for AI analysis."""
    return [
        f"{e['timestamp']} [{e['level']}] {e['message']}"
        for e in entries
        if e["level"] == "ERROR"
    ]
