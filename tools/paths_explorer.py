import json
import time

from code_names_bot_clue_generator.text_graph.text_graph import create_text_digraph, create_test_graph, get_key
from code_names_bot_clue_generator.text_graph.dual_tree_expansion import get_paths
from code_names_bot_clue_generator.text_graph.path_utils import get_path_str
from config import DICTIONARY, TEXT_SENSES

def get_expansions():
    expansions = input("Expansions [Default 3]:")
    if expansions.isdigit():
        return int(expansions)
    return None


def print_paths(text_graph, dictionary, text_senses):
    expansions = get_expansions()
    word1 = input("Word 1:")
    word2 = input("Word 2:")

    start = time.time()
    text_paths, compound_paths = get_paths(text_graph, word1, word2, expansions)
    
    print("TEXT PATHS")
    for source_path, target_path in text_paths:
        print(len(source_path), len(target_path))
        print(get_path_str(source_path, target_path, dictionary, text_senses))
    print("COMPOUD PATHS")
    for source_path, target_path in compound_paths:
        print(get_path_str(source_path, target_path, dictionary, text_senses))

    print("Time: ", time.time() - start)
    print("Total paths", len(text_paths) + len(compound_paths))


def main():
    with open(DICTIONARY, "r") as file:
        dictionary = json.loads(file.read())
    with open(TEXT_SENSES, "r") as file:
        text_senses = json.loads(file.read())

    text_graph = create_text_digraph()

    while(True):
        print_paths(text_graph, dictionary, text_senses)


if __name__ == "__main":
    main()