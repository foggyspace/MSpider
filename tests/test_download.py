from downloader.downloader import DefaultDownloader, AsyncDownloader
from config.settings import DEFAULT_USER_AGENT


def test_default_downloader():
    default_downloader = DefaultDownloader()

    url = 'https://www.python.org'

    assert default_downloader.download(url, DEFAULT_USER_AGENT)

    print('pass')



def test_async_downloader():
    async_downloader = AsyncDownloader()

    url = 'https://www.python.org'

    assert async_downloader.download(url)


if __name__ == '__main__':
    test_default_downloader()
    # test_async_downloader()
