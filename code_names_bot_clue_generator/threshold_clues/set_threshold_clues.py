from config import DICTIONARY, CARDWORDS, THRESHOLD_CLUES

import json
from collections import defaultdict

VALID_POS = set(["noun", "proper"])

def select_entry(entries):
    for i, entry in enumerate(entries):
        print(f"[{i}]: {entry['lemma']} -- {entry['definition']}")
    
    idx = int(input("Select entry:"))
    return entries[idx]


def get_cardword_threshold_clue_old(cardword, lemma_to_entries, class_to_entries):
    entries = lemma_to_entries[cardword]

    if len(entries) == 1:
        entry = entries[0]
    else:
        entry = select_entry(entries)
    
    semantic_class = entry["classes"][0]
    print("Semantic class", semantic_class)

    class_entry = select_entry(class_to_entries[semantic_class])
    return class_entry["lemma"]


def get_lemma_class_to_entries(dictionary):
    lemma_to_entries = defaultdict(lambda: [])
    class_to_entries = defaultdict(lambda: [])
    for entry in dictionary.values():
        if entry["meta"]["is_primary"] and entry["pos"] in VALID_POS:
            lemma_to_entries[entry["lemma"].upper()].append(entry)

            if " " not in entry["lemma"]:
                for semantic_class in entry["classes"]:
                    class_to_entries[semantic_class].append(entry)
    return lemma_to_entries, class_to_entries


def main():
    with open(CARDWORDS, "r") as file:
        cardwords = file.read().splitlines()
    
    with open(DICTIONARY, "r") as file:
        dictionary = json.loads(file.read())

    with open(THRESHOLD_CLUES, "r") as file:
        threshold_clues = json.loads(file.read())

    print("Status:", "Create lemma to entries")
    lemma_to_entries, class_to_entries = get_lemma_class_to_entries(dictionary)

    missing_cardwords = set(cardwords).difference(set(threshold_clues.keys()))
    missing_cardwords = sorted(list(missing_cardwords))

    print("Total: ", len(missing_cardwords), "/", len(cardwords))
    for i, cardword in enumerate(missing_cardwords):
        if cardword in threshold_clues:
            continue

        print("Cardword: ", cardword, i, "/", len(missing_cardwords))
        #threshold_clues[cardword] = get_cardword_threshold_clue(cardword, lemma_to_entries, class_to_entries)

        clue = input("Threshold clue: ")
        threshold_clues[cardword] = clue

        if clue not in threshold_clues:
            threshold_clues[clue] = cardword

        with open(THRESHOLD_CLUES, "w") as file:
            file.write(json.dumps(threshold_clues, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()