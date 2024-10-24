import logging
import time
import random

class Crawler:
    def __init__(self, requester):
        self.requester = requester

    def crawl(self, url):
        logging.info(f"开始抓取: {url}")

        html = self.requester.get(url)

        if html:
            logging.info("抓取成功")
        else:
            logging.warning("抓取失败")

        # 限速
        time.sleep(random.uniform(1, 2))

        return html