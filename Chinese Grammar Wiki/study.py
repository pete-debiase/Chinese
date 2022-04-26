#!/usr/bin/env python3
"""Prepare the scraped pronunciation points for study in Anki"""

from collections import defaultdict
import json
import random
import requests
import os

from bs4 import BeautifulSoup

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Basic setup
# └─────────────────────────────────────────────────────────────────────────────
path = r'C:\Users\pete\ALL\Languages\ZH\Chinese Grammar Wiki'
os.chdir(path)

def organize_by_level(grammar_points: dict):
    """Organize a raw grammar point JSON object by CEFR level."""
    points_by_level = defaultdict(list)
    for k, v in grammar_points.items():
        level = v['level']
        points_by_level[level].append([k, v])
    return points_by_level

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Identify grammar points available for study
# └─────────────────────────────────────────────────────────────────────────────
with open('scraped.json', 'r', encoding='utf-8') as f:
    scraped_points = json.load(f)

with open('studied.json', 'r', encoding='utf-8') as f:
    studied_points = json.load(f)

new_points = {k: v for k, v in scraped_points.items() if k not in studied_points}

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Select a new point at random from the lowest available level
# └─────────────────────────────────────────────────────────────────────────────
levels = ['A1', 'A2', 'B1', 'B2', 'C1']
new_points = organize_by_level(new_points)

for level in levels:
    if new_points[level]:
        selection = random.choice(new_points[level])
        _id = selection[0]
        lesson = selection[1]
        break

studied_points[_id] = lesson
with open('studied.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(studied_points, f, indent=2)

print(f"Chinese Grammar Wiki\n{lesson['level']}: {lesson['title']}\n")
link = f'''<a href="{lesson['url']}">{lesson['level']}: {lesson['title']}</a>'''
print(link, '\n\n')

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Display overall progress stats
# └─────────────────────────────────────────────────────────────────────────────
scraped_points_by_level = organize_by_level(scraped_points)
studied_points_by_level = organize_by_level(studied_points)

print('Progress Stats')
total_studied = total_scraped = 0
for level in levels:
    num_studied = len(studied_points_by_level[level])
    num_scraped = len(scraped_points_by_level[level])
    ratio = num_studied / num_scraped
    print(f"{level}: {num_studied} / {num_scraped} ({ratio:.0%})")
    total_studied += num_studied
    total_scraped += num_scraped
print(f"Total: {total_studied} / {total_scraped} ({total_studied / total_scraped:.0%})")

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Pull example sentences from selected point
# └─────────────────────────────────────────────────────────────────────────────
url = lesson['url']
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
example_groups = soup.find_all('div', {'class': 'liju'})

examples = []
for group in example_groups:
    items = group.find_all('li')
    for i in items:
        chinese = i.text
        try:
            expl = i.find_all('span', {'class': 'expl'})
            pinyin = i.find_all('span', {'class': 'pinyin'})[0].text
            english = i.find_all('span', {'class': 'trans'})[0].text
            if expl: expl = expl[0].text

            if expl: chinese = chinese.replace(expl, '')
            for rep in [pinyin, english, ' ']:
                chinese = chinese.replace(rep, '')
            pinyin = pinyin.replace('  ', ' ')
            if expl: english += f' ({expl})'

            example = f'{chinese}\t\t{pinyin.strip()}\t{english.strip()}\t\t\t{link}\tCGW'
            example.replace('  ', ' ')
        except:
            example = chinese
        examples.append(example)

examples = [e for e in examples if e]
with open('temp.tsv', 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(examples))
