from argparse import ArgumentParser
from config import TEXT_SENSES, DICTIONARY

import json

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("text_id")
    args = parser.parse_args()
    return args.text_id


def main():
    with open(TEXT_SENSES, "r") as file:
        text_senses_dict = json.loads(file.read())
    
    with open(DICTIONARY, "r") as file:
        dictionary = json.loads(file.read())

    text_id = parse_args()

    text_senses = text_senses_dict[text_id]
    text = text_senses["text"]
    print(text)
    for sense in text_senses["senses"]:
        sense_id = sense["sense"]
        start = int(sense["start"])
        length = int(sense["len"])
        print(sense_id, text[start : start + length], dictionary[sense_id]["definition"])



if __name__ == "__main__":
    main()