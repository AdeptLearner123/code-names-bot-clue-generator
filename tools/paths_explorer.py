import json
import time

from code_names_bot_clue_generator.text_graph.text_graph import create_text_digraph, create_test_graph, get_key
from code_names_bot_clue_generator.text_graph.dual_tree_expansion import get_paths, get_paths_old
from code_names_bot_clue_generator.text_graph.path_utils import get_path_str
from config import DICTIONARY, TEXT_SENSES

def get_expansions():
    expansions = input("Expansions [Default 3]:")
    if expansions.isdigit():
        return int(expansions)
    return 3


def print_paths(text_graph, dictionary, text_senses):
    expansions = 2
    word1 = "TORCH"
    word2 = "MELT"
    #expansions = get_expansions()
    #word1 = input("Word 1:")
    #word2 = input("Word 2:")

    start = time.time()
    text_paths = get_paths_old(text_graph, word1, word2, expansions)
    
    for path in text_paths:
        print(get_path_str(path, text_graph, dictionary, text_senses))

    print("Time: ", time.time() - start)
    print("Total paths", len(text_paths))


def main():
    print("Main")
    with open(DICTIONARY, "r") as file:
        dictionary = json.loads(file.read())
    with open(TEXT_SENSES, "r") as file:
        text_senses = json.loads(file.read())

    text_graph = create_text_digraph()

    while(True):
        print_paths(text_graph, dictionary, text_senses)
        break


if __name__ == "__main__":
    main()