import functools
from typing import List

from crawler import Repository


class DummyStorage(Repository):
    links = list()
    data = list()

    def save_links(self, links: List):
        self.links.extend(links)

    def load_links(self, flag=False) -> List:
        return self.links

    def save_data(self, data):
        self.data.append(data)


@functools.cache
def get_dummy_storage() -> DummyStorage:
    return DummyStorage()
