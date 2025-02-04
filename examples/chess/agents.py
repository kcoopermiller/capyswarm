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
        
        2. Move pieces by dragging:
           - Move mouse to source: computer(action="mouse_move", coordinate=[x, y])
           - Start drag: computer(action="left_click_drag")
           - Move mouse to target: computer(action="mouse_move", coordinate=[x, y])
           - Release: computer(action="left_click")
        
        Before each move:
        1. Take a screenshot to analyze the position
        2. Plan your move carefully
        3. Execute the move with precise drag coordinates
        4. Take another screenshot to verify the move
        
        Chess Strategy Tips:
        - Control the center (e4, d4, e5, d5)
        - Develop your pieces early
        - Castle for king safety
        - Create and exploit weaknesses
        - Think about pawn structure
        
        End your turn after playing your move.""",
    color=(222, 74, 11),
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
        
        2. Move pieces by dragging:
           - Move mouse to source: computer(action="mouse_move", coordinate=[x, y])
           - Start drag: computer(action="left_click_drag")
           - Move mouse to target: computer(action="mouse_move", coordinate=[x, y])
           - Release: computer(action="left_click")
        
        Before each move:
        1. Take a screenshot to analyze the position
        2. Plan your move carefully
        3. Execute the move with precise drag coordinates
        4. Take another screenshot to verify the move
        
        Chess Strategy Tips:
        - Control the center (e4, d4, e5, d5)
        - Develop your pieces early
        - Castle for king safety
        - Create and exploit weaknesses
        - Think about pawn structure
        
        End your turn after playing your move.""",
    color=(11, 111, 222),
    orchestrator=False,
)

orchestrator = Agent(
    name="Orchestrator",
    color=(146, 11, 222),
    orchestrator=True,
)
