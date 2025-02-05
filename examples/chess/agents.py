from capyswarm import Agent

white = Agent(
    name="White",
    prompt="""You are playing chess as White. Your goal is to play strong moves and win the game.
        
        Your capabilities:
        - Take screenshots to analyze the position:
           1. computer(action="screenshot")
           2. Use this to see Black's last move
           3. Analyze the current position
           4. Plan your response
        
        - Move pieces by clicking:
           1. Move mouse to source 
           2. left click on the source 
           3. move mouse to target (there will be dark circles on the board where the piece can move) 
           4. left click on the target
        
        Before each move:
        1. Take a screenshot to analyze the position
        2. Plan your move carefully
        3. Execute the move with precise click coordinates
        4. Take another screenshot to verify the move
        
        End your turn after playing your move.""",
    instance="s-64af29cf",  # example, replace with your own instance
    orchestrator=False,
)

black = Agent(
    name="Black",
    prompt="""You are playing chess as Black. Your goal is to play strong moves and win the game.
        
        Some of your key capabilities:
        - Take screenshots to analyze the position:
           1. computer(action="screenshot")
           2. Use this to see White's last move
           3. Analyze the current position
           4. Plan your response
        
        - Move pieces by clicking:
           1. Move mouse to source 
           2. left click on the source 
           3. move mouse to target (there will be dark circles on the board where the piece can move) 
           4. left click on the target
        
        Before each move:
        1. Take a screenshot to analyze the position
        2. Plan your move carefully
        3. Execute the move with precise click coordinates
        4. Take another screenshot to verify the move
        
        End your turn after playing your move.""",
    instance="s-64af29cf",
    orchestrator=False,
)

orchestrator = Agent(
    name="Orchestrator",
    instance="s-64af29cf",
    orchestrator=True,
)
