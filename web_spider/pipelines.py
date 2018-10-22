# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2

class WebSpiderPipeline(object):
    
    def __init__(self, db_user, db_url, db_passwd):
        self.db_user = db_user
        self,db_url = db_url
        self.db_passwd = db_passwd
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_user=crawler.settings.get('DB_USER'),
            db_url=crawler.settings.get('DB_URL'),
            db_passwd=crawler.settings.get('DB_PASSWD')
        )
    
    def open_spider(self, spider):
        print(spider)
    
    def close_spider(self, spider):
        print('asdasd')
        pass
    
    def process_item(self, item, spider):
        # print(item)
        return item


class PostgresPipeline(object):
    def __init__(self, db_name, db_host, db_port, db_user, db_passwd):
        self.db_name = db_name
        self.db_user = db_user
        self.db_host = db_host
        self.db_port = db_port
        self.db_passwd = db_passwd
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_name=crawler.settings.get('DB_NAME', 'postgres'),
            db_user=crawler.settings.get('DB_USER', 'postgres'),
            db_host=crawler.settings.get('DB_HOST', 'localhost'),
            db_port=crawler.settings.get('DB_USER', 5432),
            db_passwd=crawler.settings.get('DB_PASSWD', 1234567890)
        )
    
    def open_spider(self, spider):
        self.client = psycopg2.connect(
            database=self.db_name,
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_passwd
        )

        print(self.client)
    
    def close_spider(self, spider):
        print('asdasd')
        pass
    
    def process_item(self, item, spider):
        # print(item)
        return item