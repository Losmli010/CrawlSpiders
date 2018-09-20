# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import pymysql

from career import settings

class CareerPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST,
                                    port=settings.MYSQL_PORT,
                                    user=settings.MYSQL_USER,
                                    password=settings.MYSQL_PASSWORD,
                                    db=settings.MYSQL_DB)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        #更新爬取
        # if datetime.now().date().strftime('%Y-%m-%d') == item['update_time']:
        try:
            sql = 'INSERT INTO job VALUES(NULL, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % \
                  (item['title'], item['type'], item['num'], item['place'], item['education'], item['work_year'],
                   item['detail_url'], item['desc'], item['requirement'], item['update_time'])
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            pass
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
