# -*- coding = utf-8 -*-
# 内置库模块
import traceback
import random  # 生成随机数或随机选择
import json  # 处理 JSON 数据，编码/解码 JSON
import time  # 处理时间相关的操作（如延时）
import http.client
import urllib.error  # 处理 URL 请求中的错误
import urllib.parse  # 解析和构建 URL
import urllib.request  # 发起 HTTP 请求
import urllib.robotparser  # 解析 robots.txt 文件，检查爬虫的合法性
from urllib.error import URLError  # 解析请求错误

# 并发执行模块
import concurrent.futures  # 用于多线程和多进程并发操作

# HTML 解析库
from lxml import etree  # 解析 XML 和 HTML 文档，使用 XPath 查找节点
# from bs4 import BeautifulSoup  # 解析 HTML/XML 文档，支持标签查找和选择器

# Selenium 模块，用于浏览器自动化
from selenium.webdriver.chrome.service import Service  # 启动和管理 ChromeDriver 服务
from selenium.webdriver.chrome.options import Options  # 配置 Chrome 浏览器选项
from selenium import webdriver  # 用于启动和控制 Chrome 浏览器实例
from selenium.webdriver.common.by import By  # 查找页面元素的方式，如通过 ID、标签名等
from selenium.webdriver.support.ui import WebDriverWait  # 显式等待，直到某个条件满足为止
from selenium.webdriver.support import expected_conditions as EC  # 提供常用的条件判断，如元素是否可见

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
url = 'https://www.zhihu.com'

# headers
# UserAgent可行性测试
# URL: http://httpbin.org/user-agent
# 这个网站可以检测并显示你的User-Agent字符串，并提供有关其的详细信息。你可以将你的爬虫User-Agent粘贴到这个网站上，查看它被识别为哪种浏览器或设备。
def heads():
    # 系统信息
    system_information = {
        "Windows NT 10.0; Win64; x64": ["Chrome", "Firefox", "Edge"],
        "Windows NT 6.1; Win64; x64": ["Chrome", "Firefox", "Edge"],
        "X11; Linux x86_64": ["Chrome", "Firefox"],
        "Macintosh; Intel Mac OS X 10_15_7": ["Safari", "Chrome"],
        "Macintosh; Intel Mac OS X 10_14_6": ["Safari", "Chrome"],
        "Windows NT 6.3; WOW64": ["Chrome", "Firefox", "Edge"],
        "Macintosh; Intel Mac OS X 10_13_6": ["Safari", "Chrome"]
    }

    # 浏览器内核
    platform = {
        "Chrome": "AppleWebKit/537.36",
        "Safari": "AppleWebKit/605.1.15",
        "Firefox": "Gecko/20100101",
        "Edge": "AppleWebKit/537.36"
    }

    # 平台详细信息
    platform_details = {
        "Chrome": "(KHTML, like Gecko)",
        "Safari": "(KHTML, like WebKit)",
        "Firefox": "",
        "Edge": "(KHTML, like Gecko)"
    }

    # 浏览器版本
    extensions = {
        "Chrome": "Chrome/91.0.4472.124",
        "Safari": "Safari/605.1.15",
        "Firefox": "Firefox/92.0",
        "Edge": "Edge/18.18362"
    }

    # 随机选择系统和相应浏览器
    system = random.choice(list(system_information.keys()))
    browser = random.choice(system_information[system])

    # 构建 User-Agent
    user_agent = (
        "Mozilla/5.0" + " (" + system + ") "
        + platform[browser] + " "
        + platform_details[browser] + " "
        + extensions[browser]
    )

    return {"User-Agent": user_agent}

def validate_user_agents(user_agents):
    def check_user_agent(user_agent):
        print(user_agent)
        url = "https://httpbin.org/user-agent"
        request = urllib.request.Request(url, headers={"User-Agent": user_agent})

        try:
            response = urllib.request.urlopen(request)
            user_agent_info = response.read().decode("utf-8")
            if user_agent in user_agent_info:
                return user_agent
        except Exception as e:
            print(f"检查 User-Agent 时出错: {e}")
            return None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        return list(filter(None, executor.map(check_user_agent, user_agents)))

