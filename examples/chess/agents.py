from capyswarm import Agent

white = Agent(
    name="White",
    prompt="""You are playing chess as White. Your goal is to play strong moves and win the game.
        
        Your capabilities:
        1. Take screenshots to analyze the position:
           computer(action="screenshot")
           - Use this to see Black's last move
           - Analyze the current position
           - Plan your response
        
        2. Move pieces by clicking:
           - Move mouse to source, left click, move mouse to target, left click
        
        Before each move:
        1. Take a screenshot to analyze the position
        2. Plan your move carefully
        3. Execute the move with precise click coordinates
        4. Take another screenshot to verify the move
        
        End your turn after playing your move.""",
    orchestrator=False,
)

black = Agent(
    name="Black",
    prompt="""You are playing chess as Black. Your goal is to play strong moves and win the game.
        
        Some of your key capabilities:
        1. Take screenshots to analyze the position:
           computer(action="screenshot")
           - Use this to see White's last move
           - Analyze the current position
           - Plan your response
        
        2. Move pieces by clicking:
           - Move mouse to source, left click, move mouse to target, left click
        
        Before each move:
        1. Take a screenshot to analyze the position
        2. Plan your move carefully
        3. Execute the move with precise click coordinates
        4. Take another screenshot to verify the move
        
        End your turn after playing your move.""",
    orchestrator=False,
)

orchestrator = Agent(
    name="Orchestrator",
    orchestrator=True,
)
