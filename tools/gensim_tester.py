import gensim.downloader
from argparse import ArgumentParser

def parse_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-m", type=str, required=True)
    args = arg_parser.parse_args()
    return args.m


def main():
    model = parse_args()
    gensim.downloader.load(model)

    while(True):
        word1 = input("Word1: ")
        word2 = input("Word2: ")

        print("Similarity:", model.similarity(word1, word2))

if __name__ == "__main__":
    main()