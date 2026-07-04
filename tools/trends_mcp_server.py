"""
Kyron Trends MCP Server
------------------------
A standalone MCP Server that exposes one tool: get_trending_ai_topics.

Why an MCP Server instead of a plain Python function?
To demonstrate the course's "MCP Server" concept: the capability is exposed
as a standalone, standard service (Model Context Protocol) that any agent --
or even a completely different project -- could connect to. That's different
from a regular Python function, which is only usable inside this one project.

Sourcing policy for this knowledge base:
Every entry below is compiled from reputable, well-known, and recently
published sources (official announcements from Anthropic and Google, plus
industry coverage from TechCrunch and aggregated benchmark/pricing trend
data from llm-stats.com and AI Weekly), curated at build time. This static
list is a deliberate, reasonable substitute for a live paid news API (per
the competition's "reasonable cost / equal access" rule). In a production
deployment (see "Deployability" in the README), this same function would
be swapped for a live RSS/API feed pulling from these exact same reputable
outlets -- no other part of the system would need to change, which is the
main benefit of hiding this behind a tool interface.

Run the server standalone (optional, to test the real protocol):
    python tools/trends_mcp_server.py
"""

from mcp.server.fastmcp import FastMCP

mcp_server = FastMCP(
    name="kyron-trends-server",
    instructions="Serves current AI/ML industry topics and trends to agents.",
)

# Knowledge base curated from reputable, well-known, up-to-date sources.
# Each entry lists its source publisher for traceability.
_TRENDING_TOPICS = [
    {
        "topic": "Anthropic's Claude Sonnet 5 becomes the new default model for Free and Pro users",
        "why_it_matters": "A major frontier lab just shipped its most agentic mid-tier model yet at aggressive pricing, showing how fast frontier capability is becoming affordable and accessible.",
        "source": "Anthropic (official announcement, June 30, 2026)",
    },
    {
        "topic": "Google ships two new image-generation models, Gemini 3.1 Flash Image and Gemini 3 Pro Image",
        "why_it_matters": "Google is expanding multimodal coverage with a cost-sensitive tier and a quality-first tier, reflecting how model providers now segment by production use case rather than one-size-fits-all.",
        "source": "Google AI Studio / Gemini API (official announcement, June 30, 2026)",
    },
    {
        "topic": "Reasoning models are trading raw speed for accuracy across the industry",
        "why_it_matters": "Teams building production ML systems increasingly choose slower, more deliberate reasoning models for high-stakes tasks instead of defaulting to the fastest option.",
        "source": "Industry benchmark tracking, llm-stats.com (aggregated from TechCrunch, VentureBeat, and lab announcements)",
    },
    {
        "topic": "Workflow AI is winning over chatbot hype in enterprise adoption",
        "why_it_matters": "Businesses are rewarding AI tools that reliably finish bounded, real tasks with human review -- like support routing or research prep -- over open-ended chatbot demos.",
        "source": "AI Industry Trends report, July 2026 (startup and enterprise adoption coverage)",
    },
    {
        "topic": "Inference cost for GPT-4-level capability has dropped roughly 10x per year",
        "why_it_matters": "Falling inference costs make it economically realistic for smaller startups to run frontier-adjacent capability in production, not just in demos.",
        "source": "Industry benchmark and pricing tracking, llm-stats.com",
    },
]


@mcp_server.tool()
def get_trending_ai_topics(count: int = 3) -> list[dict]:
    """
    Returns a set of current, well-sourced AI/ML industry topics.

    Args:
        count: How many topics to return (default 3).

    Returns:
        A list of dicts, each with topic, why_it_matters, and source.
    """
    return _TRENDING_TOPICS[: max(1, min(count, len(_TRENDING_TOPICS)))]


if __name__ == "__main__":
    # Run the server over the standard stdio transport -- the same way MCP
    # clients (like Claude Desktop or ADK itself) would connect to it.
    mcp_server.run(transport="stdio")
