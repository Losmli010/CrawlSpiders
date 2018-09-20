# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

from lagou import settings
from lagou.items import LagouItem, CompanyItem


class LagouPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST,
                                    port=settings.MYSQL_PORT,
                                    user=settings.MYSQL_USER,
                                    password=settings.MYSQL_PASSWORD,
                                    db=settings.MYSQL_DB)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, LagouItem):
            try:
                sql = 'INSERT INTO lagou(id, title, salary, company_name, city, update_time, detail_url) ' \
                      'VALUES(%d, "%s", "%s", "%s", "%s", "%s", "%s")' % \
                      (item['id'], item['title'], item['salary'], item['company_name'],
                       item['city'], item['update_time'], item['detail_url'])
                self.cursor.execute(sql)
                self.conn.commit()
            except:
                pass

        if isinstance(item, CompanyItem):
            sql = 'UPDATE lagou SET work_year="%s", education="%s", company_info="%s", company_label="%s", requirement="%s" WHERE id=%d' % \
                  (item['work_year'], item['education'], item['company_info'], item['company_label'], item['requirement'], item['id'])
            self.cursor.execute(sql)
            self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
