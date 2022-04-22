#!/usr/bin/env python3
"""Scrape the Chinese Grammar Wiki"""

import json
import random
import requests
import time

from bs4 import BeautifulSoup

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Basic Setup
# └─────────────────────────────────────────────────────────────────────────────
levels = ['A1', 'A2', 'B1', 'B2', 'C1']
url_base = 'https://resources.allsetlearning.com'
with open('scraped.json', 'r', encoding='utf-8') as f:
    scraped_points = json.load(f)

url_pattern = url_base + '/chinese/grammar/{}_grammar_points'
urls = [url_pattern.format(l) for l in levels]

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Aggregate New Grammar Points For Each Level
# └─────────────────────────────────────────────────────────────────────────────
new_points = {}
for level, url in zip(levels, urls):
    time.sleep(random.randint(3, 6))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get pronunciation points from first column of each table row
    count = 0
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 3:
            a_tag = cols[0].find_all('a')[0] # a-tag in first column
            href = a_tag.get('href')
            title = a_tag.text
            _id = href.split('/')[-1]

            if _id not in scraped_points:
                new_points[_id] = {'level': level, 'title': title, 'url': url_base + href}
                count += 1

    # Display stats
    print(f'Level {level}: {count} new points')

scraped_points.update(new_points)
with open('scraped.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(scraped_points, f, indent=2)
