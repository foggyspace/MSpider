class _DefaultDownloader(object):
    '''
    下载器基础类，包含了以没有具体实现的下载方法
    '''
    def download(self, url=None, headers=None, proxies=None, session=None, retries_number=5):
        '''
        获取网页原内容
        :param url: 网站url, 默认为None
        :param headers: 请求头部, 默认为None
        :param proxies: 代理设置, 默认为None
        :param session: 启用异步下载时, 调用aiohttp.ClientSession对象
        :param retries_number: 最大重试次数, 默认为五次
        :return:
        '''
        raise NotImplementedError
