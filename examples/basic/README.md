# Basic Examples

This directory contains basic examples of using the Capyswarm library.

### Examples

1. **hackernews.py**

   - Demonstrates how to scrape Hacker News using an Orchestrator and a specialized Agent.
   - **Usage**: Scrapes the top 5 posts from Hacker News.

2. **hn_mal.py**

   - Demonstrates how to scrape two different websites in parallel using an Orchestrator and two specialized Agents.
   - **Usage**: Scrapes the top 5 posts from Hacker News and the top 5 anime from MyAnimeList.

3. **github_analysis.py**

   - Shows how two agents can collaborate on a shared goal simultaneously, analyzing different aspects of a GitHub repository.
   - **Usage**: Performs a comprehensive analysis of the FastAPI repository with agents sharing insights.

4. **hn_analysis.py**

    - Demonstrates a hand-off between agents, where one agent collects data and another waits for that data and then analyzes it.
    - **Usage**: Collects and analyzes the top 5 posts from Hacker News.

5. **repl.py (WIP)**

   - Shows how to use context variables within an agent.
   - **Usage**: Demonstrates maintaining state between agent interactions.

## Running the Examples

To run any of the examples, you can use the following command:

```shell
uv run examples/basic/<example_name>.py
```

