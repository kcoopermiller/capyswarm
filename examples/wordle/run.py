import asyncio
from capyswarm import Swarm
from agents import wordle_agent_1, wordle_agent_2, orchestrator
from dotenv import load_dotenv
import os

load_dotenv()


async def main():
    async with Swarm(
        [wordle_agent_1, wordle_agent_2, orchestrator],
        api_key=os.getenv("SCRAPYBARA_API_KEY"),
    ) as swarm:
        await swarm.run(
            prompt="""
            Play a game of Wordle between Wordle Agent 1 and Wordle Agent 2.
        
            Before instructing Wordle Agent 1 and Wordle Agent 2 to play the game, you must:
            1. In the browser, navigate to https://www.nytimes.com/games/wordle/index.html in two separate tabs
            2. Accept the terms and conditions and continue to the game
            3. Start the game in both tabs
            4. Verify that the game is loaded

            Then, instruct the Wordle Agent 1 and Wordle Agent 2 to play out their respective games. 
            Each agent should try to solve the wordle in 6 tries or less. Each try should be assigned a priority of 1-6.
            """,
            interactive=True,
        )


if __name__ == "__main__":
    asyncio.run(main())
