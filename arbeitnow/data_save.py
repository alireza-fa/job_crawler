from bs4 import BeautifulSoup
import requests


def get(get_url: str):
    try:
        response_get = requests.get(get_url)
        if response_get.status_code == 200:
            return response_get
        raise ValueError
    except Exception as ex:
        raise ex


class AdvertisementParser:
    def __init__(self):
        self.soup = None

    @property
    def title(self):
        title_element = self.soup.find("a", attrs={"itemprop": "url"})
        if title_element:
            return title_element.get("title")

    @property
    def tags(self):
        tags = self.soup.find("div", attrs={"class": "hidden sm:flex mt-4 ml-4 sm:col-span-2"})
        if tags:
            tag_buttons = tags.find_all("button")
            tag_list = list()
            for tag in tag_buttons:
                tag_list.append(tag.text.replace("\n", ""))

            return tag_list

    @property
    def salary(self):
        salary_elem = self.soup.find("div", attrs={"title": "Salary Information"})
        if salary_elem:
            return salary_elem.text.replace("Salary Icon", "").replace("\n", "")

    @property
    def company_link(self):
        company_link_elem = self.soup.find("a", attrs={"class": "text-primary-700 font-medium hover:text-primary-800 hover:underline"})
        if company_link_elem:
            return company_link_elem.get("href")

    @property
    def city(self):
        city_elem = self.soup.find("span", attrs={"class": "text-gray-600"})
        if city_elem:
            return city_elem.text

    @property
    def posted_at(self):
        posted_at_elem = self.soup.find("time")
        if posted_at_elem:
            return posted_at_elem.get("datetime")

    @property
    def content(self):
        content_elem = self.soup.find("div", attrs={"itemprop": "description"})
        if content_elem:
            return content_elem.text
        raise ValueError

    def parse(self, html_doc):
        self.soup = BeautifulSoup(html_doc, 'html.parser')

        data = dict(
            title=self.title,
            tags=self.tags,
            salary=self.salary,
            company_link=self.company_link,
            city=self.city,
            posted_at=self.posted_at,
            content=self.content
        )

        return data
