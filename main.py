# -*- coding = utf-8 -*-
import random
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser

from bs4 import BeautifulSoup

# 1. Wikipedia
# URL: https://en.wikipedia.org/wiki/Main_Page
# Wikipedia有丰富的内容，适合用于测试和练习爬虫技术。
# 2. OpenWeatherMap
# URL: https://openweathermap.org/city/2172797
# 这个链接指向的是悉尼的天气页面，你可以抓取页面上的天气信息。
# 3. IMDB
# URL: https://www.imdb.com/chart/top
# 这个链接指向的是IMDB的电影排行榜页面，你可以抓取电影标题、评分等信息。
# 4. Books to Scrape
# URL: http://books.toscrape.com/
# 这是一个专门为爬虫设计的练习网站，提供了各种书籍的信息，可以自由地练习抓取。
# 5. Quotes to Scrape
# URL: http://quotes.toscrape.com/
# 另一个专门设计供爬虫练习的网站，提供了大量的名人名言数据，非常适合新手练习。
# 6. BBC News
# URL: https://www.bbc.com/news
# BBC新闻主页有大量的新闻文章，可以尝试抓取标题、日期、摘要等信息。

# URL
url = 'https://en.wikipedia.org/wiki/Main_Page'


# ip list
proxy_list = [
    {"http": "http://101.200.127.149:3129"},
    {"http": "http://59.55.162.4:3256"},
    {"http": "http://180.122.147.76:3000"},
    {"http": "http://114.230.107.102:3256"},
    {"http": "http://121.230.211.163:3256"}
]

# headers
# UserAgent可行性测试
# URL: http://httpbin.org/user-agent
# 这个网站可以检测并显示你的User-Agent字符串，并提供有关其的详细信息。你可以将你的爬虫User-Agent粘贴到这个网站上，查看它被识别为哪种浏览器或设备。
def heads():
    system_information = [
        "Windows NT 10.0; Win64; x64",
        "Windows NT 6.1; Win64; x64",
        "X11; Linux x86_64",
        "Macintosh; Intel Mac OS X 10_15_7",
        "Macintosh; Intel Mac OS X 10_14_6",
        "Windows NT 6.3; WOW64",
        "Macintosh; Intel Mac OS X 10_13_6"
    ]

    platform = [
        "Gecko/20100101 Firefox/92.0",
        "AppleWebKit/537.36 Chrome/91.0.4472.124",
        "AppleWebKit/605.1.15 Safari/537.36",
        "Gecko/20100101 Firefox/91.0",
        "AppleWebKit/537.36 Chrome/90.0.4430.212",
        "Gecko/20100101 Firefox/89.0"
    ]

    # noinspection SpellCheckingInspection
    platform_details = [
        " (KHTML, like Gecko) ",
        "",
        " (KHTML, like WebKit) ",
        " (KHTML, like AppleWebKit) "
    ]

    extensions = [
        "Safari/537.36",
        "Safari/605.1.15",
        "",
        "Chrome/91.0.4472.124",
        "Firefox/92.0",
        "Edge/18.18362"
    ]

    head = {
        "User-Agent": "Mozilla/5.0" + " (" + random.choice(system_information) + ") "
                      + random.choice(platform)
                      + random.choice(platform_details)
                      + random.choice(extensions)
    }

    return head


def check_user_agent():
    url = "https://httpbin.org/user-agent"
    request = urllib.request.Request(url, headers=heads())

    try:
        response = urllib.request.urlopen(request)
        print(response.read().decode("utf-8"))

    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} - {e.reason}")

    except urllib.error.URLError as e:
        print(f"URLError: {e.reason}")

    except Exception as e:
        print(f"Unexpected error: {e}")


# check the ip
def check_ip(ip_list):
    for i in range(len(ip_list) - 1, -1, -1):  # 逆序遍历列表
        ip = ip_list[i]
        proxy_handler = urllib.request.ProxyHandler({'http': ip.get("http"), 'https': ip.get("https")})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)

        try:
            # 发送 GET 请求，将获取的每个 IP 地址设置为代理
            response = urllib.request.urlopen("http://httpbin.org/ip", timeout=3)
            print(f'IP 地址：{ip.get("http")}有效')
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            # 失败则输出 IP 地址无效，并从列表中移除
            print(f'IP 地址：{ip.get("http")}无效, 原因: {e}')
            ip_list.pop(i)  # 从列表中移除无效IP

    return ip_list


# Send request to the goal website
# Make sure about the website allows to fetch
def can_fetch(url, user_agent=None):
    if user_agent is None:
        user_agent = heads()["User-Agent"]
    rp = urllib.robotparser.RobotFileParser()

    parsed_url = urllib.parse.urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

    rp.set_url(robots_url)
    rp.read()

    return rp.can_fetch(user_agent, url)


def askURL(url, ip):
    if not can_fetch(url):
        print(f"访问被 robots.txt 禁止: {url}")
        return

    if valid_proxy_list:
        proxy = random.choice(valid_proxy_list)
        proxy_handler = urllib.request.ProxyHandler({'http': proxy.get("http"), 'https': proxy.get("https")})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)

    request = urllib.request.Request(url, headers=heads())
    html = ""

    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")

    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)

    return html


def getData(url, ip):
    try:
        html = askURL(url, ip)
        if not html:
            return []

        time.sleep(2)  # 每次请求后暂停2秒

        datalist = []
        soup = BeautifulSoup(html, 'html.parser')

        # Collect information
        for title in soup.find_all('h1'):
            datalist.append(title.get_text())

        return datalist

    except ConnectionResetError as e:
        print(f"连接重置错误: {e}")
        return []


if __name__ == '__main__':
    # test the head
    # print(heads())
    # print(check_user_agent() == heads())

    valid_proxy_list = check_ip(proxy_list)  # 筛选有效的代理IP
    data = getData(url, valid_proxy_list)  # 使用有效的代理IP请求数据
    print(data)
