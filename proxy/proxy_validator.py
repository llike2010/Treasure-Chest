import urllib.request
import json

def validate_proxy(proxy, ua):
    handler = urllib.request.ProxyHandler({
        "http": proxy.get("http"),
        "https": proxy.get("https")
    })

    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)

    try:
        req = urllib.request.Request(
            "https://httpbin.org/ip",
            headers={"User-Agent": ua}
        )
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read().decode())

        return proxy if data else None

    except:
        return None