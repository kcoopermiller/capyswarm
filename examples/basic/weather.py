import asyncio
from capyswarm import Swarm, Agent
from dotenv import load_dotenv
import os

load_dotenv()


async def main():
    weather_agent = Agent(
        name="Weather Agent",
        prompt="""You are specialized in extracting weather data from weather.com.
        
        Your tasks:
        1. Navigate to weather.com
        2. Get the current weather for the requested location
        3. Extract key data points:
           - Temperature
           - Precipitation chance
           - Wind conditions
           - General weather description
        
        Format your findings in a clear, structured way for the Activity Planner to use.""",
        orchestrator=False,
    )

    planner_agent = Agent(
        name="Activity Planner",
        prompt="""You are specialized in planning outdoor activities based on weather conditions.
        
        Your capabilities:
        1. Analyze weather data to recommend suitable activities
        2. Consider factors like:
           - Temperature ranges
           - Precipitation risk
           - Wind conditions
           - Time of day
        
        Provide activity recommendations with clear reasoning based on the weather data.""",
        orchestrator=False,
    )

    orchestrator = Agent(
        name="Orchestrator",
        orchestrator=True,
    )

    async with Swarm(
        [weather_agent, planner_agent, orchestrator],
        api_key=os.getenv("SCRAPYBARA_API_KEY"),
    ) as swarm:
        await swarm.run(
            prompt="""Get the weather forecast for Tokyo and recommend suitable outdoor activities for today.
            
            The Weather Agent should first collect the weather data, then the Activity Planner should use that data to make recommendations.""",
            interactive=True,
        )


if __name__ == "__main__":
    asyncio.run(main())
