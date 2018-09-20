# -*- coding: utf-8 -*-
import pymysql
import scrapy
from scrapy import Request

from lagou import settings
from lagou.items import CompanyItem


class ZhaopinSpider(scrapy.Spider):
    name = 'zhaopin'
    allowed_domains = ['lagou.com']

    #修改请求头
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': settings.REQUEST_HEADERS
        }

    def start_requests(self):
        for id, url in self.get_url():
            yield Request(url=url, callback=self.parse_info, meta={'id': id})

    def parse_info(self, response):
        item = CompanyItem()
        item['id'] = response.meta.get('id')
        item['work_year'] = response.xpath('//span[@class="item workyear"]/span/text()').extract_first()
        item['education'] = response.xpath('//span[@class="item education"]/span/text()').extract_first()
        item['company_info'] = ''.join(response.xpath('//p[@class="info"]/text()').extract())
        item['company_label'] = response.xpath('//div[@class="temptation"]/text()').extract_first()
        item['requirement'] = ' '.join(response.xpath('//div[@class="content"]/p/text()').extract())
        yield item

    def get_url(self):
        conn = pymysql.connect(host=settings.MYSQL_HOST,
                               port=settings.MYSQL_PORT,
                               user=settings.MYSQL_USER,
                               password=settings.MYSQL_PASSWORD,
                               db=settings.MYSQL_DB)
        cursor = conn.cursor()
        count_sql = 'SELECT count(id) FROM lagou'
        cursor.execute(count_sql)
        num, = cursor.fetchone()
        sql = 'SELECT id, detail_url FROM lagou'
        cursor.execute(sql)
        for _ in range(num):
            id, url = cursor.fetchone()
            yield id, url
        cursor.close()
        conn.close()