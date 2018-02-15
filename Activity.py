from abc import ABC, abstractmethod


class Activity(ABC):
    @abstractmethod
    def process(self, query):
        pass
