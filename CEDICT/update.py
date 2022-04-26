#!/usr/bin/env python3
"""Download and parse latest CEDICT"""

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
    entries = [line.strip() for line in f if line[0] != '#']

cedict = {}
for e in entries:
    # CEDICT format: trad simp [pinyin] /def1/def2/.../
    parsed = re.search(r'^(.*?) (.*?) \[(.*?)\] /(.*)/$', e).groups()
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

    cedict[simp] = {'trad': trad, 'simp': simp, 'pinyin': pinyin, 'defs': defs}
    cedict[trad] = {'trad': trad, 'simp': simp, 'pinyin': pinyin, 'defs': defs}

with open('cedict_ts.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(cedict, f, indent=2, ensure_ascii=False)
