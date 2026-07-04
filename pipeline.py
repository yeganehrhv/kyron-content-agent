"""
Pipeline Orchestrator
---------------------
Wires the three agents (Strategist -> Writer -> Reviewer) into a single
pipeline using ADK's SequentialAgent.

Why SequentialAgent?
Because our workflow is inherently step-by-step: without a strategic brief,
the writer doesn't know what to write; without a written post, the reviewer
has nothing to check. Each agent runs exactly once, in order, and writes
its output (via output_key) into session state for the next agent to read.

Note on ADK's newer Workflow API: in very recent ADK versions,
SequentialAgent is superseded by a graph-based API called Workflow and
emits a deprecation warning. We deliberately kept SequentialAgent because:
(1) it is fully stable and not yet removed,
(2) for a simple linear three-step chain, the added complexity of the
    Workflow graph API brings no real benefit,
(3) given this project's tight timeline, stability was prioritized over
    chasing the newest API.
"""

from google.adk.agents import SequentialAgent

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.strategist_agent import build_strategist_agent
from agents.writer_agent import build_writer_agent
from agents.reviewer_agent import build_reviewer_agent


def build_kyron_pipeline() -> SequentialAgent:
    """Builds Kyron's entire content pipeline as a single agent."""

    return SequentialAgent(
        name="kyron_content_pipeline",
        description=(
            "Kyron's full social media content pipeline: from a raw topic "
            "to a final, reviewed post ready to publish."
        ),
        sub_agents=[
            build_strategist_agent(),
            build_writer_agent(),
            build_reviewer_agent(),
        ],
    )


if __name__ == "__main__":
    pipeline = build_kyron_pipeline()
    print(f"✅ Pipeline built: {pipeline.name}")
    print(f"   Number of agents in the chain: {len(pipeline.sub_agents)}")
    for i, sub_agent in enumerate(pipeline.sub_agents, start=1):
        print(f"   {i}. {sub_agent.name}")
