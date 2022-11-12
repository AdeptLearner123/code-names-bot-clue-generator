from .text_graph import get_key
from .paths_matcher import match_paths
from collections import defaultdict

MAX_EXPANSIONS = 3

def get_outward_paths_dict(graph, source, expansions):
    rules = [
        {
            "node_types": ["COMPOUND", "HAS_SENSE"],
            "out_only": True
        },
        {
            "node_types": ["SENSE"],
            "out_only": True
        },
        {
            "node_types": ["SENSE", "TEXT", "CLASS", "DOMAIN"],
            "out_only": True,
            "min_times": 0,
            "max_times": expansions * 2
        }
    ]

    paths = match_paths(graph, source, rules, cutoff = 3 + expansions * 2)

    paths_dict = defaultdict(lambda: [])
    for path in paths:
        paths_dict[path[-1]].append(path)
    
    return paths_dict


def get_paths(graph, source_lemma, target_lemma, expansions):
    source_id = get_key("LEMMA", source_lemma)
    target_id = get_key("LEMMA", target_lemma)

    source_paths_dict = get_outward_paths_dict(graph, source_id, expansions)
    target_paths_dict = get_outward_paths_dict(graph, target_id, expansions)

    paths = []
    cutoff = 5 + expansions * 2

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
                paths.append(source_path + target_path[1:])
    
    return paths


def get_paths(graph, source_lemma, target_lemma, expansions = None):
    rules = [
        {
            "node_types": ["COMPOUND", "HAS_SENSE"],
            "out_only": True
        },
        {
            "node_types": ["SENSE"],
            "out_only": True
        },
        {
            "node_types": ["SENSE", "TEXT", "CLASS", "DOMAIN"],
            "out_only": True,
            "min_times": 0,
            "max_times": expansions * 2
        },
        {
            "node_types": ["SENSE", "TEXT", "CLASS", "DOMAIN"],
            "in_only": True,
            "min_times": 0,
            "max_times": expansions * 2
        },
        {
            "node_types": ["COMPOUND", "HAS_SENSE"],
            "in_only": True
        },
        {
            "node_types": ["LEMMA"],
            "in_only": True
        }
    ]

    source_id = get_key("LEMMA", source_lemma)
    target_id = get_key("LEMMA", target_lemma)
    return match_paths(graph, source_id, rules, target_id, 5 + expansions * 2)


def get_all_shortest_paths_dict_old(graph, source, cutoff, exclude_types = [], include_types = None):
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
    print("iterations", i)

    return shortest_paths


def get_paths_old(graph, source_lemma, target_lemma, expansions):
    cutoff = 5 + expansions * 2

    source_id = get_key("LEMMA", source_lemma)
    target_id = get_key("LEMMA", target_lemma)

    source_paths_dict = get_all_shortest_paths_dict_old(graph, source_id, cutoff)
    target_paths_dict = get_all_shortest_paths_dict_old(graph, target_id, cutoff)

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
    
    print("Paths", paths)
    return paths