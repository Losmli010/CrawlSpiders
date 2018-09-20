# -*- coding: utf-8 -*-
import json
from urllib import parse

import scrapy
from scrapy import FormRequest, Request

from lagou import settings
from lagou.items import LagouItem


class LagoujobSpider(scrapy.Spider):
    name = 'lagoujob'
    allowed_domains = ['lagou.com']

    def start_requests(self):
        get_url = 'https://m.lagou.com/search.json'
        citys = ['北京', '上海', '广州', '深圳', '成都', '杭州', '武汉']
        for city in citys:
            for page in range(1, 51):
                formdata = {
                    'city': '%s' % city,
                    'positionName': '爬虫',
                    'pageNo': '%d' % page,
                    'pageSize': '15'
                }
                yield FormRequest(url=get_url, method='GET', formdata=formdata, callback=self.parse_json)

    def parse_json(self, response):
        json_data = json.loads(response.text)
        if json_data.get('content'):
            results = json_data.get('content').get('data').get('page').get('result')
            for result in results:
                item = LagouItem()
                item['id'] = result.get('positionId')
                item['title'] = result.get('positionName')
                item['salary'] = result.get('salary')
                item['company_name'] = result.get('companyFullName')
                item['city'] = result.get('city')
                item['update_time'] = result.get('createTime')
                item['detail_url'] = ''.join(['https://m.lagou.com/jobs/', str(item['id']), '.html'])
                yield item

                meta = {'id': item['id'], 'dont_redirect': True}
                # yield Request(url=item['detail_url'], callback=self.parse_info, headers=settings.REQUEST_HEADERS, meta=meta)

