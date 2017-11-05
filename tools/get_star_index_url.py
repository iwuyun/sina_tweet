# _*_ coding: utf-8 _*_

import sys

import re
import time
import random

import requests
from requests.exceptions import ConnectionError
import urllib

url_pattern = 'http://s.weibo.com/user/{}&Refer=weibo_user'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
headers = {
    'User-Agent': user_agent,
}

with open(sys.argv[1]) as src:
    names = [n.strip() for n in src.readlines()]

for name in names:
    encoded_name = urllib.quote(name)
    try:
        response = requests.get(url_pattern.format(encoded_name), timeout=2, headers=headers)
    except ConnectionError as e:
        print 'Timeout'
        break
    content = response.content
    match = re.search(r'<a target=\\"_blank\\" href=\\"(.*?)\\"', content)
    if not match:
        print 'Not Found'
        break
    index_url = match.group(1).replace('\\', '')
    print index_url
    interval = 3 + 2 * random.random()
    time.sleep(interval)
