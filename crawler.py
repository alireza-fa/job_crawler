from abc import ABC, abstractmethod
from typing import Dict

import requests


class Repository(ABC):

    @abstractmethod
    def save_data(self, data: Dict) -> None:
        """
        :param data: crawling link data.
        :return: None
        """
        pass


class AdvertisementParser(ABC):

    def __init__(self):
        self.soup = None

    @abstractmethod
    def parse(self, html_doc):
        pass


class CrawlerBaseByRequests(ABC):
    _site_root = ""

    def __init__(self, repo: Repository, parser: AdvertisementParser, search_keyword: str) -> None:
        self._repo = repo
        self._parser = parser
        self._search_keyword = search_keyword
        self._links = []
        self._advertisements = []

    @abstractmethod
    def _crawl_links(self):
        pass

    def _crawl_data_links(self):
        for link in self._links:
            response = self._get(get_url=link)
            try:
                data = self._parser.parse(response.content)
                self._advertisements.append(data)
                print("crawl data link: %s" % data["advertise_url"])
            except Exception:
                continue

    def _store(self):
        for ad in self._advertisements:
            ad["is_translate"] = False
            ad['pk'] = ad['advertise_url'].split('/')[-1] if ad['advertise_url'] else None
            print(ad)
            self._repo.save_data(data=ad)

    @staticmethod
    def _get(get_url: str):
        response_get = requests.get(url=get_url)
        if response_get.status_code == 200:
            return response_get

        raise Exception("status code is: %d" % response_get.status_code)

    def crawl(self):
        self._crawl_links()
        self._crawl_data_links()
        self._store()
