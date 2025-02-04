import asyncio
from capyswarm import Swarm
from agents import white, black, orchestrator
from dotenv import load_dotenv
import os

load_dotenv()


async def main():
    async with Swarm(
        [white, black, orchestrator], api_key=os.getenv("SCRAPYBARA_API_KEY")
    ) as swarm:
        await swarm.run(
            prompt="""
            Play a game of chess between White and Black agents on https://plainchess.timwoelfle.de/.
        
            Before instructing White and Black agents to play the game, you must:
            1. Opening the game URL
            2. Starting an offline chess game between the two agents
            3. Verifying that the game is loaded

            Then, instruct the White and Black agents to play out the first 10 moves of the game (assign priority to each move accordingly).
            """,
            interactive=True,
        )


if __name__ == "__main__":
    asyncio.run(main())
