# -*- coding: utf-8 -*-
"""
build_poem_level_dataset.py — per-poem derived dataset
Author: Zizheng Lv

Emits one row per poem with numeral counts only. Poem text is NOT included,
so the output is a derived dataset and does not redistribute the corpus.
"""
import argparse, csv, gzip, os
from numeral_scan import GROUPS, NUMERAL_CHARS, EXTENDED_QUANTITY_CHARS, resolve, TEXT_KEYS
import json

FIELDS = ['group_id', 'source_file', 'poem_index', 'author', 'title',
          'chars', 'numeral_chars', 'distinct_numerals', 'has_numeral',
          'has_numeral_or_quantity_word']


def poems(path):
    try:
        data = json.load(open(path, encoding='utf-8'))
    except Exception:
        return
    if isinstance(data, dict):
        data = data.get('poems') or data.get('content') or []
    for i, poem in enumerate(data):
        if not isinstance(poem, dict):
            continue
        value = None
        for key in TEXT_KEYS:
            value = poem.get(key)
            if value:
                break
        if not value:
            continue
        text = ''.join(value) if isinstance(value, list) else str(value)
        if text:
            yield i, poem, text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--corpus', required=True)
    ap.add_argument('--out', default='data/derived/poem_level_numerals.csv.gz')
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    n = 0
    with gzip.open(args.out, 'wt', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        for key, (_, pattern) in GROUPS.items():
            for path in resolve(args.corpus, pattern):
                rel = os.path.relpath(path, args.corpus)
                for idx, poem, text in poems(path):
                    found = sorted(set(text) & NUMERAL_CHARS)
                    writer.writerow({
                        'group_id': key,
                        'source_file': rel,
                        'poem_index': idx,
                        'author': poem.get('author', ''),
                        'title': poem.get('title') or poem.get('rhythmic') or '',
                        'chars': len(text),
                        'numeral_chars': sum(1 for c in text if c in NUMERAL_CHARS),
                        'distinct_numerals': ''.join(found),
                        'has_numeral': int(bool(found)),
                        'has_numeral_or_quantity_word': int(bool(
                            set(text) & (NUMERAL_CHARS | EXTENDED_QUANTITY_CHARS))),
                    })
                    n += 1
    print(f'{n} rows -> {args.out} ({os.path.getsize(args.out)/1e6:.1f} MB gzipped)')


if __name__ == '__main__':
    main()
