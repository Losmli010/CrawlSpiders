# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from career.items import CareerItem


class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=500#a']

    base_url = 'https://hr.tencent.com/'

    rules = (
        Rule(LinkExtractor(allow=r'position.php\?&start=\d+#a'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        jobs = response.xpath('//tr[@class="even"]')
        jobs.extend(response.xpath('//tr[@class="odd"]'))
        for job in jobs:
            item = CareerItem()
            item['title'] = job.xpath('./td[1]/a/text()').extract_first()
            item['type'] = job.xpath('./td[2]/text()').extract_first()
            item['num'] = job.xpath('./td[3]/text()').extract_first()
            item['place'] = job.xpath('./td[4]/text()').extract_first()
            item['education'] = ''
            item['work_year'] = ''
            item['update_time'] = job.xpath('./td[5]/text()').extract_first().strip()
            item['detail_url'] = self.base_url + job.xpath('./td[1]/a/@href').extract_first()

            yield Request(item['detail_url'], callback=self.parse_info, meta={'item': item})

    def parse_info(self, response):
        item = response.meta.get('item')
        item['desc'] = ''.join(response.xpath('//table//tr[3]//li/text()').extract())
        item['requirement'] = ''.join(response.xpath('//table//tr[4]//li/text()').extract())
        yield item