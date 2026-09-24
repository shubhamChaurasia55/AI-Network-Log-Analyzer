# 🔍 AI Network Log Analyzer

A lightweight CLI tool that parses network log files, detects common issues using keyword rules, and provides AI-powered diagnosis using the Groq API.

> **Note:** This is a lightweight prototype — an AI-powered network log analysis assistant. It does not perform real packet inspection or ML model training.

## Features

- **Log Parsing** — Extracts timestamp, level (INFO/WARN/ERROR), and message via regex
- **Problem Detection** — Classifies errors into DNS_FAILURE, CONNECTION_TIMEOUT, AUTH_FAILURE, CONNECTION_REFUSED, or UNKNOWN
- **Basic Stats** — Total lines, level counts, most common problem type
- **AI Analysis** — Sends error lines to Groq API for structured diagnosis with root cause and recommended actions

## Project Structure

```
ai-network-log-analyzer/
├── data/sample.log          # Sample log file
├── src/
│   ├── parser.py            # Parse log lines with regex
│   ├── analyzer.py          # Keyword rules + stats
│   ├── ai_analyzer.py       # Groq API call + Pydantic model
│   └── main.py              # CLI entry point
├── tests/
│   ├── test_parser.py       # Parser tests
│   └── test_analyzer.py     # Analyzer tests
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup

```bash
# 1. Clone and enter the project
cd ai-network-log-analyzer

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

## Set Your API Key

1. Get a free API key at [console.groq.com](https://console.groq.com)
2. Set the environment variable:

```bash
export GROQ_API_KEY="your_key_here"
```

## Run

```bash
python -m src.main data/sample.log
```

## Run Tests

Tests are fully offline — they mock the Groq API and need no API key.

```bash
pytest tests/ -v
```

## Limitations

- Keyword detection uses simple string matching, not NLP
- AI analysis requires an active internet connection and valid Groq API key
- Only processes text-based log files with the expected format
- Single API call per run — very large log files may hit token limits
- This is a prototype for learning purposes, not production monitoring
