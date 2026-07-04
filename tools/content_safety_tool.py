"""
Content Safety Tool
--------------------
This module builds two real "tools" that are handed directly to the
Reviewer Agent so it can call them itself (not just guess based on the
language model's intuition).

Why deterministic Python functions instead of trusting the LLM entirely?
Because a language model can make mistakes judging "text length" or
"presence of a banned phrase", but a simple Python function never makes
a mistake counting characters or searching for a substring. This mirrors
a real-world security pattern: LLM for qualitative judgment, deterministic
code for hard, non-negotiable rules.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills import linkedin_skill, instagram_skill

# Risky phrases a B2B startup should never claim without strong caution
RISKY_CLAIM_PATTERNS = [
    "guaranteed",
    "100% accurate",
    "no risk",
    "instant results",
    "we are the best",
    "world's #1",
    "risk-free",
    "outperforms every",
]

_SKILL_BY_PLATFORM = {
    "linkedin": linkedin_skill,
    "instagram": instagram_skill,
}


def check_post_length(platform: str, text: str) -> list[str]:
    """
    Checks the post text length against the platform's configured limit
    in config.py.

    Args:
        platform: The platform name, either "linkedin" or "instagram".
        text: The final post text to check.

    Returns:
        A list of error messages. An empty list means no problem was found.
    """
    skill = _SKILL_BY_PLATFORM.get(platform)
    if skill is None:
        return [f"Unknown platform: {platform}"]
    return skill.validate(text)


def check_risky_claims(text: str) -> list[str]:
    """
    Scans the text for risky, unverifiable claims (e.g. "guaranteed" or
    "100% accurate") that could damage brand credibility or be considered
    misleading advertising.

    Args:
        text: The final post text to check.

    Returns:
        A list of the risky phrases found in the text.
    """
    lowered = text.lower()
    found = [phrase for phrase in RISKY_CLAIM_PATTERNS if phrase in lowered]
    return [f'Risky phrase found: "{phrase}"' for phrase in found]


if __name__ == "__main__":
    # Quick, standalone test -- no API calls involved
    sample_good = "Our new dashboard helps teams ship ML models faster."
    sample_bad = "Our tool is guaranteed to give 100% accurate results, always!"

    print("Safe text:", check_risky_claims(sample_good))
    print("Risky text:", check_risky_claims(sample_bad))
    print("LinkedIn length (safe):", check_post_length("linkedin", sample_good))
