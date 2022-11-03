import networkx as nx

from config import SENSE_EDGES, LEMMA_SENSE_EDGES

def word_to_id(word):
    return f"_{word}"


def create_text_graph():
    graph = nx.Graph()

    with open(LEMMA_SENSE_EDGES, "r") as file:
        lines = file.read().splitlines()
        for line in lines:
            (lemma, sense, edge_type, data) = line.split("\t")

            edge_attributes = {
                "type": edge_type
            }                
            if edge_type == "COMPOUND":
                data= int(data)
            else:
                data = bool(data)

            graph.add_edge(word_to_id(lemma), sense, type=edge_type, data=data)
    
    with open(SENSE_EDGES) as file:
        lines = file.read().splitlines()
        for line in lines:
            (from_sense, to_sense, edge_type, data) = line.split("\t")
            graph.add_edge(from_sense, to_sense, type=edge_type, data=data)
    
    return graph