# ip list
# URL: https://www.kuaidaili.com/free
# 这个网站有免费的国外代理渠道
def send_ip_request(page, user_agent):
    print(f"============= 正在抓取第 {page} 页代理列表 =============")
    base_url = f'https://www.kuaidaili.com/free/fps/{page}'

    # 配置 Selenium 的 Chrome 选项
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')  # 启用无头模式
    chrome_options.add_argument('--disable-gpu')  # 禁用 GPU
    chrome_options.add_argument('--no-sandbox')  # 禁用沙盒模式
    chrome_options.add_argument('--disable-dev-shm-usage')  # 解决共享内存问题
    chrome_options.add_argument('--single-process')  # 只运行一个进程
    chrome_options.add_argument('--disable-software-rasterizer')  # 禁用软件光栅化
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # 防止检测为自动化浏览器
    chrome_options.add_argument('--disable-infobars')  # 禁用信息条

    # 在此处添加 User-Agent
    chrome_options.add_argument(f"user-agent={user_agent}")

    # 指定 ChromeDriver 的路径
    driver_path = r'D:\chromedriver-win64\chromedriver.exe'  # 替换为实际的路径
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 使用 Selenium 加载目标页面
        driver.get(base_url)
        print("页面加载成功")

        # 等待动态内容加载完成
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "table__free-proxy")))

        # 获取页面的 HTML 内容
        data = driver.page_source
        print(f"成功获取页面 HTML 内容")

        return data

    except Exception as e:
        print(f"抓取第 {page} 页代理列表时出错: {e}")
        return None

    finally:
        # 确保浏览器关闭
        driver.quit()

def parse_ip_data(data):
    proxy_list = []
    html_data = etree.HTML(data)
    parse_list = html_data.xpath('//*[@id="table__free-proxy"]/div/table/tbody/tr')

    for tr in parse_list:
        proxies_dict = {
            tr.xpath('./td[4]/text()')[0].lower(): f"{tr.xpath('./td[1]/text()')[0]}:{tr.xpath('./td[2]/text()')[0]}"
        }
        proxy_list.append(proxies_dict)

    return proxy_list

# check the ip
def check_ip(ip_list, verified_user_agents):
    def is_valid_ip(ip):
        http_proxy = ip.get("http")
        https_proxy = ip.get("https") or ip.get("http(s)")

        if not http_proxy and not https_proxy:
            return None

        # 为每个 IP 分配一个独立的 User-Agent
        headers = {"User-Agent": random.choice(verified_user_agents)}

        proxy_handler = urllib.request.ProxyHandler({
            'http': http_proxy,
            'https': https_proxy
        })
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)

        try:
            request = urllib.request.Request("https://httpbin.org/ip", headers=headers)
            response = urllib.request.urlopen(request, timeout=5)
            ip_info = json.loads(response.read().decode('utf-8'))

            if http_proxy and ip_info.get("origin") == http_proxy.split(":")[0]:
                return ip
            elif https_proxy and ip_info.get("origin") == https_proxy.split(":")[0]:
                return ip

        except urllib.error.HTTPError as e:
            if e.code == 400:
                # 输出错误码和响应头
                print(f"HTTP报400错误代码: {e.code} - {e.reason}, 请求头为: {headers}, 响应头为: {e.headers}")
            else:
                # 处理其他 HTTP 错误
                print(f"HTTP 错误: {e.code} - {e.reason}")
            return None

        except urllib.error.URLError as e:
            # 处理 URL 相关的错误（比如连接问题、无法解析主机等）
            print(f"URL 错误: {e.reason}, 请求头为: {headers}")
            return None

        except http.client.BadStatusLine as e:
            print(f"BadStatusLine 错误: {e}, 请求头为: {headers}")
            # 可能的 HTML 响应内容
            return None

        except Exception as e:
            # 处理其他未知错误，输出完整堆栈信息
            print(f"验证 IP 时出错: {e}")
            traceback.print_exc()
            return None

    # 使用 ThreadPoolExecutor 并为每个 IP 进行独立验证
    with concurrent.futures.ThreadPoolExecutor() as executor:
        valid_ips = list(executor.map(is_valid_ip, ip_list))

    # 返回验证通过的 IP 列表
    return [ip for ip in valid_ips if ip is not None]

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

