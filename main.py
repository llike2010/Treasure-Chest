from config import BASE_URL
from core.crawler import Crawler
from core.requester import Requester
from logger import setup_logger
from proxy.proxy_pool import ProxyPool
from ua.user_agent import UserAgentPool


def main():
    setup_logger()

    # UA池
    ua_pool = UserAgentPool(size=10)
    ua_pool.build_pool()

    # 代理池
    proxy_pool = ProxyPool()
    proxy_pool.build()

    # 请求器
    requester = Requester(proxy_pool, ua_pool)

    crawler = Crawler(requester)

    crawler.crawl(BASE_URL)

if __name__ == "__main__":
    main()