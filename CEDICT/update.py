#!/usr/bin/env python3
"""Download and parse latest CEDICT"""

from collections import defaultdict
import json
import re

from pinyin import decode_pinyin

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Download latest CEDICT
# └─────────────────────────────────────────────────────────────────────────────

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Parse + Convert to JSON
# └─────────────────────────────────────────────────────────────────────────────
with open('cedict_ts.u8', 'r', encoding='utf-8') as f:
    raw_entries = [line.strip() for line in f if line[0] != '#']

cedict = defaultdict(list)
trad_all, simp_all = [], []
for raw_entry in raw_entries:
    # CEDICT format: trad simp [pinyin] /def1/def2/.../
    parsed = re.search(r'^(.*?) (.*?) \[(.*?)\] /(.*)/$', raw_entry).groups()
    trad = parsed[0]
    simp = parsed[1]
    pinyin = parsed[2]
    defs = parsed[3]

    pinyin_unicode = decode_pinyin(pinyin)
    defs = defs.replace('/', '; ')
    inner_pinyins = re.findall(r'\[(.*?)\]', defs)
    for ip in inner_pinyins:
        ip_unicode = decode_pinyin(ip)
        defs = defs.replace(ip, ip_unicode)

    keys = set([simp, trad])
    parsed_entry = {'t': trad, 's': simp, 'p': pinyin_unicode, 'p#': pinyin, 'd': defs}
    for key in keys: cedict[key].append(parsed_entry)

    trad_all.append(trad)
    simp_all.append(simp)


with open('cedict_ts.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(cedict, f, ensure_ascii=False)

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Create text files to power Jieba segmentation
# └─────────────────────────────────────────────────────────────────────────────
with open('cedict_t_jieba.txt', 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(trad_all))

with open('cedict_s_jieba.txt', 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(simp_all))
