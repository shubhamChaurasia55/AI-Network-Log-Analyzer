"""Send error logs to Groq API and get structured AI analysis."""

import os
import json
from pydantic import BaseModel

SYSTEM_PROMPT = """You are an expert network troubleshooting assistant.
Analyze ONLY the provided log lines. Do not invent information.
Return your analysis as JSON matching the required schema exactly.
Be concise and actionable in your recommendations."""


class AIAnalysis(BaseModel):
    """Structured response schema for AI log analysis."""
    issue: str
    category: str
    severity: str
    possible_root_cause: str
    evidence: str
    recommended_actions: list[str]


def build_user_prompt(error_lines: list[str]) -> str:
    """Build the user prompt with error log lines."""
    logs = "\n".join(error_lines)
    return (
        f"Analyze these network error logs and provide a diagnosis:\n\n{logs}"
    )


def _build_strict_schema() -> dict:
    """Build a JSON schema with additionalProperties:false for Groq strict mode."""
    return {
        "type": "object",
        "properties": {
            "issue": {"type": "string"},
            "category": {"type": "string"},
            "severity": {"type": "string"},
            "possible_root_cause": {"type": "string"},
            "evidence": {"type": "string"},
            "recommended_actions": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": [
            "issue", "category", "severity",
            "possible_root_cause", "evidence", "recommended_actions",
        ],
        "additionalProperties": False,
    }


def analyze_with_ai(error_lines: list[str]) -> dict | None:
    """Send error lines to Groq API, return parsed AI analysis or None."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Warning: GROQ_API_KEY not set. Skipping AI analysis.")
        return None

    if not error_lines:
        print("No error lines to analyze.")
        return None

    try:
        from groq import Groq

        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(error_lines)},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "network_analysis",
                    "strict": True,
                    "schema": _build_strict_schema(),
                },
            },
            temperature=0.2,
        )

        raw = response.choices[0].message.content
        analysis = AIAnalysis.model_validate(json.loads(raw))
        return analysis.model_dump()

    except ImportError:
        print("Error: 'groq' package not installed. Run: pip install groq")
        return None
    except json.JSONDecodeError:
        print("Error: AI returned invalid JSON.")
        return None
    except Exception as e:
        print(f"Error: AI analysis failed — {e}")
        return None
