# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    #岗位id
    id = scrapy.Field()
    #标题
    title = scrapy.Field()
    # 薪资
    salary = scrapy.Field()
    #公司名称
    company_name = scrapy.Field()
    #公司所在城市
    city = scrapy.Field()
    #更新时间
    update_time = scrapy.Field()
    #详情页url
    detail_url = scrapy.Field()

class CompanyItem(scrapy.Item):
    # 岗位id
    id = scrapy.Field()
    # 经验
    work_year = scrapy.Field()
    # 教育程度
    education = scrapy.Field()
    # 公司信息
    company_info = scrapy.Field()
    # 公司福利
    company_label = scrapy.Field()
    #岗位要求
    requirement = scrapy.Field()

