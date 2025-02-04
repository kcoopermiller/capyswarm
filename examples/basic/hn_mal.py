import asyncio
from capyswarm import Swarm, Agent
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    hn_agent = Agent(
        name="Hacker News Agent",
        prompt="You are specialized in web browsing and data extraction from Hacker News.",
        color=(183, 65, 14),
        orchestrator=False
    )

    mal_agent = Agent(
        name="MyAnimeList Agent",
        prompt="You are specialized in web browsing and data extraction from MyAnimeList.",
        color=(47, 82, 162),
        orchestrator=False
    )
    
    orchestrator = Agent(
        name="Orchestrator",
        color=(255, 0, 0),
        orchestrator=True,
    )
    
    async with Swarm([hn_agent, mal_agent, orchestrator], api_key=os.getenv("SCRAPYBARA_API_KEY")) as swarm:
        response = await swarm.run(
            prompt="Collect the top 5 posts from Hacker News (news.ycombinator.com) and the top 5 anime from MyAnimeList (myanimelist.net)"
        )

if __name__ == "__main__":
    asyncio.run(main())