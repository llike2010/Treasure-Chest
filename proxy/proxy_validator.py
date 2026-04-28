import concurrent.futures
import json
import logging
import urllib.request


def validate_proxy_list(proxy_list, ua_pool, max_workers=5):
    def check(proxy):
        http_proxy = proxy.get("http")
        https_proxy = proxy.get("https") or proxy.get("http(s)")

        if not http_proxy and not https_proxy:
            return None

        ua = ua_pool.get()

        handler = urllib.request.ProxyHandler({
            "http": http_proxy,
            "https": https_proxy
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

            origin_ip = data.get("origin", "")

            # 简单验证IP是否一致
            if http_proxy and origin_ip.startswith(http_proxy.split(":")[0]):
                return proxy
            elif https_proxy and origin_ip.startswith(https_proxy.split(":")[0]):
                return proxy

        except Exception as e:
            logging.debug(f"[ProxyValidator] 代理失效: {proxy} | {e}")

        return None

    logging.info("[ProxyValidator] 开始验证代理")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(check, proxy_list))

    valid_list = [p for p in results if p]

    logging.info(f"[ProxyValidator] 验证完成: {len(valid_list)}/{len(proxy_list)} 可用")

    return valid_list