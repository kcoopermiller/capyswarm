import asyncio
from capyswarm import Swarm, Agent
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    browser_agent = Agent(
        name="Hacker News Agent",
        prompt="You are specialized in web browsing and data extraction from Hacker News.",
        orchestrator=False
    )
    
    orchestrator = Agent(
        name="Orchestrator",
        orchestrator=True
    )
    
    async with Swarm([browser_agent, orchestrator], api_key=os.getenv("SCRAPYBARA_API_KEY")) as swarm:
        response = await swarm.run(
            prompt="Collect the top 5 posts from Hacker News (news.ycombinator.com)"
        )

if __name__ == "__main__":
    asyncio.run(main())