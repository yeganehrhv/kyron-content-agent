
"""
Main Entry Point
----------------
Main execution entry point for the Kyron Content Agent project.

Usage (after setting your real Gemini key in .env):
    python main.py "the topic you want a post generated about"

Example:
    python main.py "We just released a new feature for real-time model monitoring"
"""

import asyncio
import sys
import json

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from pipeline import build_kyron_pipeline


APP_NAME = "kyron_content_agent"
USER_ID = "kyron_demo_user"


async def run_pipeline(topic: str) -> None:
    """Runs the input topic through the full three-agent chain and prints the result."""

    # Each run gets its own session -- so state from previous runs never
    # mixes with the current run's state.
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    pipeline = build_kyron_pipeline()
    runner = Runner(
        app_name=APP_NAME,
        agent=pipeline,
        session_service=session_service,
    )

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=topic)],
    )

    print(f"🚀 Processing topic: {topic}\n")

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=user_message,
    ):
        # Print progress every time an agent finishes its step
        if event.author:
            print(f"   ✅ {event.author} finished.")

    # Read the final state from the session to show the full output
    final_session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session.id
    )
    result = final_session.state.get("reviewer_output")

    print("\n" + "=" * 60)
    print("📋 Final result (after security and quality review):")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    load_dotenv()  # reads the API key from the .env file

    if len(sys.argv) < 2:
        print('Usage: python main.py "your post topic"')
        sys.exit(1)

    topic_arg = " ".join(sys.argv[1:])
    asyncio.run(run_pipeline(topic_arg))
