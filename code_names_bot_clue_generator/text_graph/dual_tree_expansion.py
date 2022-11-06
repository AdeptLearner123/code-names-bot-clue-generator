import networkx as nx

from .text_graph import get_key

MAX_EXPANSIONS = 3

def get_all_shortest_paths_dict(graph, source, cutoff):
    queue = [source]
    shortest_paths = dict()
    shortest_paths[source] = [[source]]

    while len(queue) > 0:
        current = queue.pop(0)
        paths = shortest_paths[current]

        if len(paths[0]) == cutoff:
            continue

        for _, out_node in graph.out_edges(current):
            out_node_paths = [ path + [out_node] for path in paths ]
            
            if out_node not in shortest_paths:
                shortest_paths[out_node] = out_node_paths
                queue.append(out_node)
            elif len(shortest_paths[out_node][0]) == len(out_node_paths[0]):
                shortest_paths[out_node] += out_node_paths

    return shortest_paths


def get_paths(graph, source_lemma, target_lemma):
    source_id = get_key("LEMMA", source_lemma)
    target_id = get_key("LEMMA", target_lemma)

    cutoff = 1 + MAX_EXPANSIONS * 2
    source_paths_dict = get_all_shortest_paths_dict(graph, source_id, cutoff)
    target_paths_dict = get_all_shortest_paths_dict(graph, target_id, cutoff)

    paths = []

    for node_key in source_paths_dict.keys():
        node_type, _ = node_key.split("|")

        if node_type != "SENSE":
            continue

        if node_key not in target_paths_dict:
            continue

        source_paths = source_paths_dict[node_key]
        target_paths = target_paths_dict[node_key]
        source_expansions = (len(source_paths[0]) - 2) // 2
        target_expansions = (len(target_paths[0]) - 2) // 2

        if source_expansions + target_expansions > MAX_EXPANSIONS:
            continue

        for source_path in source_paths:
            for target_path in target_paths:
                paths.append((source_path, target_path))
    
    return paths