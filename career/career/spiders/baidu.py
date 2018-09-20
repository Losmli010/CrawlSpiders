# -*- coding: utf-8 -*-
import json
from datetime import datetime

import scrapy
from scrapy import Request, FormRequest

from career.items import CareerItem


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['talent.baidu.com']

    def start_requests(self):
        post_url = 'https://talent.baidu.com/baidu/web/httpservice/getPostList'
        for i in range(1, 144):
            data = {
                'postType': '',
                'workPlace': '0/4/7/9',
                'recruitType': '2',
                'keyWord': '',
                'pageSize': '10',
                'curPage': '%d' % i,
                '_': '1536376946771'
            }
            yield FormRequest(url=post_url, method='GET', formdata=data, callback=self.parse_json)

    def parse_json(self, response):
        json_data = json.loads(response.text)
        post_list = json_data.get('postList')
        for data in post_list:
            item = CareerItem()
            item['title'] = data.get('name')
            item['type'] = data.get('postType')
            item['num'] = data.get('recruitNum')
            item['place'] = data.get('workPlace')
            item['education'] = data.get('education')
            item['work_year'] = data.get('workYears')
            item['detail_url'] = 'https://talent.baidu.com/external/baidu/index.html#/jobDetail/2/%d' % data.get('postId')
            item['desc'] = data.get('workContent')
            item['requirement'] = data.get('serviceCondition')
            item['update_time'] = data.get('publishDate')
            yield item
