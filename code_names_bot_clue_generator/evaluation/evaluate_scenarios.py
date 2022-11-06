from code_names_bot_clue_generator.clue_guesser.vector_guesser import Word2VecGuesser, GloveNetGuesser
from config import SCENARIOS

import yaml

def main():
    with open(SCENARIOS, "r") as file:
        scenarios = yaml.safe_load(file)
    
    print("Status:", "Loading guesser")
    guesser = GloveNetGuesser()

    print("Status:", "Evaluating")
    correct_scenarios = 0
    total_correct_guesses = 0
    total_clue_num = 0
    for scenario_id, scenario in scenarios.items():
        words = scenario["pos"] + scenario["neg"]
        clue_num = len(scenario["pos"])
        predicted = guesser.guess(words, scenario["clue"], clue_num)
        expected = scenario["pos"]

        correct_guesses = set(predicted).intersection(expected)
        total_correct_guesses += len(correct_guesses)
        total_clue_num += clue_num
        incorrect_guesses = set(predicted).difference(expected)

        if len(incorrect_guesses) > 0:
            print("Incorrect scenario:", scenario_id)
            print("\tWords:", words)
            print("\tClue:", scenario["clue"], clue_num)
            print("\tExpected:", expected)
            print("\tGuessed:", predicted)
        else:
            correct_scenarios += 1
    
    print(f"Scenario accuracy: { correct_scenarios } / { len(scenarios) } = { correct_scenarios / len(scenarios) }")
    print(f"Guess accuracy: { total_correct_guesses } / { total_clue_num } = { total_correct_guesses / total_clue_num }")



if __name__ == "__main__":
    main()