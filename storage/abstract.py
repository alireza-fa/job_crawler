from abc import ABC, abstractmethod
from typing import List


class Storage(ABC):

    @abstractmethod
    def save_links(self, links: List):
        pass

    @abstractmethod
    def load_links(self, flag=False) -> List:
        pass

    @abstractmethod
    def save_data(self, data):
        pass
