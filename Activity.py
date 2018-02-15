from abc import ABC, abstractmethod


class Activity(ABC):
    @abstractmethod
    def first_query(self, bot, update):
        pass

    @abstractmethod
    def process(self, query, bot, update):
        pass
