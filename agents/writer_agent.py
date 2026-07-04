"""
Writer Agent
------------
Second link in the chain. Its input is the Strategist Agent's output
(read from session state under the key content_brief -- ADK injects this
automatically).

Important architecture note: the writing guidelines for each platform are
read from the skills/ modules, not hard-coded inside this agent. This means
if we want to add a new platform (e.g. Twitter) tomorrow, we just add a new
skill file and leave this agent untouched.
"""

from google.adk.agents import LlmAgent

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from agents.schemas import WriterOutput
from skills import linkedin_skill, instagram_skill


def build_writer_agent() -> LlmAgent:
    """Builds the Writer Agent, with both platform skills' guidelines injected."""

    instruction = f"""
You are the social media copywriter for {config.BRAND_NAME}.
Brand tone: {config.BRAND_TONE}

Content brief received from the strategist:
{{content_brief}}

Only write a post for the platforms listed in this brief's
recommended_platforms field. For each platform, follow that platform's
writing guide exactly:

{linkedin_skill.get_writing_guidelines()}

{instagram_skill.get_writing_guidelines()}

Write all post content in English. The brand's audience is international.
Base every post strictly on the key_message and call_to_action from the
brief -- do not invent facts about the product that are not implied by
the brief.
"""

    return LlmAgent(
        name="writer_agent",
        model=config.GEMINI_MODEL,
        description="Writes social media posts based on the strategist's brief and platform skills",
        instruction=instruction,
        output_schema=WriterOutput,
        output_key="writer_output",
    )


if __name__ == "__main__":
    agent = build_writer_agent()
    print(f"✅ Writer Agent built: {agent.name}")
    print(f"   Model: {agent.model}")
    print(f"   Expected output: {agent.output_schema.__name__}")
    print(f"   Skills loaded: linkedin_skill, instagram_skill")
