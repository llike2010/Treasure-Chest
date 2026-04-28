import logging
import random

from lxml import etree

from proxy.proxy_fetcher import ProxyFetcher
from proxy.proxy_validator import validate_proxy_list
from ua.user_agent import UserAgentPool


class ProxyPool:
    def __init__(self, driver_path):
        self.proxies = []
        self.fetcher = ProxyFetcher(driver_path)
        self.ua_pool = UserAgentPool()

    def parse(self, html):
        proxy_list = []

        tree = etree.HTML(html)
        rows = tree.xpath('//*[@id="table__free-proxy"]/div/table/tbody/tr')

        for row in rows:
            try:
                ip = row.xpath('./td[1]/text()')[0]
                port = row.xpath('./td[2]/text()')[0]
                protocol = row.xpath('./td[4]/text()')[0].lower()

                proxy_list.append({
                    protocol: f"{ip}:{port}"
                })
            except:
                continue

        return proxy_list

    def build(self, pages=2):
        logging.info("[ProxyPool] 开始构建代理池")

        all_proxies = []

        for page in range(1, pages + 1):
            ua = self.ua_pool.get()

            html = self.fetcher.fetch(page, ua)
            if not html:
                continue

            proxy_list = self.parse(html)
            all_proxies.extend(proxy_list)

        logging.info(f"[ProxyPool] 共抓取代理: {len(all_proxies)}")

        # 验证代理
        self.proxies = validate_proxy_list(all_proxies, self.ua_pool)

        logging.info(f"[ProxyPool] 可用代理: {len(self.proxies)}")

    def get_proxy(self):
        if not self.proxies:
            return None
        return random.choice(self.proxies)