"""
Strategist Agent
-----------------
First link in the three-agent chain.

Job: take the user's raw input topic (e.g. "new monitoring dashboard
feature launch") and turn it into a structured "content brief":
- Which of Kyron's 4 content pillars does this topic fit best?
- What is the key message?
- Who is the target audience?
- What should the audience do after reading the post?
- Which platform(s) fit this topic best?

This structured output (ContentBrief) is passed directly to the Writer
Agent so post-writing is based on a clear strategic decision, not guesswork.
"""

from google.adk.agents import LlmAgent

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from agents.schemas import ContentBrief
from tools.trends_mcp_server import get_trending_ai_topics


def build_strategist_agent() -> LlmAgent:
    """Builds and returns the Strategist Agent, configured with Kyron's brand."""

    pillars_description = "\n".join(
        f"- {key}: {info['label']} -> goal: {info['goal']}"
        for key, info in config.CONTENT_PILLARS.items()
    )

    instruction = f"""
You are the social media content strategist for the following startup:

Brand name: {config.BRAND_NAME}
Brand description: {config.BRAND_DESCRIPTION}
Brand tone: {config.BRAND_TONE}

Allowed content pillars (choose only from these):
{pillars_description}

Your job:
Analyze the raw topic the user provides and produce a precise content brief.
- Choose pillar based on the closest topical fit, not randomly.
- key_message must be specific and understandable to a non-expert.
- call_to_action must be realistic and match the goal of that pillar.
- Choose recommended_platforms based on the nature of the content:
  technical/specialist content -> LinkedIn, visual/human/quick content ->
  Instagram, it can be both.

If and only if the topic fits the "ai_news" pillar, first call the
get_trending_ai_topics tool to ground yourself in real, current, well-sourced
industry trends, and write a more accurate key_message based on that.
For all other pillars, you do not need to call this tool.

Respond strictly according to the specified output structure.
Write all output field values in English, since Kyron's audience is
international.
"""

    return LlmAgent(
        name="strategist_agent",
        model=config.GEMINI_MODEL,
        description="Analyzes the input topic and produces a strategic content brief for Kyron",
        instruction=instruction,
        tools=[get_trending_ai_topics],
        output_schema=ContentBrief,
        output_key="content_brief",
    )


if __name__ == "__main__":
    # Test agent construction without calling the API (config check only)
    agent = build_strategist_agent()
    print(f"✅ Strategist Agent built: {agent.name}")
    print(f"   Model: {agent.model}")
    print(f"   Expected output: {agent.output_schema.__name__}")
