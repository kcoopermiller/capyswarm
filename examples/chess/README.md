# Chess Playing Example

[chess.webm](https://github.com/user-attachments/assets/3ff4119e-0136-4f3c-a5f5-b7c1d831e196)

> [!WARNING]
> This example fails sporadically. It is not yet clear why.

This example demonstrates how two agents can play chess against each other using the [Plain Chess Game](https://plainchess.timwoelfle.de/).

## Running the Example

1. Start an instance of Scrapybara in your dashboard.

2. Open the instance and open up the [Plain Chess Game](https://plainchess.timwoelfle.de/).

3. Copy the instance ID and set it in the `instance` parameter of the `Agent`s.

4. Set up your environment:
   ```bash
   export SCRAPYBARA_API_KEY="your_api_key"
   ```

5. Run the example:
   ```bash
   uv run examples/chess/run.py
   ```
