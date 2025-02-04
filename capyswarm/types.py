from typing import List, Callable, Optional, Any, Tuple
from pydantic import BaseModel, Field, model_validator
from scrapybara.anthropic import Anthropic
from scrapybara.prompts import UBUNTU_SYSTEM_PROMPT
from scrapybara.types.act import Message
from .util import pretty_print_step
import random

class Agent(BaseModel):
    """An AI agent that is part of a swarm, capable of executing tasks and communicating with other agents.
    
    Attributes:
        name (str): The agent's identifier, used in communication and task assignment
        instance (Optional[str]): The Scrapybara instance ID this agent uses, defaults to "shared"
        color (Optional[Tuple[int, int, int]]): RGB color tuple for agent's output (r,g,b)
        orchestrator (bool): Whether this agent is the orchestrator (False for worker agents)
        model (Anthropic): The LLM model instance used by this agent
        tools (List[Any]): Tools available to this agent (set by Swarm)
        system (str): System prompt defining the agent's role and capabilities
        prompt (Optional[str]): Current task or instruction for the agent
        messages (Optional[List[Message]]): Agent's conversation history
        response_schema (Optional[Any]): Schema for structured output (used by orchestrator)
        on_step (Optional[Callable]): Callback for processing execution steps
    """
    # Swarm-specific fields
    name: str = "Agent"
    instance: Optional[str] = "shared"  # Track which Scrapybara instance this agent uses
    color: Optional[Tuple[int, int, int]] = Field(
        default_factory=lambda: (
            random.randint(100,255),
            random.randint(100,255),
            random.randint(100,255)
        )
    )
    orchestrator: bool = False
    
    # client.act parameters
    model: Anthropic = Field(default_factory=Anthropic)
    tools: List[Any] = Field(default_factory=list)  # List of tool instances
    system: str = UBUNTU_SYSTEM_PROMPT
    prompt: Optional[str] = None
    messages: Optional[List[Message]] = None  # Agent's conversation history
    response_schema: Optional[Any] = None  # Schema for structured output
    on_step: Optional[Callable] = None
    
    @model_validator(mode='after')
    def setup_defaults(self) -> 'Agent':
        """Set up default on_step function"""
        if self.on_step is None:
            self.on_step = lambda step: pretty_print_step(step, self.name, self.color)
        return self
