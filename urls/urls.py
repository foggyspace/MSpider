class Urls(object):
    '''
    url管理类
    '''
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def has_new_url(self):
        '''
        是否还有未爬取的网页url
        :return:
        '''
        return len(self.new_urls) != 0

    def add_new_url(self, url):
        '''
        添加新的待爬取的url到new_urls集合中
        :param url: 待爬取的url
        :return:
        '''
        if url is None:
            return

        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        '''
        批量添加待爬取的url到new_urls集合中
        :param urls: 待爬取的urls列表
        :return:
        '''
        if urls is None and len(urls) == 0:
            return

        for url in urls:
            self.add_new_url(url)

    def get_new_url(self):
        '''
        从new_urls获取一条待爬取的url链接
        并把它添加至old_urls集合中，表示该url已经爬取过了
        :return:
        '''
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def get_new_urls_size(self):
        '''
        获取待爬取url集合的大小
        :return:
        '''
        return len(self.new_urls)

    def get_old_urls_size(self):
        '''
        获取已经爬取过的url集合的大小
        :return:
        '''
        return len(self.old_urls)
