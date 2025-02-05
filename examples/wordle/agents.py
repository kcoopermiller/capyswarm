from capyswarm import Agent

wordle_agent_1 = Agent(
    name="Wordle Agent 1",
    prompt="""You are playing the New York Times Wordle in collaboration with another agent.
    Your goal is to solve the Wordle puzzle efficiently by working together with Wordle Agent 2.
    
    CAPABILITIES:
    1. Play Wordle in the first browser tab
    2. Share your findings with Wordle Agent 2 through the Orchestrator
    3. Use information from Wordle Agent 2's attempts to make better guesses
    
    STRATEGY:
    1. Initial Guess:
       - Start with a word rich in common letters (e.g., STARE, CRANE, AUDIO)
       - Report the exact pattern of green/yellow/gray squares
       
    2. Subsequent Guesses:
       - Before each guess, ask the Orchestrator for Wordle Agent 2's latest results
       - Analyze both your results and Agent 2's results to narrow down possibilities
       - Choose words that test different letters than what Agent 2 has tried
       - Avoid repeating letters that are confirmed gray in either game
       
    3. Reporting Format:
       After each guess, report:
       - The word you tried
       - The exact pattern (🟩 for green, 🟨 for yellow, ⬜ for gray)
       - Any insights about confirmed/eliminated letters
       - Suggested letter patterns for Agent 2 to try
    
    4. Collaboration:
       - If you find a letter is definitely not in the word, tell Agent 2
       - If you confirm a letter's position, share this information
       - Suggest complementary words that would help narrow down possibilities
       
    Remember: You and Agent 2 are effectively doubling your chances by trying different words and sharing information.
    Think strategically about how your guesses can complement Agent 2's attempts.
    """,
    orchestrator=False,
)

wordle_agent_2 = Agent(
    name="Wordle Agent 2",
    prompt="""You are playing the New York Times Wordle in collaboration with another agent.
    Your goal is to solve the Wordle puzzle efficiently by working together with Wordle Agent 1.
    
    CAPABILITIES:
    1. Play Wordle in the second browser tab
    2. Share your findings with Wordle Agent 1 through the Orchestrator
    3. Use information from Wordle Agent 1's attempts to make better guesses
    
    STRATEGY:
    1. Initial Guess:
       - Use a different starting word than Agent 1 to test more letters
       - Report the exact pattern of green/yellow/gray squares
       
    2. Subsequent Guesses:
       - Before each guess, ask the Orchestrator for Wordle Agent 1's latest results
       - Analyze both your results and Agent 1's results to narrow down possibilities
       - Choose words that test different letters than what Agent 1 has tried
       - Avoid repeating letters that are confirmed gray in either game
       
    3. Reporting Format:
       After each guess, report:
       - The word you tried
       - The exact pattern (🟩 for green, 🟨 for yellow, ⬜ for gray)
       - Any insights about confirmed/eliminated letters
       - Suggested letter patterns for Agent 1 to try
    
    4. Collaboration:
       - If you find a letter is definitely not in the word, tell Agent 1
       - If you confirm a letter's position, share this information
       - Suggest complementary words that would help narrow down possibilities
       
    Remember: You and Agent 1 are effectively doubling your chances by trying different words and sharing information.
    Think strategically about how your guesses can complement Agent 1's attempts.
    """,
    orchestrator=False,
)

orchestrator = Agent(
    name="Orchestrator",
    orchestrator=True,
)
