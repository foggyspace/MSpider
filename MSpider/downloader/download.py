import time

import requests
from requests.exceptions import ConnectionError, RequestException

from . import _DefaultDownloader


class DefaultDownloader(_DefaultDownloader):
    '''
    通用的下载器类, 继承自_DefaultDownloader
    '''
    def __call__(self, url=None, headers=None, proxies=None, session=None, retries_number=5):
        '''
        使DefaultDownloader能想方法一样被调用
        :param url: 目标url, 默认为None
        :param headers: 请求头部, 默认为None
        :param proxies: 代理设置, 默认为None
        :param session: 启用异步下载器时调用, aiohttp.ClientSession对象
        :param retries_number: 出错最大重试次数
        :return: res.text
        '''
        try:
            res = requests.get(url=url, headers=headers, timeout=10)
            if res.status_code == 200:
                return res.text
        except (ConnectionError, RequestException) as e:
            time.sleep(3)
            if retries_number > 0:
                return self.download(url, headers, retries_number-1)

    def download(self, url=None, headers=None, proxies=None, session=None, retries_number=5):
        '''
        下载网页源内容
        :param url: 目标url, 默认为None
        :param headers: 请求头部, 默认为None
        :param proxies: 代理设置, 默认为None
        :param session: 启用异步下载器时调用, aiohttp.ClientSession对象
        :param retries_number: 出错最大重试次数
        :return: res.text
        '''
        try:
            res = requests.get(url=url, headers=headers, timeout=10)
            if res.status_code == 200:
                return res.text
        except (ConnectionError, RequestException) as e:
            if retries_number > 0:
                time.sleep(3)
                return self.download(url, headers, retries_number-1)


class AsyncDownloader(_DefaultDownloader):
    '''
    异步下载器类
    '''
    async def __call__(self, url=None, headers=None, proxies=None, session=None, retries_number=5):
        '''
        使AsyncDownloader能想方法一样被调用
        :param url: 目标url, 默认为None
        :param headers: 请求头部, 默认为None
        :param proxies: 代理设置, 默认为None
        :param session: 启用异步下载器时调用, aiohttp.ClientSession对象
        :param retries_number: 出错最大重试次数
        :return: resp.text()
        '''
        async with session.get(url) as resp:
            return await resp.text()

    async def download(self, url=None, headers=None, proxies=None, session=None, retries_number=5):
        '''
        异步获取网页源内容
        :param url: 目标url, 默认为None
        :param headers: 请求头部, 默认为None
        :param proxies: 代理设置, 默认为None
        :param session: 启用异步下载器时调用, aiohttp.ClientSession对象
        :param retries_number: 出错最大重试次数
        :return: resp.text()
        '''
        async with session.get(url) as resp:
            return await resp.text()

