# Basic Examples

This directory contains basic examples of using the Capyswarm library.

### Examples

1. **hackernews.py**

   - Demonstrates how to scrape Hacker News using an Orchestrator and a specialized Agent.
   - **Usage**: Scrapes the top 5 posts from Hacker News.

2. **hn_analysis.py**

    - Demonstrates a hand-off between agents, where one agent collects data and another waits for that data and then analyzes it.
    - **Usage**: Collects and analyzes the top 5 posts from Hacker News.

3. **weather.py**

   - Another demonstration of how to coordinate two agents, where one agent collects data and another waits for that data and then analyzes it.
   - **Usage**: Gets the weather forecast for Tokyo and recommends suitable outdoor activities for the next 3 days.

<details open>
<summary><b>Click to view demo video 📽️</b></summary>
   
[weather.webm](https://github.com/user-attachments/assets/e289d12b-4dae-480b-b324-e5a874c78d77)
   
</details>

4. **hn_mal.py**

   - Demonstrates how to scrape two different websites in parallel in two separate instances using an Orchestrator and two specialized Agents.
   - **Usage**: Scrapes the top 5 posts from Hacker News and the top 5 anime from MyAnimeList.
   - **Note**: This example requires you to have two different Scrapybara instances running before you run the example.

<details open>
<summary><b>Click to view demo video 📽️</b></summary>
   
[hn_mal.webm](https://github.com/user-attachments/assets/1756fdf8-701b-4cd8-9555-055a4d007ad0)

</details>

5. **github_analysis.py**

   - Shows how two agents can collaborate on a shared goal simultaneously, analyzing different aspects of a GitHub repository.
   - **Usage**: Performs a comprehensive analysis of the FastAPI repository with agents sharing insights.
   - **Note**: Doesn't always work as expected.

6. **repl.py (WIP)**

   - Shows how to use context variables within an agent.
   - **Usage**: Demonstrates maintaining state between agent interactions.

## Running the Examples

1. Set up your environment:
   ```bash
   export SCRAPYBARA_API_KEY="your_api_key"
   ```

2. Run the example:
   ```bash
   uv run examples/basic/<example_name>.py
   ```

