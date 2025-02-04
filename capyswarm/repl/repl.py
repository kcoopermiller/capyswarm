from capyswarm import Swarm


def run_demo_loop(agent, debug=False) -> None:
    client = Swarm()
    print("Starting Baraswarm CLI ₍ᐢ•(ܫ)•ᐢ₎")

    messages = []

    while True:
        user_input = input("\033[90mUser\033[0m: ")

        response = client.run(
            agent=agent,
            messages=user_input,
            debug=debug,
        )

        messages.extend(response.messages)
