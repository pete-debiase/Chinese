#!/usr/bin/env python3
"""Thin wrapper around tools for segmenting/converting pinyin"""

import re

import dragonmapper.transcriptions as dmt
import zhon.pinyin as zp


def segment_accented_pinyin(unicode_pinyin: str) -> list[str]:
    """Segment the specified pinyin into individual syllables."""
    syllables = re.findall(zp.syllable, unicode_pinyin, re.I)
    return syllables

def numeric_to_accented(numeric_pinyin: str) -> str:
    """Convert numeric pinyin to unicode pinyin (ge1 ge5 ⇒ gē ge)"""
    accented = dmt.numbered_to_accented(numeric_pinyin)
    return accented

def accented_to_numeric(accented_pinyin: str) -> str:
    """Convert numeric pinyin to unicode pinyin (gē ge ⇒ ge1 ge5)"""
    numeric = dmt.accented_to_numbered(accented_pinyin)
    return numeric

def tonetag(pinyin_accented: str, hanzi=None) -> tuple[str, str|None]:
    """Span-tag pinyin/by tone (for displaying with color)."""
    pinyin_tagged, hanzi_tagged = pinyin_accented, hanzi

    syllables_accented = segment_accented_pinyin(pinyin_accented)
    syllables_numeric = [accented_to_numeric(s) for s in syllables_accented]
    tones = [re.findall(r'\d', s)[0] for s in syllables_numeric]

    for a, t in zip(syllables_accented, tones):
        pinyin_tagged = pinyin_tagged.replace(a, f'<span class="tone{t}">{a}</span>')

    if hanzi:
        hanzis = list(hanzi)
        for h, t in zip(hanzis, tones):
            hanzi_tagged = hanzi_tagged.replace(h, f'<span class="tone{t}">{h}</span>')

    return (pinyin_tagged, hanzi_tagged)


if __name__ == '__main__':
    # Segmentation
    pinyin_sentence = 'Nǐ xiǎng chī gè bāozi ma?'
    print(segment_accented_pinyin(pinyin_sentence))

    # Numeric to accented
    pinyin_numeric = 'guan1 xin1'
    print(numeric_to_accented(pinyin_numeric))

    # Accented to numeric
    pinyin_accented = 'guānxīn'
    print(accented_to_numeric(pinyin_accented))

    # Tonetag
    pinyin_accented = '“Nǐ shì bu shì hái méi chīfàn?”'
    print(tonetag(pinyin_accented))

    pinyin_accented, hanzi = 'yàoshi', '要是'
    print(tonetag(pinyin_accented, hanzi))
