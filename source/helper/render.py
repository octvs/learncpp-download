import logging
import os
import sys
import time
from typing import Optional

import pdfkit
import ray
from helper import scraper


class Render:
    download_path = 'downloads'

    def __init__(self, cooldown: Optional[int] = 0) -> None:
        self.urls = scraper.get_urls(cooldown)[:20]
        self.make_download_dir()

    def make_download_dir(self) -> None:
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    @staticmethod
    def progress(count: int, total: int, status: Optional[str] = '') -> None:
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        sys.stdout.flush()


class WkRender(Render):
    options = {
        'cookie': [('ezCMPCookieConsent', '-1=1|1=1|2=1|3=1|4=1')],
        'disable-javascript': None,
        'page-size': 'A4',
        'margin-top': '0',
        'margin-bottom': '0',
        'margin-left': '0',
        'margin-right': '0'
    }

    def __init__(self) -> None:
        super().__init__()
        self.cooldown = 0

    def set_cooldown(self, cooldown: int):
        self.cooldown = cooldown

    def download(self):
        futures = []
        for it, url in enumerate(self.urls):
            logging.info(f'Downloading: {url}')
            futures.append(ray_download.remote(1 + it, url))
            Render.progress(it, len(self.urls))
            time.sleep(self.cooldown)

        ray.get(futures)


@ray.remote
def ray_download(sno: int, url: str) -> None:
    filename = Render.download_path \
               + '/' \
               + str(sno).zfill(3) \
               + '-' \
               + url.split('/')[-2] \
               + '.pdf'

    try:
        pdfkit.from_url(url, filename, options=WkRender.options)
    except Exception as e:
        logging.error(f'unable to download: {url}')
        logging.exception(e)


logging.basicConfig(
    level=logging.WARN,
    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'
)

