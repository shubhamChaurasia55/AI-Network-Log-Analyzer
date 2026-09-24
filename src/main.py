"""CLI entry point: parse → analyze → AI → print report."""

import sys
from dotenv import load_dotenv
load_dotenv()  # reads .env file automatically

from src.parser import parse_file
from src.analyzer import compute_stats, get_error_lines
from src.ai_analyzer import analyze_with_ai


def print_stats(stats: dict) -> None:
    """Print basic log statistics to the terminal."""
    print("\n" + "=" * 50)
    print("  📊 LOG ANALYSIS REPORT")
    print("=" * 50)
    print(f"  Total lines parsed : {stats['total']}")
    print(f"  INFO               : {stats['info']}")
    print(f"  WARN               : {stats['warn']}")
    print(f"  ERROR              : {stats['error']}")
    print(f"  Top problem        : {stats['top_problem']} ({stats['top_problem_count']}x)")
    if stats["problem_breakdown"]:
        print("\n  Problem breakdown:")
        for problem, count in stats["problem_breakdown"].items():
            print(f"    {problem:<25} {count}")
    print("=" * 50)


def print_ai_report(analysis: dict) -> None:
    """Print the AI analysis report to the terminal."""
    print("\n" + "=" * 50)
    print("  🤖 AI-POWERED ANALYSIS")
    print("=" * 50)
    print(f"  Issue       : {analysis['issue']}")
    print(f"  Category    : {analysis['category']}")
    print(f"  Severity    : {analysis['severity']}")
    print(f"  Root Cause  : {analysis['possible_root_cause']}")
    print(f"  Evidence    : {analysis['evidence']}")
    print("\n  Recommended Actions:")
    for i, action in enumerate(analysis["recommended_actions"], 1):
        print(f"    {i}. {action}")
    print("=" * 50 + "\n")


def main() -> None:
    """Run the full analysis pipeline."""
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <logfile>")
        print("Example: python -m src.main data/sample.log")
        sys.exit(1)

    filepath = sys.argv[1]
    print(f"\n🔍 Analyzing: {filepath}")

    # Step 1: Parse
    entries = parse_file(filepath)
    if not entries:
        print("No valid log entries found. Exiting.")
        sys.exit(1)

    # Step 2: Stats
    stats = compute_stats(entries)
    print_stats(stats)

    # Step 3: AI Analysis
    error_lines = get_error_lines(entries)
    if error_lines:
        print(f"\n⏳ Sending {len(error_lines)} error line(s) to AI...")
        ai_result = analyze_with_ai(error_lines)
        if ai_result:
            print_ai_report(ai_result)
        else:
            print("\n⚠️  AI analysis unavailable. See warnings above.")
    else:
        print("\n✅ No errors found — nothing to send to AI.")


if __name__ == "__main__":
    main()
