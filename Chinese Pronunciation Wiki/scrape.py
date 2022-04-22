#!/usr/bin/env python3
"""Scrape the Chinese Pronunciation Wiki"""

import json
import random
import requests
import time

from bs4 import BeautifulSoup

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Basic Setup
# └─────────────────────────────────────────────────────────────────────────────
levels = ['A1', 'A2', 'B1', 'B2']
url_base = 'https://resources.allsetlearning.com'
with open('studied.json', 'r', encoding='utf-8') as f:
    studied = json.load(f)

url_pattern = url_base + '/chinese/pronunciation/{}_pronunciation_points'
urls = [url_pattern.format(l) for l in levels]

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Aggregate New Pronunciation Points For Each Level
# └─────────────────────────────────────────────────────────────────────────────
points = {}
for level, url in zip(levels, urls):
    time.sleep(random.randint(1, 3))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get pronunciation points from second column of each table row
    count = 0
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 3:
            a_tag = cols[1].find_all('a')[0] # a-tag in second column
            href = a_tag.get('href')
            title = a_tag.text
            _id = href.split('/')[-1]

            if _id not in studied:
                points[_id] = {'level': level, 'title': title, 'url': url_base + href}
                count += 1

    # Display stats
    print(f'Level {level}: {count} new points')

with open('scraped.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(points, f, indent=2)
