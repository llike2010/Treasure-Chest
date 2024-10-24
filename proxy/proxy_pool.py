import random
import logging
from proxy.proxy_fetcher import fetch_proxy
from proxy.proxy_validator import validate_proxy
from ua.user_agent import UserAgentPool

class ProxyPool:
    def __init__(self):
        self.proxies = []
        self.ua_pool = UserAgentPool()

    def build(self):
        logging.info("开始构建代理池")

        for page in range(1, 3):
            raw_proxies = fetch_proxy(page)

            for proxy in raw_proxies:
                ua = self.ua_pool.get()
                valid = validate_proxy(proxy, ua)

                if valid:
                    self.proxies.append(valid)

        logging.info(f"代理池构建完成，共 {len(self.proxies)} 个")

    def get_proxy(self):
        if not self.proxies:
            return None
        return random.choice(self.proxies)