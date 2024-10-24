import random
import logging
import urllib.request
import concurrent.futures

class UserAgentPool:
    def __init__(self, size=10):
        self.size = size
        self.user_agents = []
        self.valid_user_agents = []

    def generate(self):
        system_information = {
            "Windows NT 10.0; Win64; x64": ["Chrome", "Firefox", "Edge"],
            "X11; Linux x86_64": ["Chrome", "Firefox"],
            "Macintosh; Intel Mac OS X 10_15_7": ["Safari", "Chrome"]
        }

        platform = {
            "Chrome": "AppleWebKit/537.36",
            "Safari": "AppleWebKit/605.1.15",
            "Firefox": "Gecko/20100101",
            "Edge": "AppleWebKit/537.36"
        }

        platform_details = {
            "Chrome": "(KHTML, like Gecko)",
            "Safari": "(KHTML, like WebKit)",
            "Firefox": "",
            "Edge": "(KHTML, like Gecko)"
        }

        extensions = {
            "Chrome": "Chrome/120.0",
            "Safari": "Safari/605.1.15",
            "Firefox": "Firefox/115.0",
            "Edge": "Edg/120.0"
        }

        system = random.choice(list(system_information.keys()))
        browser = random.choice(system_information[system])

        return (
            "Mozilla/5.0" + " (" + system + ") "
            + platform[browser] + " "
            + platform_details[browser] + " "
            + extensions[browser]
        )

    def build_pool(self):
        logging.info("生成 User-Agent 池")

        self.user_agents = [self.generate() for _ in range(self.size)]

        self.valid_user_agents = self.validate(self.user_agents)

        if not self.valid_user_agents:
            raise ValueError("没有可用的 User-Agent")

        logging.info(f"UA池构建完成: {len(self.valid_user_agents)} 个")

    def validate(self, ua_list):
        def check(ua):
            try:
                req = urllib.request.Request(
                    "https://httpbin.org/user-agent",
                    headers={"User-Agent": ua}
                )
                resp = urllib.request.urlopen(req, timeout=3)
                data = resp.read().decode()

                return ua if ua in data else None
            except:
                return None

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(check, ua_list))

        return [ua for ua in results if ua]

    def get(self):
        if not self.valid_user_agents:
            return self.generate()  # fallback
        return random.choice(self.valid_user_agents)