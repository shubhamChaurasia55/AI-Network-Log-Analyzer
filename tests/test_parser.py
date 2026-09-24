"""Tests for the log parser."""

from src.parser import parse_line


def test_parse_info_line():
    """INFO lines are parsed correctly."""
    line = "2024-01-15 08:23:01 [INFO] Server started on port 8080"
    result = parse_line(line)
    assert result is not None
    assert result["level"] == "INFO"
    assert result["timestamp"] == "2024-01-15 08:23:01"
    assert "Server started" in result["message"]


def test_parse_error_line():
    """ERROR lines are parsed correctly."""
    line = "2024-01-15 08:25:30 [ERROR] DNS resolution failed for api.example.com"
    result = parse_line(line)
    assert result is not None
    assert result["level"] == "ERROR"
    assert "DNS resolution failed" in result["message"]


def test_malformed_line_returns_none():
    """Malformed lines return None instead of crashing."""
    assert parse_line("this is not a log line") is None
    assert parse_line("") is None
    assert parse_line("   ") is None
