class Xparse(object):
    '''
    一个类似于接口类型的解析基础类
    '''

    def parse(self, response):
        '''
        解析主调方法
        :param response: 网页源代码
        :return:
        '''
        raise NotImplementedError

    def xpath_lxml(self, response):
        '''
        一个要使用lxml解析库的解析方法
        :param response: 网页源代码
        :return:
        '''
        raise NotImplementedError

    def bs_soup(self, response):
        '''
        一个要用bs4来解析网页的解析方法
        :param response: 网页源代码
        :return:
        '''
        raise NotImplementedError

    def pyquery_selector(self, response):
        '''
        一个要使用Pyquery来解析网页的解析方法
        :param response: 网页员代码
        :return:
        '''
        raise NotImplementedError

    def extract_next_page_link(self, response):
        '''
        获取网页的下一页的链接地址
        :param response: 网页源代码
        :return:
        '''
        raise NotImplementedError

    def _extract_all_links(self, response):
        '''
        获取网页所有的链接地址
        :param response: 网页源代码
        :return:
        '''
        raise NotImplementedError

    def _extract_page_data(self, url=None,response=None):
        '''
        通用的解析方法，也就是用什么解析库都可以
        :param url: 目标url地址
        :param response: 网页源代码
        :return:
        '''
        raise NotImplementedError
