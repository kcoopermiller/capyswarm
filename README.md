<div id="toc" align="center">
  <ul style="list-style: none">
    <summary>
      <h1>
        <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/06a6476f-6a97-402d-bcc5-5d8d6e1fab17" width="30" >
        <img src="https://github.com/user-attachments/assets/4808459b-bbf8-40a6-9e94-a56dd37c7d0c" width="30"> 
        </picture>
        Capyswarm
        <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/61a94a9d-51e2-486c-adb9-c1afa23f29f1" width="30" >
        <img src="https://github.com/user-attachments/assets/fee4b43a-3010-4d0a-b265-60b39d18adc8" alt="Scrapybara" width="30">
        </picture>
      </h1>
    </summary>
  </ul>
</div>

<p align="center">
  A lightweight multi-agent orchestration framework for Scrapybara computer-use agents
</p>
<p align="center">
  <a href="https://github.com/kcoopermiller/baraswarm/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://discord.gg/s4bPUVFXqA"><img alt="Discord" src="https://img.shields.io/badge/Discord-Join%20the%20community-yellow.svg?logo=discord" /></a>
</p>

> [!NOTE]
> This is a work in progress and is not yet ready for production use. Also, while the API is similar to [OpenAI's Swarm](https://github.com/openai/swarm) and was initially a fork of the framework, the underlying implementation has been almost entirely rewritten.

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
        await swarm.run(
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
- [Evaluations](#evaluations)
- [Roadmap](#roadmap) 

# Overview

Swarm focuses on making agent **coordination** and **execution** lightweight, highly controllable, and easily testable.

In the OpenAI Swarm framework, this is achieved through two core abstractions: `Agent`s and **handoffs**. An `Agent` encompasses `instructions` and `tools`, and can at any point choose to hand off a conversation to another `Agent`. Handoffs occur synchronously, ensuring controlled transitions between agents.

Capyswarm introduces an **orchestrator-worker** architecture, drawing inspiration from Anthropic's [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents). Instead of direct agent-to-agent handoffs, all task delegation is routed through a central `Orchestrator`. The `Orchestrator` decomposes high-level tasks, assigns subtasks to individual agents, and manages asynchronous execution. Agents can still transfer tasks to others, but only via the orchestrator, ensuring structured coordination.

Additionally, agents can retrieve relevant information about each other's progress, enabling more informed decision-making. Once all assigned tasks are completed, the Orchestrator aggregates the results and determines whether the user's request has been successfully fulfilled.

All interactions between the user and agents are mediated by the `Orchestrator`, maintaining a streamlined and coherent workflow.

# Examples

Check out `/examples` for inspiration! Learn more about each one in its README.

- [`basic`](examples/basic): Simple examples of fundamentals
- [`chess`](examples/chess): An example of two agents playing [Chess](https://plainchess.timwoelfle.de/)

# Documentation

> [!IMPORTANT]
> This section is a work in progress.

## Swarm

Start by instantiating a Swarm client (which internally instantiates a `Scrapybara` client).

```python
from capyswarm import Swarm
...
client = Swarm(agents, api_key)
```

### `client.run()`

Swarm's `run()` function is analogous to the `client.act()` function in the [Scrapybara Act SDK](https://docs.scrapybara.com/act-sdk) – it takes a `prompt` that should denote the agent's current objective, and starts an interaction loop between the `Agent`s that continues until they achieve the user's objective.

#### Arguments

| Argument              | Type    | Description                                                                                                                                            | Default        |
| --------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------- |
| **prompt**            | `str`   | The main task description for the swarm                                                                                                                | (required)     |
| **messages**          | `List[Message]` | Initial messages for context                                                                                                                   | `None`         |
| **debug**             | `bool`  | If `True`, enables debug logging                                                                                                                       | `False`        |
| **interactive**       | `bool`  | If `True`, opens a browser stream                                                                                                                      | `False`        |

## Agents

```python
from capyswarm import Agent

agent = Agent()
```

There are two main types of agents:

- **Worker Agents**: Specialize in performing focused tasks such as web data extraction, code analysis, data processing, etc.
- **Orchestrator Agent**: Manages the overall task by delegating subtasks to workers, coordinating their interactions, and aggregating results. Only one agent in the swarm should have this role.

### `Agent` Fields

| Field               | Type                             | Description                                                                   | Default                                          |
| ------------------- | -------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------ |
| **name**            | `str`                            | The name of the agent                                                         | `"Agent"`                                        |
| **instance**        | `str`                            | The Scrapybara instance ID this agent uses                                    | `"shared"`                                       |
| **instance_type**   | `Literal["ubuntu", "windows", "browser"]` | The type of instance to use                                         | `"ubuntu"`                                       |
| **color**           | `Tuple[int, int, int]`           | RGB color tuple for agent's output (r,g,b)                                    | random `Tuple` of rgb values                     |
| **orchestrator**    | `bool`                           | True if this agent is orchestrator                                            | `False`                                          |
| **model**           | `scrapybara.anthropic.Anthropic` | The model to be used by the agent                                            | `scrapybara.anthropic.Anthropic`                 |
| **tools**           | `List[Any]`                      | List of tools available to agent                                              | Default tools based on instance type             |
| **system**          | `Optional[str]`                  | System prompt (if None, uses default based on instance_type)                  | `None`                                           |
| **prompt**          | `Optional[str]`                  | Description of preferred Agent objective                                      | `None`                                           |
| **messages**        | `Optional[List[Message]]`        | A list of `scrapybara.types.act.Message` objects                             | `None`                                           |
| **response_schema** | `Optional[Any]`                  | [Structured output](https://docs.scrapybara.com/act-sdk#structured-output)    | `None`                                           |
| **on_step**         | `Optional[Callable]`             | What to print after one iteration                                             | [pretty_print_step](https://github.com/kcoopermiller/baraswarm/blob/main/swarm/util.py#L4) |

### Using Agents in a Swarm

Agents work together by joining a Swarm. Typically, you have one orchestrator managing multiple worker agents.

Here's a high-level overview of the workflow:

1. The **Orchestrator Agent** receives the main task and generates an overall plan by decomposing it into subtasks, each tailored to a specific worker agent.
2. The assigned tasks are grouped by priority levels. Tasks sharing the same priority are executed as asynchronous coroutines concurrently, ensuring that resource-intensive or dependent tasks are coordinated seamlessly.
3. As each worker agent completes its task, the results are logged. The orchestrator waits for all higher-priority tasks to finish before proceeding with lower-priority tasks.
4. Finally, the orchestrator aggregates all agent outputs into a comprehensive final report, which is then returned to the user.

# Evaluations

TODO: create example evals. Check `weather_agent` and `triage_agent` in OpenAI Swarm for example

# Roadmap

- [ ] Priority lists are currently bugged and the swarm will fail if the length is greater than 2
- [ ] Add more examples / benchmarks
- [ ] Add more documentation and visualizations
- [ ] Custom Response object
- [ ] Give Orchestrator ability to create Agents
- [ ] Rework the prompts. Currently they get overwritten or merged at odd times.
