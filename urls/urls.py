from urllib.parse import urlparse
from queue import PriorityQueue
import re
import json

class Urls(object):
    '''
    url管理类
    '''
    def __init__(self, config_file=None):
        self.new_urls = PriorityQueue()
        self.old_urls = set()
        self.url_filters = []
        self.config = self._load_config(config_file) if config_file else {}

    def _load_config(self, config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f'加载配置文件失败: {e}')
            return {}

    def _is_valid_url(self, url):
        '''
        验证URL格式是否有效
        :param url: 待验证的URL
        :return: bool
        '''
        if not url:
            return False
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def _apply_filters(self, url):
        '''
        应用URL过滤规则
        :param url: 待过滤的URL
        :return: bool
        '''
        for pattern in self.url_filters:
            if re.match(pattern, url):
                return False
        return True

    def add_filter(self, pattern):
        '''
        添加URL过滤规则
        :param pattern: 正则表达式模式
        '''
        if pattern and isinstance(pattern, str):
            self.url_filters.append(pattern)

    def has_new_url(self):
        '''
        是否还有未爬取的网页url
        :return: bool
        '''
        return not self.new_urls.empty()

    def add_new_url(self, url, priority=0):
        '''
        添加新的待爬取的url到new_urls队列中
        :param url: 待爬取的url
        :param priority: 优先级(数字越小优先级越高)
        :return:
        '''
        try:
            if not self._is_valid_url(url):
                print(f'无效的URL格式: {url}')
                return

            if not self._apply_filters(url):
                print(f'URL被过滤规则拦截: {url}')
                return

            if url not in self.old_urls:
                self.new_urls.put((priority, url))
        except Exception as e:
            print(f'添加URL时发生错误: {e}')

    def add_new_urls(self, urls, priority=0):
        '''
        批量添加待爬取的url到new_urls队列中
        :param urls: 待爬取的urls列表
        :param priority: 优先级(数字越小优先级越高)
        :return:
        '''
        if not urls:
            return

        for url in urls:
            self.add_new_url(url, priority)

    def get_new_url(self):
        '''
        从new_urls获取一条待爬取的url链接
        并把它添加至old_urls集合中，表示该url已经爬取过了
        :return: str
        '''
        try:
            if not self.has_new_url():
                return None
            _, new_url = self.new_urls.get()
            self.old_urls.add(new_url)
            return new_url
        except Exception as e:
            print(f'获取URL时发生错误: {e}')
            return None

    def get_new_urls_size(self):
        '''
        获取待爬取url队列的大小
        :return: int
        '''
        return self.new_urls.qsize()

    def get_old_urls_size(self):
        '''
        获取已经爬取过的url集合的大小
        :return: int
        '''
        return len(self.old_urls)

    def save_progress(self, file_path):
        '''
        保存爬取进度
        :param file_path: 保存文件路径
        '''
        try:
            data = {
                'old_urls': list(self.old_urls)
            }
            with open(file_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f'保存进度时发生错误: {e}')

    def load_progress(self, file_path):
        '''
        加载爬取进度
        :param file_path: 进度文件路径
        '''
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.old_urls = set(data.get('old_urls', []))
        except Exception as e:
            print(f'加载进度时发生错误: {e}')
