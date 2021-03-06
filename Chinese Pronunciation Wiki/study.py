#!/usr/bin/env python3
"""Prepare the scraped pronunciation points for study in Anki"""

import json
import os

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Prepare Anki cards from new pronunciation points
# └─────────────────────────────────────────────────────────────────────────────
with open('scraped.json', 'r', encoding='utf-8') as f:
    new_points = json.load(f)

s = 'Chinese Pronunciation Wiki {level}<br><br><a href="{url}">{title}</a>'
tsv = [s.format(p['level'], p['url'], p['title']) for p in new_points.values()]

with open('for_Anki.txt', 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(tsv))

os.remove('scraped.json')

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Update studied pronunciation points
# └─────────────────────────────────────────────────────────────────────────────
with open('studied.json', 'r', encoding='utf-8') as f:
    studied_points = json.load(f)

studied_points.update(new_points)
with open('studied.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(studied_points, f, indent=2)

# Display stats
print(f'New points: {len(new_points)}\nTotal points: {len(studied_points)}')
