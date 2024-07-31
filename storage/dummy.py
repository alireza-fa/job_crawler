import functools
from typing import List

from storage.abstract import Storage


class DummyStorage(Storage):
    links = list()
    data = list()

    def save_links(self, links: List):
        self.links.extend(links)

    def load_links(self, flag=False) -> List:
        return self.links

    def save_data(self, data):
        self.data.append(data)


@functools.cache
def get_dummy_storage() -> Storage:
    return DummyStorage()
