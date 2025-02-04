import asyncio
from pydantic import BaseModel, Field
from typing import Any, List, Optional, Tuple, Sequence
from scrapybara.tools import Tool
from scrapybara.client import UbuntuInstance
from scrapybara.instance.types import Action, Command
from scrapybara.types.act import UserMessage, TextPart
from scrapybara.client import AsyncBaseInstance, AsyncUbuntuInstance

class OrchestratorSchema(BaseModel):
    """The orchestrator's structured plan for task distribution"""
    class TaskAssignment(BaseModel):
        agent_name: str
        prompt: str
        priority: int = 1  # Higher number = higher priority
    overall_task: str  # The original task being broken down
    task_assignments: List[TaskAssignment]  # List of assignments for each agent
    execution_notes: str  # Any additional notes about task execution or coordination

class InspectAgentParameters(BaseModel):
    """Parameters for inspecting an agent's work"""
    agent_name: str  # Name of the agent to inspect

class InspectAgentTool(Tool):
    """Tool for orchestrator to inspect an agent's work history"""
    _instance: UbuntuInstance
    _agent: Any  # Reference to the orchestrator
    _swarm: Any  # Reference to the swarm instance
    _loop: asyncio.AbstractEventLoop

    def __init__(self, instance: UbuntuInstance, agent: Any, swarm: Any) -> None:
        if not agent.orchestrator:
            raise ValueError("InspectAgentTool is only available to the orchestrator")
            
        super().__init__(
            name="inspect_agent",
            description="Check an agent's work history to see what they've done or find specific information.",
            parameters=InspectAgentParameters,
        )
        self._instance = instance
        self._agent = agent
        self._swarm = swarm
        self._loop = asyncio.get_running_loop()

    def __call__(self, **kwargs: Any) -> Any:
        future = asyncio.run_coroutine_threadsafe(
            self._async_call(**kwargs), self._loop
        )
        return future.result()

    async def _async_call(self, **kwargs: Any) -> Any:
        params = InspectAgentParameters(**kwargs)
        
        # Find the target agent
        target_agent = next(
            (a for a in self._swarm.agents if a.name == params.agent_name),
            None
        )
        
        if not target_agent:
            raise ValueError(f"Agent {params.agent_name} not found")
            
        # Get agent's work history
        history = {
            "agent_name": target_agent.name,
            "current_prompt": target_agent.prompt,
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content
                }
                for msg in target_agent.messages
            ],
            "steps": target_agent.steps
        }
        
        return history

class CommunicateParameters(BaseModel):
    """Parameters for agent communication"""
    message: str  # The message content

class CommunicateTool(Tool):
    """Tool for agents to communicate with the orchestrator"""
    _instance: UbuntuInstance
    _agent: Any  # Reference to the current agent
    _swarm: Any  # Reference to the swarm instance
    _loop: asyncio.AbstractEventLoop

    def __init__(self, instance: UbuntuInstance, agent: Any, swarm: Any) -> None:
        if agent.orchestrator:
            raise ValueError("CommunicateTool is only available to non-orchestrator agents")
            
        super().__init__(
            name="communicate",
            description="Send a message to the Orchestrator to share information, request assistance, or provide updates.",
            parameters=CommunicateParameters,
        )
        self._instance = instance
        self._agent = agent
        self._swarm = swarm
        self._loop = asyncio.get_running_loop()

    def __call__(self, **kwargs: Any) -> Any:
        future = asyncio.run_coroutine_threadsafe(
            self._async_call(**kwargs), self._loop
        )
        return future.result()

    async def _async_call(self, **kwargs: Any) -> Any:
        params = CommunicateParameters(**kwargs)
        
        # Create message for orchestrator as a user message
        agent_message = UserMessage(
            content=[
                TextPart(
                    type="text",
                    text=f"[{self._agent.name}] {params.message}"
                )
            ]
        )
            
        self._swarm.orchestrator.messages.append(agent_message)
        
        response = await self._swarm.run_agent_task(self._swarm.orchestrator)
        
        if not response:
            raise ValueError("Failed to get response from orchestrator")
            
        return {
            "from_agent": self._agent.name,
            "to_agent": "Orchestrator",
            "message": params.message,
            "orchestrator_response": response.text if response.text else "No response from orchestrator"
        }
    
