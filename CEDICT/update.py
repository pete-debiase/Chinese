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
    regex_search = re.search(r'^(.*?) (.*?) \[(.*?)\] /(.*)/', e).groups()
    trad = regex_search[0]
    simp = regex_search[1]
    pinyin = regex_search[2]
    defs = regex_search[3]

    pinyin = decode_pinyin(pinyin)
    defs = defs.replace('/', '; ')

    cedict[simp] = {'trad': trad, 'simp': simp, 'pinyin': pinyin, 'defs': defs}
    cedict[trad] = {'trad': trad, 'simp': simp, 'pinyin': pinyin, 'defs': defs}

with open('cedict_ts.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(cedict, f, indent=2, ensure_ascii=False)
