import json
from config import TEXT_SENSES
from tqdm import tqdm


def main():
    with open("static/text_senses_(old).json", "r") as file:
        text_senses = json.loads(file.read())

    new_text_senses = dict()
    
    for text_id, entry in tqdm(text_senses.items()):
        combined_senses = []

        senses = entry["senses"]

        if len(senses) == 0:
            continue

        current_sense = senses[0]
        for i in range(1, len(senses)):
            next_sense = senses[i]

            if current_sense["sense"] == next_sense["sense"]:
                current_sense["len"] = next_sense["start"] + next_sense["len"] - current_sense["start"]
            else:
                combined_senses.append(current_sense)
                current_sense = next_sense
        combined_senses.append(current_sense)

        entry["senses"] = combined_senses
        new_text_senses[text_id] = entry

    with open(TEXT_SENSES, "w+") as file:
        file.write(json.dumps(new_text_senses, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()