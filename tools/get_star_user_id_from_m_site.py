# _*_ coding: utf-8 _*_
import sys

import requests
from requests.exceptions import ConnectionError

import urllib

import json
import time
import random


url_pattern = 'https://m.weibo.cn/api/container/getIndex?type=user&query{0}&luicode=10000011&lfid=106003type%3D1&title={0}&containerid=100103type%3D3%26q%3D{0}'

user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/61.0.3163.100 Mobile/13B143 Safari/601.1.46'

headers = {
    'User-Agent': user_agent,
}

with open(sys.argv[1]) as src:
    names = [n.strip() for n in src.readlines()]

for name in names:
    encoded_name = urllib.quote(name)
    url = url_pattern.format(encoded_name)
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except ConnectionError as e:
        print 'Timeout'
        break
    data = response.content
    data = json.loads(data)
    assert 'cards' in data
    cards = data['cards']
    assert len(cards) > 0
    target_card = cards[1]
    assert 'card_group' in target_card
    card_group = target_card['card_group']
    assert len(card_group) > 0
    card_wrapper = card_group[0]
    assert 'user' in card_wrapper
    user = card_wrapper['user']
    assert 'id' in user
    user_id = user['id']
    print user_id
    interval = 1 + 3 * random.random()
    time.sleep(interval)
