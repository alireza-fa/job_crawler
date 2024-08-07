from typing import List

from bs4 import BeautifulSoup

from arbeitnow.data_save import AdvertisementParser
from crawler import CrawlerBaseByRequests, Repository


class ArbeitnowLinkCrawler(CrawlerBaseByRequests):
    site_root = "https://www.arbeitnow.com/"
    search_keyword_format = '?search=%s&tags=%s&sort_by=%s&page=%d'
    search_by_category = 'jobs/%s/' + search_keyword_format

    def __init__(self, repo: Repository, current_page_num: int,
                 skill: str | None = None, sorted_by: str = "relevance",
                 category: str | None = None, tags: List | None = None):
        super().__init__(repo)
        self.current_page_num = current_page_num
        self.category = category
        self.tags = self.get_tags(tags=tags)
        self.sorted_by = sorted_by
        self.skill = skill

    @staticmethod
    def get_tags(tags) -> str:
        if not tags:
            return '[]'

        if len(tags) == 1:
            return '["%s", ""]' % tags[0]

        template = '['

        for i in range(len(tags) - 1):
            template += '"%s",' % tags[i]

        template += '"%s"]' % tags[len(tags) - 1]

        return template

    def get_crawl_link(self):
        link_template = self.site_root

        if self.category:
            link_template += self.search_by_category
            link_template = link_template % (self.category, self.skill, self.tags, self.sorted_by, self.current_page_num)
            self.current_page_num += 1
        else:
            link_template += self.search_keyword_format
            link_template = link_template % (self.skill, self.tags, self.sorted_by, self.current_page_num)
            self.current_page_num += 1

        print(link_template)

        return link_template

    @staticmethod
    def find_links(html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')

        noscript_data = soup.find("noscript")
        all_a_tag = noscript_data.find_all("a", attrs={"class": "flex"})
        if not all_a_tag:
            return []

        old_len, new_len = len(all_a_tag[0].get("href")), len(all_a_tag[0].get("href").replace("page=", ""))
        if old_len > new_len:
            return []

        clean_links = list()

        for a in all_a_tag[:len(all_a_tag)]:
            clean_links.append((a.get("href")))

        return clean_links

    def crawl_links(self) -> List:
        link_list = list()

        while True:
            response = self.get(get_url=self.get_crawl_link())
            new_links = self.find_links(response.text)
            if not new_links:
                return link_list
            link_list.extend(new_links)

    def start(self) -> List:
        links = self.crawl_links()
        self.store(links=links)
        return links

    def store(self, links: List):
        self.repo.save_links(links=links)


class ArbeitnowDataCrawler(CrawlerBaseByRequests):
    def __init__(self, repo: Repository):
        self.parser = AdvertisementParser()
        super().__init__(repo)

    def __load_links(self):
        return self.repo.load_links(flag=False)

    def start(self, link: str | None = None):
        if link:
            response = self.get(get_url=link)
            data = self.parser.parse(response.content)
            self.store(data=data)
            print(data)
            return

        # links = self.__load_links()

        # for link in links:
        #     if not link.flag:
        #         response = self.get(link.url)
        #         if response is not None:
        #             data = self.parser.parse(response.text)
        #             self.store(data)
        #             link.save()

    def store(self, data):
        self.repo.save_data(data=data)
