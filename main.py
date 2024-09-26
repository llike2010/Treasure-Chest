# -*- coding = utf-8 -*-
# 内置库模块
import random  # 生成随机数或随机选择
import json  # 处理 JSON 数据，编码/解码 JSON
import time  # 处理时间相关的操作（如延时）
import urllib.error  # 处理 URL 请求中的错误
import urllib.parse  # 解析和构建 URL
import urllib.request  # 发起 HTTP 请求
import urllib.robotparser  # 解析 robots.txt 文件，检查爬虫的合法性

# 并发执行模块
import concurrent.futures  # 用于多线程和多进程并发操作

# HTML 解析库
from lxml import etree  # 解析 XML 和 HTML 文档，使用 XPath 查找节点
from bs4 import BeautifulSoup  # 解析 HTML/XML 文档，支持标签查找和选择器

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


# ip list
# URL: https://www.kuaidaili.com/free
# 这个网站有免费的国外代理渠道
def send_ip_request(page, user_agent):
    print(f"============= 正在抓取第 {page} 页代理列表 =============")
    base_url = f'https://www.kuaidaili.com/free/fps/{page}'

    # 配置 Selenium 的 Edge 选项
    chrome_options = Options()

    # 确保无头模式被启用
    chrome_options.add_argument('--headless=new')  # 新的无头模式参数
    chrome_options.add_argument('--disable-gpu')  # 禁用 GPU，防止渲染问题
    chrome_options.add_argument('--no-sandbox')  # 禁用沙盒模式，避免某些环境问题
    chrome_options.add_argument('--disable-dev-shm-usage')  # 共享内存文件系统问题
    chrome_options.add_argument('--single-process')  # 只运行一个进程
    chrome_options.add_argument('--disable-software-rasterizer')  # 禁用软件光栅化

    # 进一步伪装为普通浏览器
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # 防止检测为自动化浏览器
    chrome_options.add_argument('--disable-infobars')  # 禁用 "Chrome is being controlled by automated software" 信息条
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 防止某些检测

    # 指定 ChromDriver 的路径
    driver_path = r'D:\chromedriver-win64\chromedriver.exe'  # 替换为 EdgeDriver 的路径
    service = Service(executable_path=driver_path)
    driver = webdriver.Edge(service=service, options=chrome_options)

    try:
        # 使用 Selenium 加载目标页面
        driver.get(base_url)
        print("页面加载成功")

        # 等待动态内容加载完成
        # time.sleep(2)
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

#原推荐代码修改，但是目标网站似乎变成了异步同步，改用模拟
# def send_ip_request(page, user_agent):
#     print("=============正在抓取第{}页代理列表===========".format(page))
#     base_url = 'https://www.kuaidaili.com/free/fps/{}'.format(page)
#     # headers = {'User-Agent': user_agent}
#     # 确保打印 headers 信息并显示其格式
#     print(f"爬取代理IP池子所使用的 User-Agent 信息: {user_agent}, 其格式为: {type(user_agent)}")
#     # print(f"完整的 headers 信息: {headers}, 其格式为: {type(headers)}")
#
#     try:
#         # 使用本机IP抓取代理网站，但加上随机生成的User-Agent
#         RpUrl = urllib.request.Request(url=base_url, headers=user_agent)
#         print(f"爬取代理ip池子request函数已生效 信息: {RpUrl}, 其格式为: {type(RpUrl)}")
#
#         response = urllib.request.urlopen(RpUrl)
#         print(f"代理ip池子信息已获得 信息: {response}, 其格式为: {type(response)}")
#
#         data = response.read().decode('utf-8')
#
#         time.sleep(1)  # 避免请求过快
#         print(data)
#         return data
#     except Exception as e:
#         print(f"抓取第{page}页代理列表时出错: {e}")
#         return None


def parse_ip_data(data):
    proxy_list = []

    # 解析HTML数据
    html_data = etree.HTML(data)

    # 定位到包含代理IP信息的table
    parse_list = html_data.xpath('//*[@id="table__free-proxy"]/div/table/tbody/tr')
    print(f"找到 {len(parse_list)} 条代理IP信息")

    for tr in parse_list:
        proxies_dict = {}

        # 提取第1列的IP地址
        ip_num = tr.xpath('./td[1]/text()')[0]

        # 提取第2列的端口号
        port_num = tr.xpath('./td[2]/text()')[0]

        # 提取第4列的HTTP类型
        http_type = tr.xpath('./td[4]/text()')[0]

        # 构建代理字典
        proxies_dict[http_type.lower()] = f"{ip_num}:{port_num}"

        # 将解析的代理信息添加到代理列表中
        proxy_list.append(proxies_dict)

    # 显示解析后的代理列表的长度
    print(f"解析后的代理列表中含有 {len(proxy_list)} 条IP信息")

    return proxy_list


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


