def item_key_to_string(item_key, dictionary, text_senses):
    item_type, item_data = item_key.split("|")

    if item_type == "LEMMA":
        return item_data
    elif item_type == "SENSE":
        entry = dictionary[item_data]
        return f"{entry['lemma']}.{entry['pos']}"
    elif item_type == "COMPOUND":
        return "In Compound"
    elif item_type == "HAS_SENSE":
        return "Has Sense"
    elif item_type == "TEXT":
        (text_id, start, end) = item_data.split(":")
        return text_senses[text_id]["text"]
    elif item_type == "SYNONYM":
        return "Synonym"
    elif item_type == "CLASS":
        return "Class"
    elif item_type == "DOMAIN":
        return "Domain"

def get_path_str(path, dictionary, text_senses):
    path_items = []
    for edge_tuple in path:
        (node1, node2, edge_key) = edge_tuple

        if len(path_items) == 0:
            path_items.append(node1)
        
        path_items.append(edge_key)
        path_items.append(node2)
    
    path_items = [ item_key_to_string(item_key, dictionary, text_senses) for item_key in path_items ]
    return " -- ".join(path_items)