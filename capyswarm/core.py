# Standard library imports
import asyncio
import webbrowser
from typing import List, Optional, Dict

# Package/library imports
from scrapybara import AsyncScrapybara
from scrapybara.core.api_error import ApiError
from scrapybara.types.act import Message
from scrapybara.types.act import UserMessage, TextPart

# Local imports
from .util import debug_print
from .types import Agent
from .tools import (
    OrchestratorSchema,
    CommunicateTool,
    InspectAgentTool,
    AsyncBashTool,
    AsyncComputerTool,
    AsyncEditTool,
)
from .prompts import get_orchestrator_prompt, get_agent_prompt


class Swarm:
    """A coordinated group of AI agents working together to accomplish complex tasks.
    Args:
        agents (List[Agent]): List of agents, must include exactly one orchestrator
        api_key (Optional[str]): Scrapybara API key for authentication
    """

    def __init__(self, agents: List[Agent], api_key: Optional[str] = None):
        self.client = AsyncScrapybara(api_key=api_key)
        self.instances: Dict[str, any] = {}  # Track active Scrapybara instances
        self.agents = agents
        self.running_tasks = {}  # Track running agent tasks

        orchestrator = [agent for agent in agents if agent.orchestrator]
        match len(orchestrator):
            case 0:
                raise ValueError("Swarm requires exactly one orchestrator agent")
            case 1:
                self.orchestrator = orchestrator[0]
                self.orchestrator.response_schema = OrchestratorSchema
                self.orchestrator.system = get_orchestrator_prompt(self.agents)
            case _:
                raise ValueError("Cannot have multiple orchestrator agents")

        # Set up system prompts for regular agents
        for agent in self.agents:
            if not agent.orchestrator:
                agent.system = get_agent_prompt(agent.name, self.agents, agent.prompt)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up all Scrapybara instances"""
        for instance in self.instances.values():
            try:
                await instance.browser.stop()
                await instance.stop()
            except ApiError as e:
                print(f"Error {e.status_code}: {e.body}")
        self.instances.clear()

    async def _get_or_create_instance(
        self, agent: Agent, interactive: bool = False
    ) -> any:
        """Get existing instance or create new one for agent"""
        if agent.instance in self.instances:
            return self.instances[agent.instance]

        try:
            if agent.instance == "shared":
                instance = await self.client.start_ubuntu(timeout_hours=1)
            else:
                try:
                    instance = next(
                        inst
                        for inst in await self.client.get_instances()
                        if inst.id == agent.instance
                    )
                except StopIteration:
                    print(
                        f"Instance {agent.instance} not found, falling back to shared instance"
                    )
                    agent.instance = "shared"
                    if "shared" in self.instances:
                        return self.instances["shared"]
                    instance = await self.client.start_ubuntu(timeout_hours=1)

            if interactive:
                stream_url = await instance.get_stream_url()
                webbrowser.open(stream_url.stream_url)
                await asyncio.sleep(7)

            self.instances[agent.instance] = instance
            return instance
        except ApiError as e:
            print(f"Error {e.status_code}: {e.body}")
            raise e

    def _setup_agent_tools(self, agent: Agent, instance: any) -> List:
        """Set up the appropriate tools for an agent."""
        tools = []

        if agent.orchestrator:
            tools.append(InspectAgentTool(instance, agent, self))
        else:
            tools.append(CommunicateTool(instance, agent, self))

        if agent.tools:
            return agent.tools + tools

        default_tools = [
            AsyncBashTool(instance),
            AsyncComputerTool(instance),
            AsyncEditTool(instance),
        ]
        return default_tools + tools

    async def run_agent_task(self, agent: Agent, interactive: bool = False):
        """Run a single agent's assigned task"""
        try:
            instance = await self._get_or_create_instance(agent, interactive)
            tools = self._setup_agent_tools(agent, instance)

            response = await self.client.act(
                model=agent.model,
                tools=tools,
                system=agent.system,
                prompt=agent.prompt,
                messages=agent.messages,
                schema=agent.response_schema,
                on_step=agent.on_step,
            )

            if agent.messages is None:
                agent.messages = response.messages
            else:
                agent.messages.extend(response.messages)

            return response
        except Exception as e:
            print(f"Error running agent {agent.name}: {e}")
            return None

    async def run(
        self,
        prompt: str,
        messages: Optional[List[Message]] = None,
        debug: bool = False,
        interactive: bool = False,
    ) -> str:
        """Execute a task using the swarm of agents.

        Args:
            prompt (str): The main task description for the swarm
            messages (Optional[List[Message]]): Initial messages for context
            debug (bool): Whether to print debug information during execution
            interactive (bool): Whether to open a browser stream

        Returns:
            str: The final aggregated report from the orchestrator
        """
        self.orchestrator.prompt = prompt
        self.orchestrator.messages = messages

        # Initial planning phase
        orchestrator_completion = await self.run_agent_task(
            self.orchestrator, interactive
        )
        self.orchestrator.response_schema = None

        debug_print(debug, orchestrator_completion)

        if not orchestrator_completion or not orchestrator_completion.output:
            return "Failed to create initial plan"

        plan = orchestrator_completion.output

        # Group tasks by priority
        priority_groups = {}
        for assignment in plan.task_assignments:
            priority = assignment.priority
            if priority not in priority_groups:
                priority_groups[priority] = []
            priority_groups[priority].append(assignment)

        # Execute tasks in priority order
        for priority in sorted(priority_groups.keys(), reverse=True):
            debug_print(debug, f"Executing priority {priority} tasks...")
            priority_tasks = []

            # Create tasks for this priority level
            for assignment in priority_groups[priority]:
                target_agent = next(
                    (a for a in self.agents if a.name == assignment.agent_name), None
                )
                if target_agent:
                    target_agent.prompt = assignment.prompt
                    task = asyncio.create_task(self.run_agent_task(target_agent))
                    priority_tasks.append(task)
                    self.running_tasks[target_agent.name] = task

            # Wait for all tasks of this priority to complete before moving to next priority
            await asyncio.gather(*priority_tasks, return_exceptions=True)
            debug_print(debug, f"Completed priority {priority} tasks")

        # Final aggregation phase
        orchestrator_prompt = """
        Based on all the information shared during this task:
        1. Create a comprehensive final report
        2. Include key findings and insights from all agents
        3. Format the report in a clear, readable way using markdown
        """
        orchestrator_message = UserMessage(
            content=[TextPart(type="text", text=orchestrator_prompt)]
        )
        self.orchestrator.messages.append(orchestrator_message)
        final_report = await self.run_agent_task(self.orchestrator)
        return final_report.text if final_report else "Failed to generate final report"
