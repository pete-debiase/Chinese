#!/usr/bin/env python3
"""Prepare the scraped pronunciation points for study in Anki"""

from collections import defaultdict
import json
import random
import os

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
print(f'''<a href="{lesson['url']}">{lesson['level']}: {lesson['title']}</a>\n\n''')

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Display stats
# └─────────────────────────────────────────────────────────────────────────────
scraped_points_by_level = organize_by_level(scraped_points)
studied_points_by_level = organize_by_level(studied_points)

print('Progress Stats')
for level in levels:
    num_studied = len(studied_points_by_level[level])
    num_scraped = len(scraped_points_by_level[level])
    ratio = num_studied / num_scraped
    print(f"{level}: {num_studied} / {num_scraped} ({ratio:.0%})")
