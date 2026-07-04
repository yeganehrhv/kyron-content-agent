"""
LinkedIn Skill
--------------
A standalone "skill" that holds LinkedIn writing rules.

Why keep this separate from the agent's own code?
Because the "Agent Skills" concept from the course requires skills to be
modular and reusable -- this same file could be reused by a different
agent in the future without rewriting the Writer Agent from scratch.
"""

import config

PLATFORM_KEY = "linkedin"


def get_writing_guidelines() -> str:
    """Returns LinkedIn-specific writing guidelines."""
    platform_cfg = config.PLATFORMS[PLATFORM_KEY]
    return f"""
[LinkedIn Skill]
- Tone: {platform_cfg['style']}
- Max length: {platform_cfg['max_chars']} characters.
- Structure: strong opening line (hook), 2-4 short paragraphs, one clear
  takeaway, end with 2-3 relevant hashtags.
- Avoid excessive emojis. Professional but human voice.
- Write for a technical / business decision-maker audience.
"""


def validate(text: str) -> list[str]:
    """
    A fast, deterministic check (no language model needed) on the generated
    text. Also used directly as a tool by the Reviewer Agent later on.
    """
    issues = []
    max_chars = config.PLATFORMS[PLATFORM_KEY]["max_chars"]
    if len(text) > max_chars:
        issues.append(
            f"LinkedIn post is {len(text)} characters, over the {max_chars} limit."
        )
    if len(text.strip()) == 0:
        issues.append("Post text is empty.")
    return issues
