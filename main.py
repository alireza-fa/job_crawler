from arbeitnow.crawler import ArbeitnowCrawler
from storage.dummy import DummyStorage
from arbeitnow.data_save import AdvertisementParser


if __name__ == "__main__":
    crawler = ArbeitnowCrawler(
        repo=DummyStorage(),
        parser=AdvertisementParser(),
        search_keyword="django")

    # setter
    # crawler.set_current_page_num(1)
    # crawler.set_sorted_by("newest")
    # crawler.set_category("backend")
    # crawler.set_tags(["remote"])

    crawler.crawl()
