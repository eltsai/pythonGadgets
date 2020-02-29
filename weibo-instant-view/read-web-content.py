#!/usr/bin/env python3
# -*- coding: utf-8 -*-
my_url = 'https://m.weibo.cn/status/4477083902547837'


# import dryscrape
# from bs4 import BeautifulSoup
# session = dryscrape.Session()
# session.visit(my_url)
# response = session.body()
# soup = BeautifulSoup(response)
# soup.find(id="intro-text")

import requests
import json
import re
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
r = requests.get(my_url)
content = re.match(r"\"text\": \"[^(\")]*\"", str(r.text.encode()))
#print(repr(r.text))
print(content) 
#print(data)