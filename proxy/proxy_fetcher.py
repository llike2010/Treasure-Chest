import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ProxyFetcher:
    def __init__(self, driver_path):
        self.driver_path = driver_path

    def fetch(self, page, user_agent):
        url = f"https://www.kuaidaili.com/free/fps/{page}"
        logging.info(f"[ProxyFetcher] 抓取第 {page} 页代理")

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(f"user-agent={user_agent}")

        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.get(url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "table__free-proxy"))
            )

            html = driver.page_source
            logging.info("[ProxyFetcher] 页面获取成功")

            return html

        except Exception as e:
            logging.error(f"[ProxyFetcher] 抓取失败: {e}")
            return None

        finally:
            driver.quit()