class AsyncBashToolParameters(BaseModel):
    command: str = Field(description="The bash command to execute")
    restart: Optional[bool] = Field(False, description="Whether to restart the shell")

class AsyncBashTool(Tool):
    _instance: AsyncUbuntuInstance
    _loop: asyncio.AbstractEventLoop

    def __init__(self, instance: AsyncUbuntuInstance) -> None:
        super().__init__(
            name="bash",
            description="Execute bash commands in the shell",
            parameters=AsyncBashToolParameters,
        )
        self._instance = instance
        # Save the current (main) event loop for later use.
        self._loop = asyncio.get_running_loop()

    def __call__(self, **kwargs: Any) -> Any:
        # Schedule the asynchronous call on the stored (main) event loop.
        future = asyncio.run_coroutine_threadsafe(
            self._async_call(**kwargs), self._loop
        )
        return future.result()

    async def _async_call(self, **kwargs: Any) -> Any:
        params = AsyncBashToolParameters.model_validate(kwargs)
        result = await self._instance.bash(command=params.command, restart=params.restart)
        return result 

class AsyncComputerToolParameters(BaseModel):
    """Parameters for computer interaction commands."""
    action: Action = Field(description="The computer action to execute")
    coordinate: Optional[Sequence[int]] = Field(None, description="Coordinates for mouse actions")
    text: Optional[str] = Field(None, description="Text for keyboard actions")

class AsyncComputerTool(Tool):
    _instance: AsyncBaseInstance
    _loop: asyncio.AbstractEventLoop

    def __init__(self, instance: AsyncBaseInstance) -> None:
        super().__init__(
            name="computer",
            description="Control mouse and keyboard for computer interaction",
            parameters=AsyncComputerToolParameters,
        )
        self._instance = instance
        self._loop = asyncio.get_running_loop()

    def __call__(self, **kwargs: Any) -> Any:
        future = asyncio.run_coroutine_threadsafe(
            self._async_call(**kwargs), self._loop
        )
        return future.result()

    async def _async_call(self, **kwargs: Any) -> Any:
        params = AsyncComputerToolParameters.model_validate(kwargs)
        result = await self._instance.computer(
            action=params.action,
            coordinate=tuple(params.coordinate) if params.coordinate else None,
            text=params.text,
        )
        return result 

class AsyncEditToolParameters(BaseModel):
    """Parameters for file editing commands."""
    command: Command = Field(description="The edit command to execute")
    path: str = Field(description="Path to the file to edit")
    file_text: Optional[str] = Field(None, description="File content for create command")
    view_range: Optional[Tuple[int, int]] = Field(None, description="Line range for view command")
    old_str: Optional[str] = Field(None, description="String to replace for replace command")
    new_str: Optional[str] = Field(None, description="New string for replace command")
    insert_line: Optional[int] = Field(None, description="Line number for insert command")

class AsyncEditTool(Tool):
    _instance: AsyncUbuntuInstance
    _loop: asyncio.AbstractEventLoop

    def __init__(self, instance: AsyncUbuntuInstance) -> None:
        super().__init__(
            name="str_replace_editor",
            description="View, create, and edit files in the filesystem",
            parameters=AsyncEditToolParameters,
        )
        self._instance = instance
        self._loop = asyncio.get_running_loop()

    def __call__(self, **kwargs: Any) -> Any:
        future = asyncio.run_coroutine_threadsafe(
            self._async_call(**kwargs), self._loop
        )
        return future.result()

    async def _async_call(self, **kwargs: Any) -> Any:
        params = AsyncEditToolParameters.model_validate(kwargs)
        result = await self._instance.edit(
            command=params.command,
            path=params.path,
            file_text=params.file_text,
            view_range=params.view_range,
            old_str=params.old_str,
            new_str=params.new_str,
            insert_line=params.insert_line,
        )
        return result 