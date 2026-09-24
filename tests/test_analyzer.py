"""Tests for the log analyzer."""

from src.analyzer import detect_problem, compute_stats


def test_detect_dns_failure():
    """DNS-related messages are classified as DNS_FAILURE."""
    assert detect_problem("DNS resolution failed for api.example.com") == "DNS_FAILURE"


def test_detect_timeout():
    """Timeout messages are classified as CONNECTION_TIMEOUT."""
    assert detect_problem("Connection timed out to 10.0.0.1") == "CONNECTION_TIMEOUT"


def test_detect_auth_failure():
    """Auth-related messages are classified as AUTH_FAILURE."""
    assert detect_problem("Authentication failed for user admin") == "AUTH_FAILURE"


def test_empty_entries_stats():
    """Empty input returns zero counts without crashing."""
    stats = compute_stats([])
    assert stats["total"] == 0
    assert stats["error"] == 0
    assert stats["top_problem"] == "NONE"
