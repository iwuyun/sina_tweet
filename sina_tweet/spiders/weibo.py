# -*- coding: utf-8 -*-
import scrapy

import os

import json
import time
import random
# import urllib

# url_pattern = 'https://m.weibo.cn/u/{}'
url_pattern = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={0}&containerid=107603{0}'

from titan_spider.settings import DATA_DIR, STAR_MAP
assert os.path.isdir(DATA_DIR)
assert os.path.isdir(STAR_MAP)

class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['m.weibo.cn']

    def __init__(self):
        self.star_map = {}
        self.start_urls = []
        with open(STAR_MAP) as src:
            for line in src.readlines():
                star_name, user_id = line.strip().split('\t')
                url = url_pattern.format(user_id)
                self.star_map[url] = star_name
                self.start_urls.append(url)

    def parse(self, response):
        url = response.url
        star_name = self.star_map[url]
        star_dir = os.path.join(DATA_DIR, star_name)
        if not os.path.isdir(star_dir):
            os.mkdir(star_dir)
        data = response.body
        filename = 'tweet.json'
        path = os.path.join(star_dir, filename)
        with open(path, 'w') as dest:
            dest.write(data)
        interval = 2 + 3 * random.random()
        time.sleep(interval)
