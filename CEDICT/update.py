#!/usr/bin/env python3
"""Download and parse latest CEDICT"""

from collections import defaultdict
import json
import re

from pinyin import decode_pinyin

# TODO: Export trad-only and simp-only .txts for jieba

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Download latest CEDICT
# └─────────────────────────────────────────────────────────────────────────────

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Parse + Convert to JSON
# └─────────────────────────────────────────────────────────────────────────────
with open('cedict_ts.u8', 'r', encoding='utf-8') as f:
    raw_entries = [line.strip() for line in f if line[0] != '#']

cedict = defaultdict(list)
for raw_entry in raw_entries:
    # CEDICT format: trad simp [pinyin] /def1/def2/.../
    parsed = re.search(r'^(.*?) (.*?) \[(.*?)\] /(.*)/$', raw_entry).groups()
    trad = parsed[0]
    simp = parsed[1]
    pinyin = parsed[2]
    defs = parsed[3]

    pinyin = decode_pinyin(pinyin)
    defs = defs.replace('/', '; ')
    inner_pinyins = re.findall(r'\[(.*?)\]', defs)
    for ip in inner_pinyins:
        pinyin_unicode = decode_pinyin(ip)
        defs = defs.replace(ip, pinyin_unicode)

    keys = set([simp, trad])
    parsed_entry = {'trad': trad, 'simp': simp, 'pinyin': pinyin, 'defs': defs}
    for key in keys: cedict[key].append(parsed_entry)


with open('cedict_ts.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(cedict, f, indent=2, ensure_ascii=False)
