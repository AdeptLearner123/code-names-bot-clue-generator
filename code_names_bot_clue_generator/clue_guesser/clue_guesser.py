from abc import ABC, abstractmethod

class ClueGuesser(ABC):
    @abstractmethod
    def guess(self, words, clue, num):
        pass