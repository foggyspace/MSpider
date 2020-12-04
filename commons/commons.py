import random

from config.settings import USER_AGENT_LISTS, DEFAULT_PROXIES_LISTS


def get_random_user_agent():
    '''
    随机获取一个user-agent
    :return:
    '''
    return random.choice(USER_AGENT_LISTS)


def get_random_proxies():
    '''
    获取一个随机的默认代理IP地址
    :return:
    '''
    return random.choice(DEFAULT_PROXIES_LISTS)
