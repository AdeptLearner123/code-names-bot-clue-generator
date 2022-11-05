import networkx as nx

from config import SENSE_EDGES, LEMMA_SENSE_EDGES

def get_key(item_type, data):
    return f"{item_type}|{data}"

def create_text_graph():
    graph = nx.MultiGraph()

    with open(LEMMA_SENSE_EDGES, "r") as file:
        lines = file.read().splitlines()
        for line in lines:
            (lemma, sense, edge_type, data) = line.split("\t")
            if edge_type == "COMPOUND":
                data= int(data)
            else:
                data = bool(data)

            edge_key = get_key(edge_type, data)
            graph.add_edge(get_key("LEMMA", lemma), get_key("SENSE", sense), key=edge_key)
    
    with open(SENSE_EDGES) as file:
        lines = file.read().splitlines()
        for line in lines:
            (from_sense, to_sense, edge_type, data) = line.split("\t")
            edge_key = get_key(edge_type, data)
            graph.add_edge(get_key("SENSE", from_sense), get_key("SENSE", to_sense), key=edge_key)
    
    return graph


def create_test_graph():
    graph = nx.MultiGraph()
    graph.add_edge("LEMMA|UFO", "SENSE|m_en_gbus1088080.009", key="HAS_SENSE|True")
    graph.add_edge("SENSE|m_en_gbus1088080.009", "SENSE|m_en_gbus0375730.004", key="SYNONYM|")
    graph.add_edge("SENSE|m_en_gbus0375730.004", "SENSE|m_en_gbus1088080.009", key="TEXT|m_en_gbus0375730.004_def:0:5")

    graph.add_edge("LEMMA|ALIEN", "SENSE|m_en_gbus0022530.017", key="HAS_SENSE|False")
    graph.add_edge("SENSE|m_en_gbus0375730.004", "SENSE|m_en_gbus0022530.017", key="TEXT|m_en_gbus0375730.004_def:5:10")
    return graph