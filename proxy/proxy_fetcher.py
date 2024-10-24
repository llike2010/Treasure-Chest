import urllib.request
from lxml import etree
from config import PROXY_SOURCE_URL

def fetch_proxy(page):
    url = PROXY_SOURCE_URL.format(page)
    response = urllib.request.urlopen(url)
    html = response.read().decode("utf-8")

    tree = etree.HTML(html)
    rows = tree.xpath('//*[@id="table__free-proxy"]/div/table/tbody/tr')

    proxies = []

    for row in rows:
        ip = row.xpath('./td[1]/text()')[0]
        port = row.xpath('./td[2]/text()')[0]
        protocol = row.xpath('./td[4]/text()')[0].lower()

        proxies.append({
            protocol: f"{ip}:{port}"
        })

    return proxies