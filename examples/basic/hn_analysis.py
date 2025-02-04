import asyncio
from capyswarm import Swarm, Agent
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    browser_agent = Agent(
        name="Browser Agent",
        prompt="You are specialized in web browsing and data extraction.",
        orchestrator=False
    )
    
    data_agent = Agent(
        name="Data Agent",
        prompt="You are specialized in processing and analyzing data.",
        orchestrator=False
    )
    
    orchestrator = Agent(
        name="Orchestrator",
        orchestrator=True
    )
    
    async with Swarm([browser_agent, data_agent, orchestrator], api_key=os.getenv("SCRAPYBARA_API_KEY")) as swarm:
        response = await swarm.run(
            prompt="Collect and analyze the top 5 posts from Hacker News (news.ycombinator.com).",
        )

if __name__ == "__main__":
    asyncio.run(main())