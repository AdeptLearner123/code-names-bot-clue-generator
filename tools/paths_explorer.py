import networkx as nx

from code_names_bot_clue_generator.text_graph.text_graph import create_text_graph, word_to_id

def main():
    text_graph = create_text_graph()
    word1 = input("Word 1:")
    word2 = input("Word 2:")

    paths = nx.all_simple_paths(text_graph, word_to_id(word1), word_to_id(word2), 3)
    print([ path for path in paths ])


if __name__ == "__main":
    main()