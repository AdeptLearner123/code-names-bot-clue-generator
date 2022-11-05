from argparse import ArgumentParser
import networkx as nx
import json

from code_names_bot_clue_generator.text_graph.text_graph import create_text_graph, create_test_graph, get_key
from code_names_bot_clue_generator.text_graph.path_utils import get_path_str
from config import DICTIONARY, TEXT_SENSES

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-s", action="store_true")
    args = parser.parse_args()
    return args.s


def get_paths(text_graph, dictionary, text_senses):
    word1 = input("Word 1:")
    word2 = input("Word 2:")

    source_key = get_key("LEMMA", word1)
    target_key = get_key("LEMMA", word2)
    shortest_only = parse_args()

    cutoff = 5
    if shortest_only:
        cutoff = nx.shortest_path_length(text_graph, source_key, target_key)

    paths = nx.all_simple_edge_paths(text_graph, get_key("LEMMA", word1), get_key("LEMMA", word2), cutoff)

    for path in paths:
        print(get_path_str(path, dictionary, text_senses))


def main():
    with open(DICTIONARY, "r") as file:
        dictionary = json.loads(file.read())
    with open(TEXT_SENSES, "r") as file:
        text_senses = json.loads(file.read())

    text_graph = create_text_graph()

    while(True):
        get_paths(text_graph, dictionary, text_senses)


if __name__ == "__main":
    main()