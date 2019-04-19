import random

from MSpider.MSpider.config.settings import USER_AGENT_LISTS


def get_random_user_agent():
    '''
    随机获取一个user-agent
    :return:
    '''
    return random.choice(USER_AGENT_LISTS)