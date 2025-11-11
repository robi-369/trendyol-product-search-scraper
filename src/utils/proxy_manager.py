thonimport random

class ProxyManager:
    def __init__(self, proxies):
        self.proxies = proxies
    
    def get_random_proxy(self):
        return random.choice(self.proxies)