def check_user_agent(user_agent):
    url = "https://httpbin.org/user-agent"
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})

    try:
        response = urllib.request.urlopen(request)
        user_agent_info = response.read().decode("utf-8")
        print(f"来自 httpbin.org 的 User-Agent 信息: {user_agent_info}")
        if user_agent in user_agent_info:
            return user_agent  # 返回验证通过的 User-Agent
        return None  # 验证失败
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"URLError: {e.reason}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None


# check the ip
def check_ip(ip_list):
    for i in range(len(ip_list) - 1, -1, -1):  # 逆序遍历列表
        ip = ip_list[i]
        proxy_handler = urllib.request.ProxyHandler({'http': ip.get("http"), 'https': ip.get("https")})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)

        try:
            # 发送 GET 请求，将获取的每个 IP 地址设置为代理
            response = urllib.request.urlopen("https://httpbin.org/ip", timeout=3)
            result = response.read().decode('utf-8')
            ip_info = json.loads(result)

            # 获取 httpbin 返回的 IP
            if ip_info.get("origin") == ip.get("http").split(":")[0]:
                print(f'IP 地址：{ip.get("http")}有效')
            else:
                print(f'IP 地址：{ip.get("http")}无效, 与返回 IP 不匹配')
                ip_list.pop(i)  # 从列表中移除无效IP

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


def askURL(url, ip_list, verified_user_agent):
    if not can_fetch(url, verified_user_agent):
        print(f"访问被 robots.txt 禁止: {url}")
        return None

    # 确保传入的 ip_list 是有效的，如果没有代理 IP 就终止请求
    if ip_list:
        proxy = random.choice(ip_list)  # 使用传入的代理 IP 列表中的一个
        proxy_handler = urllib.request.ProxyHandler({'http': proxy.get("http"), 'https': proxy.get("https")})
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


def getData(url, ip_list, verified_user_agent):
    try:
        html = askURL(url, ip_list, verified_user_agent)  # 传递验证通过的 User-Agent
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
    try:
        print("======= 初始化 User-Agent 阶段 =======")

        # 初始化通过验证的 User-Agent 列表
        verified_user_agents = []

        # 生成多个 User-Agent
        user_agents = [heads()["User-Agent"] for _ in range(5)]  # 可根据需要调整生成的数量

        # 并行验证 User-Agent
        print("======= 验证 User-Agent 阶段开始 =======")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(check_user_agent, ua) for ua in user_agents]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    verified_user_agents.append(result)
        print("======= 验证 User-Agent 阶段结束 =======")

        # 确保至少有一个验证通过的 User-Agent
        if not verified_user_agents:
            raise ValueError("没有验证通过的 User-Agent，无法继续执行")

        print("======= 检查 IP 池阶段开始 =======")
        # 先检查 IP 池是否为空，如果为空则不进行代理网站的抓取
        valid_proxy_list = []  # 代理 IP 池

        if not valid_proxy_list:  # 检查是否已有代理 IP
            # 设置抓取的页码范围，例如 1 到 3 页
            start_page = 1
            end_page = 3

            valid_proxy_list = []

            print(f"======= 抓取代理列表，页码范围：{start_page} 到 {end_page} =======")

            # 遍历 1 到 3 页
            for page in range(start_page, end_page + 1):
                print(f"正在抓取第 {page} 页的代理列表...")

                # 随机选择一个验证通过的 User-Agent
                selected_user_agent = random.choice(verified_user_agents)

                # 调用函数抓取当前页的代理数据
                proxy_data = send_ip_request(page, {"User-Agent": selected_user_agent})

                if proxy_data:
                    # 解析抓取到的代理 IP 列表
                    ip_list = parse_ip_data(proxy_data)
                    print(f"ip池: {ip_list}")

                    if ip_list:
                        # 提取代理列表中的 IP 地址和端口
                        valid_proxy_list = check_ip(ip_list)  # 传递提取的 IP 列表

                        if valid_proxy_list:
                            print(f"找到可用的代理 IP：{valid_proxy_list}")
                            break  # 找到可用的代理 IP，退出循环
                    else:
                        print(f"第 {page} 页未能解析到任何代理 IP")

                # 如果当前页没有获取到代理，继续抓取下一页
                print(f"未能从第 {page} 页找到有效代理，继续下一页...")

            if not valid_proxy_list:
                print("在指定页码范围内未找到任何有效代理 IP")

        print("======= 检查 IP 池阶段结束 =======")

        # 确保有可用的代理 IP
        if valid_proxy_list:
            print("======= 开始抓取数据 =======")
            # 使用有效的代理 IP 和通过验证的 User-Agent 请求数据
            for _ in range(5):  # 可以进行多次数据抓取
                selected_user_agent = random.choice(verified_user_agents)
                data = getData(url, valid_proxy_list)
                print(f"抓取的数据: {data}")
            print("======= 数据抓取结束 =======")
        else:
            print("没有可用的代理 IP，终止抓取操作")

    except ValueError as ve:
        print(f"发生错误 (代码 101): {ve}")
    except Exception as e:
        print(f"发生未知错误 (代码 102): {e}")
    finally:
        print("======= 程序执行完毕 =======")

