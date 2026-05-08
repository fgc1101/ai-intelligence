# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Intelligence — an "AI intelligence editor" that automatically collects, filters, summarizes, and publishes AI industry news in plain language for a Chinese-speaking audience.

The core pipeline is: **Collect → Filter → AI Summarize → Translate to plain language → Analyze impact → Auto-publish**

Product docs: `doc/产品落地.md`, `doc/目录结构.md`

## Architecture

```
sources/          Data crawlers — each source has its own directory
  official/       OpenAI, Anthropic, Google AI, HuggingFace, GitHub
  community/      Reddit, HackerNews, Twitter, etc.
pipelines/        Data processing pipelines (collect, clean, summarize, classify, publish)
ai/               AI layer — isolated from business code
  llm/            LLM clients + router (use LiteLLM for unified interface)
  prompts/        Prompt templates
  tasks/          AI tasks: summarize, explain, tagging, scoring, trend_analysis
storage/          Raw data retention (critical — never discard originals)
  raw/ cleaned/ summarized/ published/
configs/          settings.py, sources.yaml, prompt text files
database/         SQLite models and migrations
scripts/          CLI entry points (run_daily.py, rebuild_summary.py, etc.)
services/         Business logic (article, ranking, trend, digest)
publishing/       Output adapters (Telegram, WeChat, email, markdown)
```

Key separation: **sources only fetch**, **pipelines only process**, **AI layer only calls LLMs**. Never mix these responsibilities.

## Tech Stack

- Python, FastAPI, APScheduler, SQLite
- `feedparser`, `requests`, `beautifulsoup4`, `playwright` for crawling
- LiteLLM for unified LLM interface (OpenAI, Claude, Gemini)
- `pip install -r requirements.txt`

## Data Flow

```
crawler → raw JSON → clean pipeline → AI summarize → daily digest → Telegram
```

## Content Rules

- Only ~5% of daily AI news is worth reporting
- Worth reporting: AI capability changes, real industry impact, viral community signals
- Not worth reporting: funding announcements, minor benchmark bumps, marketing
- Content template: (1) what happened, (2) plain-language explanation, (3) who it affects, (4) future trend
- Titles in plain language, never raw technical jargon

## Design Constraints

- No user system, no login, no comments, no social features in MVP
- Raw article data must always be preserved in `storage/raw/` (needed for re-running with new prompts/models)
- All LLM calls go through `ai/llm/router.py` — never call OpenAI/Claude directly in business code
- Source config lives in `configs/sources.yaml`
