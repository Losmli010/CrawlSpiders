import os
import random
import threading
import time

import requests
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
CHECK_URL = 'https://www.baidu.com/'

#获取网页
def get_html(url):
    time.sleep(random.randint(1, 3))
    headers = {'User-Agent': USER_AGENT}
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, 'lxml')

#获取西刺代理proxy
def get_xicidaili(html):
    tr_list = html.select('#ip_list tr')
    for tr in tr_list[1:]:
        items = [td.get_text() for td in tr.select('td')]
        proxy = "%s%s%s%s%s" % (items[5].lower(), "://", items[1], ":", items[2])
        yield proxy

#获取快代理proxy
def get_kuaidaili(html):
    tr_list = html.select('table tbody tr')
    for tr in tr_list:
        items = [td.get_text() for td in tr.select('td')]
        proxy = "%s%s%s%s%s" % (items[3].lower(), "://", items[0], ":", items[1])
        yield proxy

#获取proxy
def fetch_proxy():
    proxies = []
    start_urls = ['http://www.xicidaili.com/nn/%d', 'http://www.xicidaili.com/nt/%d']
    for start_url in start_urls:
        for page in range(1, 4):
            url = start_url % page
            html = get_html(url)
            for proxy in get_xicidaili(html):
                proxies.append(proxy)

    start_urls = ['https://www.kuaidaili.com/free/inha/%d/', 'https://www.kuaidaili.com/free/intr/%d/']
    for start_url in start_urls:
        for page in range(1, 4):
            url = start_url % page
            html = get_html(url)
            for proxy in get_kuaidaili(html):
                proxies.append(proxy)
    return proxies

#保存可用proxy
PROXIES = []
lock = threading.Lock()
#检测proxy是否可用
def check_proxy(proxy):
    try:
        if proxy.startswith("https"):
            proxies = {"https": proxy}
            response = requests.get(CHECK_URL, proxies=proxies, timeout=2)
        elif proxy.startswith("http"):
            proxies = {"http": proxy}
            response = requests.get(CHECK_URL, proxies=proxies, timeout=2)
        lock.acquire()
        PROXIES.append(proxy)
        lock.release()
    except:
        pass

#多线程检测
def threading_check(proxies):
    threads = []
    for proxy in proxies:
        t = threading.Thread(target=check_proxy, args=(proxy,))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()

def fetch():
    proxies = fetch_proxy()
    threading_check(proxies)
    with open(os.path.join(BASE_DIR, 'proxies.txt'), 'w', encoding='utf-8') as fp:
        for proxy in PROXIES:
            fp.write(proxy + '\n')