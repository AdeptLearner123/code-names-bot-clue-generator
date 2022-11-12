from .text_graph import get_key

def get_all_shortest_paths_dict(graph, source, cutoff, exclude_types = [], include_types = None):
    queue = [source]
    shortest_paths = dict()
    shortest_paths[source] = [[source]]

    i = 0
    while len(queue) > 0:
        i += 1
        current = queue.pop(0)
        paths = shortest_paths[current]

        if len(paths[0]) == cutoff:
            continue

        for _, out_node in graph.out_edges(current):
            out_node_type = out_node.split("|")[0]
            if out_node_type in exclude_types or include_types is not None and out_node_type not in include_types:
                continue

            out_node_paths = [ path + [out_node] for path in paths ]
            
            if out_node not in shortest_paths:
                shortest_paths[out_node] = out_node_paths
                queue.append(out_node)
            elif len(shortest_paths[out_node][0]) == len(out_node_paths[0]):
                shortest_paths[out_node] += out_node_paths

    return shortest_paths


def get_paths(graph, source_lemma, target_lemma, expansions):
    cutoff = 5 + expansions * 2

    source_id = get_key("LEMMA", source_lemma)
    target_id = get_key("LEMMA", target_lemma)

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

        if len(source_paths[0]) + len(target_paths[0]) - 1 > cutoff:
            continue

        for source_path in source_paths:
            for target_path in target_paths:
                paths.append(source_path + list(reversed(target_path[:-1])))
    
    return paths