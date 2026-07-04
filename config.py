"""
Central brand configuration for Kyron.
Every agent reads from this file so tone and brand facts stay consistent
across the whole pipeline. Changing this file is enough to re-target the
whole system at a different brand.
"""

BRAND_NAME = "Kyron"

BRAND_DESCRIPTION = (
    "Kyron is a machine learning software startup that helps development "
    "teams build, test, and ship AI models to production faster."
)

BRAND_TONE = (
    "Professional but approachable, confident without overhyping, clear for "
    "both technical audiences and business decision-makers. Avoid baseless "
    "hype or unverifiable claims."
)

# The four content pillars chosen for Kyron's social strategy
CONTENT_PILLARS = {
    "ai_news": {
        "label": "AI/ML industry news and trends",
        "goal": "Show the team's up-to-date expertise and build thought leadership",
    },
    "behind_the_scenes": {
        "label": "Behind-the-scenes of the team's work",
        "goal": "Humanize the startup, support recruiting and build customer trust",
    },
    "product_promo": {
        "label": "Product/service promotion and conversion",
        "goal": "Turn the audience into sales leads by showing real product value",
    },
    "thought_leadership": {
        "label": "Educational, in-depth ML content",
        "goal": "Teach a technical concept simply to position Kyron as a trusted authority",
    },
}

# Target platforms and their characteristics
PLATFORMS = {
    "linkedin": {
        "max_chars": 3000,
        "style": "More formal, technical, full sentences, max 2-3 hashtags at the end",
    },
    "instagram": {
        "max_chars": 2200,
        "style": "More casual, purposeful emoji use, strong opening hook, 5-8 hashtags at the end",
    },
}

# Underlying model (used in later steps)
GEMINI_MODEL = "gemini-2.5-flash"