from storage.dummy import get_dummy_storage
from arbeitnow.crawler import ArbeitnowLinkCrawler, ArbeitnowDataCrawler


if __name__ == "__main__":
    link_crawler = ArbeitnowLinkCrawler(
        storage=get_dummy_storage(), current_page_num=1, skill="php",
        sorted_by="newest", category="backend", tags=["remote"])

    links = link_crawler.start()

    data_crawler = ArbeitnowDataCrawler(storage=get_dummy_storage())

    for link in links:
        try:
            data_crawler.start(link=link)
        except ValueError:
            # TODO -
            """
            If the ValueError raises, the link is not valid and we delete it 
            or set its flag to true so that it will not be crawled anymore.            
            """
            continue
