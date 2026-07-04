"""
Shared data models used between agents.
Defined with pydantic so every agent's output is structured and reliable,
instead of free-form text that is fragile to parse.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class ContentBrief(BaseModel):
    """Strategist Agent output: a content brief ready for the Writer Agent."""

    pillar: Literal["ai_news", "behind_the_scenes", "product_promo", "thought_leadership"] = Field(
        description="The content pillar that best fits this topic"
    )
    key_message: str = Field(
        description="The single core message the post must communicate"
    )
    target_audience: str = Field(
        description="The specific target audience for this post (e.g., technical leads at ML teams)"
    )
    call_to_action: str = Field(
        description="The action we want the audience to take after reading the post"
    )
    recommended_platforms: list[Literal["linkedin", "instagram"]] = Field(
        description="Which platforms best fit this topic"
    )


class SocialPost(BaseModel):
    """Writer Agent output: one ready-to-publish post for a specific platform."""

    platform: Literal["linkedin", "instagram"]
    text: str = Field(description="Final post text")
    hashtags: list[str] = Field(description="List of hashtags without the # symbol")


class WriterOutput(BaseModel):
    """Writer Agent output: the set of posts generated for the recommended platforms."""

    posts: list[SocialPost] = Field(
        description="One post per platform recommended in the brief"
    )


class ReviewResult(BaseModel):
    """Reviewer Agent output: the result of a safety and quality check."""

    approved: bool = Field(description="Whether the post is ready to publish as-is")
    issues_found: list[str] = Field(
        default_factory=list,
        description="List of issues found (unverifiable claims, wrong length, off-brand tone, etc.)",
    )

    @field_validator("issues_found", mode="before")
    @classmethod
    def _coerce_none_to_empty_list(cls, value):
        return value if value is not None else []

    final_text: str = Field(
        description="Final post text after any fixes (same as original if no issues were found)"
    )


class ReviewedPost(BaseModel):
    """Review result for one specific post, tied to its platform."""

    platform: Literal["linkedin", "instagram"]
    review: ReviewResult


class ReviewerOutput(BaseModel):
    """Reviewer Agent's final output: the review result for every generated post."""

    reviewed_posts: list[ReviewedPost]
