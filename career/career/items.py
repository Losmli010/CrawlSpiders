# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CareerItem(scrapy.Item):
    # define the fields for your item here like:
    # 职位名称
    title = scrapy.Field()
    # 职位类别
    type = scrapy.Field()
    # 人数
    num = scrapy.Field()
    # 工作地点
    place = scrapy.Field()
    #受教育程度
    education = scrapy.Field()
    #工作年限
    work_year = scrapy.Field()
    # 岗位描述网址
    detail_url = scrapy.Field()
    # 岗位描述
    desc = scrapy.Field()
    # 岗位要求
    requirement = scrapy.Field()
    # 更新时间
    update_time = scrapy.Field()