def askURL(url, ip_list, verified_user_agent):
    if not can_fetch(url, verified_user_agent):
        print(f"访问被 robots.txt 禁止: {url}")
        return None

    # 确保传入的 ip_list 是有效的，如果没有代理 IP 就终止请求
    if ip_list:
        proxy = random.choice(ip_list)  # 使用传入的代理 IP 列表中的一个
        proxy_handler = urllib.request.ProxyHandler({'http': proxy.get("http"), 'https': proxy.get("http(s)")})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
    else:
        print("没有可用的代理 IP，终止请求，避免使用本机 IP")
        return None

    # 使用验证过的 User-Agent 构建请求头
    request = urllib.request.Request(url, headers={"User-Agent": verified_user_agent})
    html = ""

    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(f"HTTP 错误: {e.code}")
        if hasattr(e, 'reason'):
            print(f"URL 错误原因: {e.reason}")
    except Exception as e:
        print(f"未知错误: {e}")

    return html

def getData(url, proxy_list, user_agent, retries=3):
    proxy = random.choice(proxy_list)
    proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)

    headers = {
        'User-Agent': user_agent
    }

    request = urllib.request.Request(url, headers=headers)

    for attempt in range(retries):
        try:
            response = urllib.request.urlopen(request, timeout=10)
            return response.read().decode('utf-8')
        except URLError as e:
            print(f"尝试 {attempt + 1}/{retries} 请求失败: {e}")
            time.sleep(2)  # 重试前等待一段时间

    print(f"所有 {retries} 次尝试都失败了")
    return None

if __name__ == '__main__':
    try:
        print("======= 初始化 User-Agent 阶段 =======")
        # 生成多个 User-Agent
        user_agents = [heads()["User-Agent"] for _ in range(10)]  # 可根据需要调整生成的数量

        # 并行验证 User-Agent
        print("======= 验证 User-Agent 阶段开始 =======")
        verified_user_agents = validate_user_agents(user_agents)
        print(f"======= 验证 User-Agent 阶段结束，共验证通过 {len(verified_user_agents)} 个 =======")

        # 确保至少有一个验证通过的 User-Agent
        if not verified_user_agents:
            raise ValueError("没有验证通过的 User-Agent，无法继续执行")

        print("======= 检查 IP 池阶段开始 =======")
        valid_proxy_list = []  # 代理 IP 池

        if not valid_proxy_list:  # IP 池为空时才抓取代理网站
            start_page = 1
            end_page = 3

            print(f"======= 抓取代理列表，页码范围：{start_page} 到 {end_page} =======")

            for page in range(start_page, end_page + 1):
                print(f"正在抓取第 {page} 页的代理列表...")

                # 随机选择一个验证通过的 User-Agent
                selected_user_agent = random.choice(verified_user_agents)

                # 抓取当前页的代理数据
                proxy_data = send_ip_request(page, {"User-Agent": selected_user_agent})

                if proxy_data:
                    # 解析抓取到的代理 IP 列表
                    ip_list = parse_ip_data(proxy_data)
                    print(f"解析出的代理 IP 列表：{ip_list}")

                    if ip_list:
                        # 验证解析出的代理 IP
                        valid_proxy_list.extend(check_ip(ip_list, verified_user_agents))

                        if valid_proxy_list:
                            print(f"找到可用的代理 IP：{valid_proxy_list}")

                    else:
                        print("未能解析出有效的代理 IP，继续下一页...")
                else:
                    print("未能获取当前页的代理数据，继续下一页...")

        print("======= 检查 IP 池阶段结束 =======")
        print(f"当前ip池可用代理为: {valid_proxy_list}")

        if valid_proxy_list:
            print("======= 启动抓取阶段 =======")
            target_url = "https://www.zhihu.com"  # 替换为目标 URL
            result_html = askURL(target_url, valid_proxy_list, random.choice(verified_user_agents))

            if result_html:
                print("成功获取目标页面 HTML 内容")
            else:
                print("获取目标页面 HTML 内容失败")
        else:
            print("未找到可用的代理 IP，无法继续抓取目标网站")

    except Exception as e:
        print(f"程序出现错误: {e}")

