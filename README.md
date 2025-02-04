<div id="toc" align="center">
  <ul style="list-style: none">
    <summary>
      <h1>
        <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/5c96e78f-b3ea-4714-beaf-e2afcfc1a405" width="30" >
        <img src="https://github.com/user-attachments/assets/5f5de974-b6a2-41c3-bf0a-46a308432698" width="30"> 
        </picture>
        Capyswarm
        <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/04379257-2e36-4e09-b084-65257f132eac" width="30" >
        <img src="https://github.com/user-attachments/assets/5dcddbc6-215b-48d4-ab32-16f2437b5d9f" alt="Scrapybara" width="30">
        </picture>
      </h1>
    </summary>
  </ul>
</div>

<p align="center">
  A lightweight multi-agent orchestration framework for Scrapybara computer-use agents built on top of OpenAI's <a href="https://github.com/openai/swarm">Swarm</a>
</p>
<p align="center">
  <a href="https://github.com/kcoopermiller/baraswarm/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://discord.gg/s4bPUVFXqA"><img alt="Discord" src="https://img.shields.io/badge/Discord-Join%20the%20community-yellow.svg?logo=discord" /></a>
</p>

> [!NOTE]
> This is a work in progress and is not yet ready for production use. Also, while the API is similar to OpenAI's Swarm, the underlying implementation has been almost entirely rewritten.

## Install

Requires Python 3.12+

```shell
pip install git+ssh://git@github.com/kcoopermiller/capyswarm.git
```

or

```shell
pip install git+https://github.com/kcoopermiller/capyswarm.git
```

## Usage

