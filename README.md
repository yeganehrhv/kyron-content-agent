# Kyron Content Agent

A multi-agent system that generates professional, brand-safe social media
content (LinkedIn + Instagram) for **Kyron**, a fictional ML/software startup,
built for the *AI Agents: Intensive Vibe Coding Capstone Project* (Agents for
Business track).

## Problem

Small tech startups rarely have time or expertise to produce consistent,
professional social content. This project automates that process end-to-end,
from a single topic idea to a reviewed, publish-ready post.

## Solution — Multi-Agent Architecture

```
User topic
   │
   ▼
┌─────────────────┐     content_brief      ┌─────────────────┐     writer_output      ┌──────────────────┐
│ Strategist Agent │ ─────────────────────▶ │   Writer Agent   │ ─────────────────────▶ │  Reviewer Agent   │
│                  │                        │                  │                        │                    │
│ Decides content  │                        │ Writes posts per  │                        │ Security + brand   │
│ pillar, message, │                        │ platform, using   │                        │ safety check, then │
│ audience, CTA    │                        │ LinkedIn/Instagram│                        │ approves or fixes  │
│                  │                        │ skill modules      │                        │ the final text     │
└─────────────────┘                        └─────────────────┘                        └──────────────────┘
        │ uses MCP tool                                                                          │ uses safety tools
        ▼                                                                                          ▼
  get_trending_ai_topics                                                            check_post_length / check_risky_claims
  (MCP Server)                                                                       (deterministic guardrails)
```

Three specialized agents run in a fixed sequence, each reading the previous
agent's structured output from session state:

1. **Strategist Agent** — turns a raw topic into a structured `ContentBrief`
   (content pillar, key message, audience, call-to-action, target platforms).
   For AI-news topics, it calls a real **MCP Server** tool
   (`get_trending_ai_topics`) to ground itself in current trends.
2. **Writer Agent** — writes one post per recommended platform, using
   platform-specific **Agent Skills** (`skills/linkedin_skill.py`,
   `skills/instagram_skill.py`) so tone/format rules live in reusable,
   swappable modules instead of being hard-coded in the agent.
3. **Reviewer Agent** — a security/quality gate. It calls two deterministic
   tools (`check_post_length`, `check_risky_claims`) so hard rules are never
   left to LLM judgment, then applies its own judgment for brand-tone fit,
   and produces the final, publish-ready text.

## Key concepts demonstrated (course requirement: at least 3 of 6)

| Concept | Where |
|---|---|
| Multi-agent system (ADK `SequentialAgent`) | `pipeline.py` |
| MCP Server | `tools/trends_mcp_server.py` |
| Security features | `tools/content_safety_tool.py`, `agents/reviewer_agent.py` |
| Agent Skills | `skills/linkedin_skill.py`, `skills/instagram_skill.py` |
| Deployability | see "Deployment notes" below |

## Project structure

```
kyron-content-agent/
├── agents/
│   ├── schemas.py            # pydantic models shared between agents
│   ├── strategist_agent.py
│   ├── writer_agent.py
│   └── reviewer_agent.py
├── skills/
│   ├── linkedin_skill.py
│   └── instagram_skill.py
├── tools/
│   ├── content_safety_tool.py
│   └── trends_mcp_server.py
├── config.py                 # brand identity, content pillars, platforms
├── pipeline.py                # wires the 3 agents into one SequentialAgent
├── main.py                    # CLI entry point
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# open .env and paste your real Gemini API key:
# GOOGLE_API_KEY=your_actual_key_here
```

Get a free Gemini API key at: https://ai.google.dev/gemini-api/docs/api-key

## Run

```bash
python main.py "We just released a new feature for real-time model monitoring"
```

The pipeline will print each agent's progress, then the final reviewed
JSON output (approved posts for LinkedIn and/or Instagram).

## News sourcing policy

The MCP trends tool (`tools/trends_mcp_server.py`) only surfaces AI/ML
topics compiled from reputable, well-known, and recently published sources
(official Anthropic and Google announcements, TechCrunch coverage, and
aggregated industry benchmark/pricing data from llm-stats.com and AI
Weekly), each entry tagged with its source. See the module's docstring for
the full sourcing rationale and how this would be swapped for a live feed
from the same outlets in production.

## Deployment notes

This project runs as a CLI script for the capstone demo, but the same
`pipeline.py` object is deployment-ready with minimal changes:

- Wrap `main.py`'s `run_pipeline` in a FastAPI endpoint (FastAPI is already
  an ADK dependency) and deploy on Google Cloud Run for a stateless HTTP API.
- Replace `InMemorySessionService` with a persistent session service for
  multi-user, multi-session production use.
- Swap the static topic list in `trends_mcp_server.py` for a live news API —
  no other code changes required, since it's isolated behind the MCP tool
  interface.

## Security notes

- No API keys are hard-coded anywhere in this repository; `GOOGLE_API_KEY`
  is read from environment variables via `python-dotenv`, and `.env` is
  git-ignored.
- Hard safety rules (max length, risky/unverifiable claims) are enforced by
  deterministic Python functions, not left to LLM judgment alone.

## Why `SequentialAgent` instead of the newer `Workflow` graph API

ADK's `SequentialAgent` currently emits a deprecation warning in favor of a
new graph-based `Workflow` API. We deliberately kept `SequentialAgent`
because it is stable, well-documented, and sufficient for a simple linear
3-step pipeline — the extra complexity of a full graph orchestrator was not
justified given the project scope and timeline.
