from .clue_guesser import ClueGuesser

import gensim.downloader

class VectorGuesser(ClueGuesser):
    def __init__(self, model):
        self._vectors = gensim.downloader.load(model)

    def guess(self, words, clue, num):
        word_scores = [ (self._vectors.similarity(word.lower(), clue.lower()), word) for word in words ]
        print(word_scores)
        word_scores.sort(reverse=True)

        filtered = word_scores[:num]
        return [ word for _, word in filtered ]


class Word2VecGuesser(VectorGuesser):
    def __init__(self):
        super().__init__("word2vec-google-news-300")