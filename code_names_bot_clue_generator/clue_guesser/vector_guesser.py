from .clue_guesser import ClueGuesser

import gensim.downloader

class VectorGuesser(ClueGuesser):
    def __init__(self, model):
        self._vectors = gensim.downloader.load(model)

    def _similarity(self, word1, word2):
        word1 = word1.lower()
        word2 = word2.lower()

        if word1 not in self._vectors.key_to_index or word2 not in self._vectors.key_to_index:
            return 0
        return self._vectors.similarity(word1, word2)


    def guess(self, words, clue, num):
        word_scores = [ (self._similarity(word, clue), word) for word in words ]
        print(word_scores)
        word_scores.sort(reverse=True)

        filtered = word_scores[:num]
        return [ word for _, word in filtered ]


class Word2VecGuesser(VectorGuesser):
    def __init__(self):
        super().__init__("word2vec-google-news-300")