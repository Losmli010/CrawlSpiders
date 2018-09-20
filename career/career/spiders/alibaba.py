# -*- coding: utf-8 -*-
import json
from datetime import datetime

import scrapy
from scrapy import FormRequest

from career.items import CareerItem

class AlibabaSpider(scrapy.Spider):
    name = 'alibaba'
    allowed_domains = ['job.alibaba.com']

    def start_requests(self):
        post_url = 'https://job.alibaba.com/zhaopin/socialPositionList/doList.json'
        for i in range(1, 804):
            data = {
                'pageSize': '10',
                't': '0.9258839192303483',
                'pageIndex': '%d' % i
            }
            yield FormRequest(url=post_url, formdata=data, callback=self.parse_json)

    def parse_json(self, response):
        json_data = json.loads(response.text)
        datas = json_data.get('returnValue').get('datas')
        for data in datas:
            item = CareerItem()
            item['title'] = data.get('name')
            item['type'] = data.get('secondCategory')
            item['num'] = data.get('recruitNumber')
            item['place'] = data.get('workLocation')
            item['education'] = data.get('degree')
            item['work_year'] = data.get('workExperience')
            item['detail_url'] = 'https://job.alibaba.com/zhaopin/position_detail.htm?spm=a2obv.11410903.0.0.322944f6ClHzor&positionId=%d' % data.get('id')
            item['desc'] = data.get('description')
            item['requirement'] = data.get('requirement')
            item['update_time'] = datetime.utcfromtimestamp(data.get('gmtModified') // 1000).date().strftime('%Y-%m-%d')
            yield item



