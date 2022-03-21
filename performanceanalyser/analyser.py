from abc import ABC, abstractmethod


class Analyser(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def analyse(self):
        pass
