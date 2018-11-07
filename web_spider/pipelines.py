# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
import uuid
import os

class SaveArticlePipeline(object):

    def __init__(self, article_path):
        self.article_path = article_path
        if not os.path.exists(self.article_path):
            os.makedirs(self.article_path)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            article_path=crawler.settings.get('ARTICLES_DIRECTORY', 'articles')
        )

    def open_spider(self, spider):
        print(spider)
    
    def close_spider(self, spider):
        print('asdasd')
        pass

    def process_item(self, item, spider):
        url = item.get('url').split('/').pop()
        file_name = f"{url.split('?')[0]}_{uuid.uuid4()}"
        print(file_name)
        with open(os.path.join(self.article_path, file_name), 'w') as f:
            f.write(item.get('text'))
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
            db_port=crawler.settings.get('DB_PORT', 5432),
            db_passwd=crawler.settings.get('DB_PASSWD', 1234567890)
        )
    
    def open_spider(self, spider):
        try:
            self.client = psycopg2.connect(
                database=self.db_name,
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_passwd
            )
            self.db = self.client.cursor();
            
            self.db.execute("CREATE TABLE IF NOT EXISTS pure_pc (id serial PRIMARY KEY, date varchar, text varchar);")
        except psycopg2.Error as err:
            print(err)
    
    def close_spider(self, spider):
        pass
    
    def process_item(self, item, spider):
        print(f'INSERT INTO pk_news (date, text) VALUES (\"{"test"}\", {item["text"]})')
        try:
            self.db.execute(f'INSERT INTO pk_news (date, text) VALUES (\'{item["time"]}\', \'{item["text"]}\')')
        except psycopg2.Error as err:
            print(f'Error while processing {item}: {err}')
        return item