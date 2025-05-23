from livingrimoire import Brain, DiHelloWorld, DiSysOut


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    brain = Brain()  # Create your Brain instance
    brain.add_logical_skill(DiHelloWorld())
    brain.hardwareChobit.add_continuous_skill(DiSysOut())
    while True:
        user_input = input("> ")  # Get user input

        if user_input.lower() == "exit":
            print("Exiting program...")
            break

        # Process the input through the brain
        brain.think_default(user_input)
