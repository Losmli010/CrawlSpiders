import os
import random

from scrapy import signals

from career.fetchproxy import fetch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class RandomProxyMiddleware(object):
    def __init__(self, settings):
        self.proxies = []
        self.update_proxy()
        # self.get_proxy()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if 'proxy' in request.meta:
            return

        req = self.change_proxy(request)
        # request.meta['dont_filter'] = True

    def process_response(self, request, response, spider):
        if response.status != 200 and 'proxy' in request.meta:
            self.del_proxy(request)

            return self.change_proxy(request)
        return response

    def process_exception(self, request, exception, spider):
        self.del_proxy(request)
        return self.change_proxy(request)

    def change_proxy(self, request):
        if len(self.proxies) < 1:
            self.update_proxy()
        proxy = self.proxies.pop()
        request.meta['proxy'] = proxy
        print('Now proxy is', proxy)
        return request

    def del_proxy(self, request):
        del request.meta['proxy']

    def get_proxy(self):
        with open(os.path.join(BASE_DIR, 'proxies.txt'), 'r') as fp:
            self.proxies = [line.strip() for line in fp]

    def update_proxy(self):
        fetch()
        self.get_proxy()