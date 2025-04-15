from .configs import PROXY_LIST


class ProxyRotator:
    def __init__(self, proxies: list[str], start=0):
        self.proxies = proxies
        self.index = start

    def get_proxy(self):
        if not self.proxies:
            return None

        proxy = self.proxies[self.index]
        print("proxy: " + proxy)
        self.rotate()
        return proxy

    def rotate(self):
        self.index = (self.index + 1) % len(self.proxies)

    def get_proxies(self):
        proxy = self.get_proxy()

        if not proxy:
            return None

        return {
            "http://": proxy,
            "https://": proxy,
        }


proxy = ProxyRotator(proxies=PROXY_LIST)
