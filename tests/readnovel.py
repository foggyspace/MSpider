from pprint import pprint
from urllib.parse import urljoin

from pyquery import PyQuery as pq

from MSpider.MSpider.downloader.download import DefaultDownloader
from MSpider.MSpider.urls import Urls
from MSpider.MSpider.xparse import Xparse
from MSpider.MSpider.config.settings import DEFAULT_USER_AGENT
from MSpider.MSpider.utils.fsave import ItemFile


class SaveMethods(ItemFile):
    def save_to_json(self, filename, source_data):
        data = self.dumps_json(source_data)
        with open(filename, 'a') as fd:
            print(f'save data ...')
            fd.write(data)
            print(f'save data success.')


class Parser(Xparse):
    def parse(self, response):
        data = self._extract_page_data(response=response)
        return data

    def _extract_page_data(self, url=None,response=None):
        if response is None:
            return

        books = []

        books_dict = {}

        doc = pq(response)

        book_list = doc('div.right-book-list ul li').items()

        for node in book_list:
            img_src = node.find('div.book-img a img').attr('src')
            book_info = node.find('div.book-info p.intro').text()
            book_name = node.find('div.book-info h3 a').text()
            book_link = node.find('div.book-info h3 a').attr('href')
            author = node.find('h4 a.default').text()
            story_type = node.find('p.tag span.org').text()
            status = node.find('p.tag span.red').text()
            word_number = node.find('p.tag span.blue').text()

            books_dict['author'] = author
            books_dict['story_type'] = story_type
            books_dict['book_name'] = book_name
            books_dict['book_link'] = urljoin('https://www.readnovel.com/', book_link)
            books_dict['book_img'] = img_src
            books_dict['book_status'] = status
            books_dict['word_number'] = word_number
            books_dict['info'] = book_info

            books.append(books_dict)

        return books


class Spider(object):
    def __init__(self):
        self.download = DefaultDownloader()
        self.urls = Urls()
        self.parse = Parser()
        self.filename = 'readnovel.json'
        self.save_file = SaveMethods()

    def crawl(self, url):
        self.urls.add_new_url(url)
        while self.urls.has_new_url() and self.urls.get_old_urls_size() < 100:
            try:
                new_url = self.urls.get_new_url()
                response = self.download.download(new_url, DEFAULT_USER_AGENT)
                data = self.parse.parse(response)
                pprint(data)
                self.save_file.save_to_json(self.filename, data)
            except Exception as e:
                print(f'[*] crawl exception {e}')


def main():
    spider = Spider()
    base_url = 'https://www.readnovel.com/finish?pageSize=10&gender=2&catId=-1&isFinish=1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum={}'
    urls = [base_url.format(page) for page in range(1, 101)]
    for url in urls:
        print(f'[*] start crawl => {url}')
        spider.crawl(url)



if __name__ == '__main__':
    main()
