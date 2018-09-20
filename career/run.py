import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import defer, reactor

from career.spiders.baidu import BaiduSpider
from career.spiders.alibaba import AlibabaSpider
from career.spiders.tencent import TencentSpider

# def main():
    # process = CrawlerProcess()
    # process.crawl(BaiduSpider)
    # process.crawl(AlibabaSpider)
    # process.start()

settings = get_project_settings()
configure_logging(settings)
runner = CrawlerRunner(settings)

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(BaiduSpider)
    yield runner.crawl(AlibabaSpider)
    yield runner.crawl(TencentSpider)
    reactor.stop()

if __name__ == '__main__':
    crawl()
    reactor.run()