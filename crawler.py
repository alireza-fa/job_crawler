from abc import ABC, abstractmethod

import requests


class CrawlerBaseByRequests(ABC):
    site_root = ""

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
