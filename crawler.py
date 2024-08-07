from abc import ABC, abstractmethod
from typing import List

import requests


class Repository(ABC):

    @abstractmethod
    def save_links(self, links: List):
        pass

    @abstractmethod
    def load_links(self, flag: bool | None = False):
        """
        flag = None -> return all links
        flag = False -> return Those links whose data has not yet been crawled
        """
        pass

    def save_data(self, data) -> None:
        """
        :param data: crawling link data.
        :return: None
        """
        pass


class CrawlerBaseByRequests(ABC):
    site_root = ""

    def __init__(self, repo: Repository):
        self.repo = repo

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self, data):
        pass

    @staticmethod
    def get(get_url: str):
        try:
            response_get = requests.get(url=get_url)
            if response_get.status_code == 200:
                return response_get
            raise ValueError()
        except Exception as ex:
            raise ex