```python
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
```

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)
- [Documentation (WIP)](#documentation)
  - [Swarm](#swarm)
  - [Agents](#agents)
  - [Tools](#tools)
- [Evaluations](#evaluations)
- [Roadmap](#roadmap)

# Overview

Swarm focuses on making agent **coordination** and **execution** lightweight, highly controllable, and easily testable.

In the OpenAI Swarm framework, this is achieved through two core abstractions: `Agent`s and **handoffs**. An `Agent` encompasses `instructions` and `tools`, and can at any point choose to hand off a conversation to another `Agent`. Handoffs occur synchronously, ensuring controlled transitions between agents.

Capyswarm introduces an **orchestrator-worker** architecture. Instead of direct agent-to-agent handoffs, all task delegation is routed through a central `Orchestrator`. The `Orchestrator` decomposes high-level tasks, assigns subtasks to individual agents, and manages asynchronous execution. Agents can still transfer tasks to others, but only via the orchestrator, ensuring structured coordination.

Additionally, agents can retrieve relevant information about each other's progress, enabling more informed decision-making. Once all assigned tasks are completed, the Orchestrator aggregates the results and determines whether the user's request has been successfully fulfilled.

All interactions between the user and agents are mediated by the `Orchestrator`, maintaining a streamlined and coherent workflow.

![Swarm Diagram](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F8985fc683fae4780fb34eab1365ab78c7e51bc8e-2401x1000.png&w=3840&q=75)  
*Image source: [Building effective agents](https://www.anthropic.com/research/building-effective-agents)*

# Examples

Check out `/examples` for inspiration! Learn more about each one in its README.

- [`basic`](examples/basic): Simple examples of fundamentals like setup, function calling, handoffs, and context variables
- [`fireboy_watergirl`](examples/fireboy_watergirl): An example of two agents playing [Fireboy and Watergirl](https://www.coolmathgames.com/0-fireboy-and-water-girl-in-the-forest-temple)

# Documentation

> [!IMPORTANT]
> This section is a work in progress and is mostly copied from the OpenAI Swarm docs.

## Swarm

Start by instantiating a Swarm client (which internally instantiates a `Scrapybara` client).

```python
from capyswarm import Swarm

client = Swarm()
```

### `client.run()`

Swarm's `run()` function is analogous to the `client.act()` function in the [Scrapybara Act SDK](https://docs.scrapybara.com/act-sdk) – it takes a `model` that serves as the base LLM for the agent, `tools` that enable agents to interact with the computer, a `prompt` that should denote the agent’s current objective, and starts an interaction loop that continues until the agent achieves the user's objective.

At its core, Swarm's `client.run()` implements the following loop: TODO

#### Arguments

| Argument              | Type    | Description                                                                                                                                            | Default        |
| --------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------- |
| **agent**             | `Agent` | The (initial) agent to be called.                                                                                                                      | (required)     |
| **prompt**            | `str`   | Objective                                                                                                                                              | (required)     |
| **debug**             | `bool`  | If `True`, enables debug logging                                                                                                                       | `False`        |



**OUTDATED**

Once `client.run()` is finished (after potentially multiple calls to agents and tools) it will return a `Response` containing all the relevant updated state. Specifically, the new `messages`, the last `Agent` to be called, and the most up-to-date `context_variables`. You can pass these values (plus new user messages) in to your next execution of `client.run()` to continue the interaction where it left off – much like `chat.completions.create()`. (The `run_demo_loop` function implements an example of a full execution loop in `/swarm/repl/repl.py`.)

#### `Response` Fields

| Field                 | Type    | Description                                                                                                                                                                                                                                                                  |
| --------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **messages**          | `List`  | A list of message objects generated during the conversation. Very similar to [Chat Completions `messages`](https://platform.openai.com/docs/api-reference/chat/create#chat-create-messages), but with a `sender` field indicating which `Agent` the message originated from. |
| **agent**             | `Agent` | The last agent to handle a message.                                                                                                                                                                                                                                          |
| **context_variables** | `dict`  | The same as the input variables, plus any changes.                                                                                                                                                                                                                           |

**OUTDATED_END**

## Agents

```python
from capyswarm import Agent

agent = Agent(
   
)
```

An `Agent` simply encapsulates a set of `instructions` with a set of `functions` (plus some additional settings below), and has the capability to hand off execution to another `Agent`.

While it's tempting to personify an `Agent` as "someone who does X", it can also be used to represent a very specific workflow or step defined by a set of `instructions` and `functions` (e.g. a set of steps, a complex retrieval, single step of data transformation, etc). This allows `Agent`s to be composed into a network of "agents", "workflows", and "tasks", all represented by the same primitive.

## `Agent` Fields

| Field            | Type                             | Description                                                                   | Default                                          |
| ---------------- | -------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------ |
| **name**         | `str`                            | The name of the agent.                                                        | `"Agent"`                                        |
| **instance**     | `str`                            | The Scrapybara instance this agent uses.                                      | `"shared"`                                       |
| **color**        | `str`                            | Terminal Color                                                                | `random.choice(["91","92","93","94","95","96"])` |
| **orchestrator** | `bool`                           | True if this agent is orchestrator                                            | `False`                                          |
| **model**        | `scrapybara.anthropic.Anthropic` | The model to be used by the agent.                                            | `scrapybara.anthropic.Anthropic`                 |
| **tool**         | `list`                           | List of tools available to agent                                              | check [_setup_agent_tools](https://github.com/kcoopermiller/baraswarm/blob/main/swarm/core.py#L75)                                                                                                                 |
| **system**        | `str`                           | System prompt                                                                 | `scrapybara.prompts.UBUNTU_SYSTEM_PROMPT`        |
| **prompt**        | `str`                           | Description of preferred Agent objective                                      | `None`                                           |
| **messages**      | `List`                          | A list of `scrapybara.types.act.Message` objects                              | `None`                                           |
| **schema**        | `Any`                           | [Structured output](https://docs.scrapybara.com/act-sdk#structured-output)    | `None`                                           |
| **on_step**       | `Callable`                      | What to print after one iteration                                             | [pretty_print_step](https://github.com/kcoopermiller/baraswarm/blob/main/swarm/util.py#L4) |


TODO:
- explain fields better

## Tools

# Evaluations

TODO: create example evals. Check `weather_agent` and `triage_agent` in OpenAI Swarm for example

# Roadmap

- [ ] Add more examples / benchmarks
- [ ] Add more documentation
- [ ] Custom Response object
- [ ] Give Orchestrator ability to create Agents