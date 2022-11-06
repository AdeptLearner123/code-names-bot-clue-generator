from argparse import ArgumentParser
import json
import time

from code_names_bot_clue_generator.text_graph.text_graph import create_text_digraph, create_test_graph, get_key
from code_names_bot_clue_generator.text_graph.dual_tree_expansion import get_paths
from code_names_bot_clue_generator.text_graph.path_utils import get_path_str
from config import DICTIONARY, TEXT_SENSES

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-s", action="store_true")
    args = parser.parse_args()
    return args.s


def print_paths(text_graph, dictionary, text_senses):
    word1 = input("Word 1:")
    word2 = input("Word 2:")

    start = time.time()
    paths = get_paths(text_graph, word1, word2)
    for source_path, target_path in paths:
        print(get_path_str(source_path, target_path, dictionary, text_senses))
    print("Time: ", time.time() - start)
    print("Total paths", len(paths))


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