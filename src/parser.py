"""Parse network log lines into structured data."""

import re
from typing import Optional

# Matches: 2024-01-15 08:23:01 [ERROR] Connection timed out to 10.0.0.1
LOG_PATTERN = re.compile(
    r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+\[(\w+)\]\s+(.*)"
)


def parse_line(line: str) -> Optional[dict]:
    """Parse a single log line into a dict with timestamp, level, message."""
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None
    return {
        "timestamp": match.group(1),
        "level": match.group(2).upper(),
        "message": match.group(3),
    }


def parse_file(filepath: str) -> list[dict]:
    """Read a log file and return a list of parsed log entries."""
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return []
    except PermissionError:
        print(f"Error: No permission to read '{filepath}'.")
        return []

    if not lines:
        print("Warning: Log file is empty.")
        return []

    entries = []
    skipped = 0
    for line in lines:
        if not line.strip():
            continue
        entry = parse_line(line)
        if entry:
            entries.append(entry)
        else:
            skipped += 1

    if skipped > 0:
        print(f"Note: Skipped {skipped} malformed line(s).")

    return entries
