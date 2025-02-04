import asyncio
from capyswarm import Swarm, Agent
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    metadata_agent = Agent(
        name="Metadata Analyst",
        prompt="You are specialized in analyzing GitHub repository metadata, including stars, forks, issues, and community metrics. Focus on gathering and analyzing repository statistics and community health indicators.",
        color="93",
        orchestrator=False
    )
    
    code_agent = Agent(
        name="Code Analyst",
        prompt="You are specialized in analyzing GitHub repository code structure, architecture, and patterns. Focus on examining code organization, key features, and technical implementation details.",
        color="96",
        orchestrator=False
    )
    
    orchestrator = Agent(
        name="Orchestrator",
        color="92",
        orchestrator=True
    )
    
    async with Swarm([metadata_agent, code_agent, orchestrator], api_key=os.getenv("SCRAPYBARA_API_KEY")) as swarm:
        response = await swarm.run(
            prompt="""
            Analyze the fastapi/fastapi GitHub repository (github.com/tiangolo/fastapi). 
            Work together to create a comprehensive analysis:
            - Metadata Agent: Focus on community metrics, popularity trends, and repository statistics
            - Code Agent: Focus on codebase structure, key features, and implementation patterns
            
            Agents should share findings with each other to make connections between community metrics and code quality.
            For example, if certain features have more community engagement or if code patterns affect adoption.
            """
        )

if __name__ == "__main__":
    asyncio.run(main()) 