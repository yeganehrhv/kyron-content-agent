"""
Instagram Skill
----------------
Standalone skill for Instagram writing rules (second example of the
Agent Skills pattern).
"""

import config

PLATFORM_KEY = "instagram"


def get_writing_guidelines() -> str:
    """Returns Instagram-specific writing guidelines."""
    platform_cfg = config.PLATFORMS[PLATFORM_KEY]
    return f"""
[Instagram Skill]
- Tone: {platform_cfg['style']}
- Max length: {platform_cfg['max_chars']} characters.
- Structure: attention-grabbing first line (visible before "more"),
  short punchy sentences, tasteful and purposeful emojis.
- End with 5-8 relevant hashtags on a new line.
- Assume the post accompanies an image/carousel (do not describe an image
  in detail, just write copy that works alongside visuals).
"""


def validate(text: str) -> list[str]:
    """Fast, deterministic check on Instagram post text, mirroring the LinkedIn version."""
    issues = []
    max_chars = config.PLATFORMS[PLATFORM_KEY]["max_chars"]
    if len(text) > max_chars:
        issues.append(
            f"Instagram post is {len(text)} characters, over the {max_chars} limit."
        )
    if len(text.strip()) == 0:
        issues.append("Post text is empty.")
    return issues
