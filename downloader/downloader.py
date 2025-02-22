import time
import logging

import requests
from requests.exceptions import ConnectionError, RequestException, Timeout

from . import _DefaultDownloader

logger = logging.getLogger(__name__)


class DefaultDownloader(_DefaultDownloader):
    '''
    通用的下载器类, 继承自_DefaultDownloader
    '''
    def __init__(self, default_headers=None, default_proxies=None, timeout=10):
        '''
        初始化下载器
        :param default_headers: 默认请求头
        :param default_proxies: 默认代理设置
        :param timeout: 超时时间(秒)
        '''
        self.default_headers = default_headers or {}
        self.default_proxies = default_proxies
        self.timeout = timeout

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
        return self.download(url, headers, proxies, session, retries_number)

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
        if not url:
            raise ValueError("URL不能为空")

        # 合并请求头
        merged_headers = self.default_headers.copy()
        if headers:
            merged_headers.update(headers)

        # 使用指定代理或默认代理
        current_proxies = proxies or self.default_proxies

        try:
            logger.debug(f"正在下载URL: {url}")
            res = requests.get(
                url=url,
                headers=merged_headers,
                proxies=current_proxies,
                timeout=self.timeout
            )
            
            res.raise_for_status()
            logger.debug(f"成功下载URL: {url}")
            return res.text

        except Timeout:
            logger.warning(f"下载超时: {url}")
            if retries_number > 0:
                time.sleep(3)
                return self.download(url, headers, current_proxies, session, retries_number-1)
            raise

        except ConnectionError as e:
            logger.warning(f"连接错误: {url}, 错误信息: {str(e)}")
            if retries_number > 0:
                time.sleep(3)
                return self.download(url, headers, current_proxies, session, retries_number-1)
            raise

        except RequestException as e:
            logger.error(f"请求异常: {url}, 错误信息: {str(e)}")
            if retries_number > 0:
                time.sleep(3)
                return self.download(url, headers, current_proxies, session, retries_number-1)
            raise


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

