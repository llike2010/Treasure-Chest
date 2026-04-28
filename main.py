from config import BASE_URL
from core.crawler import Crawler
from core.requester import Requester
from logger import setup_logger
from ua.user_agent import UserAgentPool

def main():
    setup_logger()

    ua_pool = UserAgentPool(size=10)
    ua_pool.build_pool()

    requester = Requester(ua_pool)
    crawler = Crawler(requester)

    crawler.crawl(BASE_URL)

if __name__ == "__main__":
    main()