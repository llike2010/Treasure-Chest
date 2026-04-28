import logging
import urllib.request


class Requester:
    def __init__(self, proxy_pool, ua_pool):
        self.proxy_pool = proxy_pool
        self.ua_pool = ua_pool

    def get(self, url):
        proxy = self.proxy_pool.get_proxy()
        ua = self.ua_pool.get()

        if not proxy:
            logging.warning("没有可用代理")
            return None

        handler = urllib.request.ProxyHandler({
            "http": proxy.get("http"),
            "https": proxy.get("https")
        })

        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)

        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua})
            resp = urllib.request.urlopen(req)
            return resp.read().decode("utf-8")

        except Exception as e:
            logging.error(f"请求失败: {e}")
            return None