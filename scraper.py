import time
import urllib.request
from typing import List
from typing import Optional

from bs4 import BeautifulSoup


def get_urls(cooldown: Optional[int] = 0) -> List[str]:
    """
    Scrape URLs

    :param cooldown: sleep duration between subsequent requests
    :return: List[str]
    """
    req = urllib.request.Request(
        'http://www.learncpp.com',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    sauce = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(sauce, 'lxml')

    urls = []
    for tutorial in soup.find_all('a'):
        url = tutorial.get('href')
        if url and 'cpp-tutorial' in url:
            if 'http' not in url or 'https' not in url:
                url = "http://www.learncpp.com" + url
            urls.append(url)
        time.sleep(cooldown)

    return urls

