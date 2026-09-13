# -*- coding: utf-8 -*-
"""
numeral_scan.py — numerals in classical Chinese poetry
Author: Zizheng Lv

Scans a corpus of classical Chinese poetry and reports how often numeral
characters appear, collection by collection.

Modes:

  --mode replicate  (default)
      Poem-level rates: the share of poems containing at least one numeral.
      Over the corpus described in the accompanying documentation this gives
      175,355 poems scanned and 103,885 containing a numeral (59.24%).

  --mode extended
      Also reports character-level rates, per-numeral frequencies, and a
      second poem-level rate counting approximate and indefinite quantity
      words alongside the numerals.

Usage:
    python3 src/numeral_scan.py --corpus path/to/chinese-poetry --out results/
"""
import argparse, csv, glob, hashlib, json, os, sys
from collections import Counter
from datetime import datetime, timezone

# The numerals counted by the scan.
NUMERAL_CHARS = set('一二三四五六七八九十百千万萬亿億两兩零廿卅')

# Approximate and indefinite quantity words, counted in extended mode.
EXTENDED_QUANTITY_CHARS = set('半双雙几幾数數无無')

GROUPS = {
    'tang_shi':      ('唐诗',           'quantang/poet.tang.*.json'),
    'song_shi_1_3':  ('宋诗(1/3抽样)',  'quantang/poet.song.*.json'),
    'song_ci':       ('宋词',           'songci/ci.song.*.json'),
    'yuan_qu':       ('元曲',           'yuanqu/yuanqu.json'),
    'wudai':         ('五代诗词',       'wudai/*/*.json'),
    'nalan_qing_ci': ('清词(纳兰)',     'nalanxingde/*.json'),
}
# Directory names differ between the upstream repo layout and the 2026 local copy.
LAYOUT_ALIASES = {
    'quantang': ['全唐诗', 'quan_tang_shi', 'quantangshi'],
    'songci': ['宋词', 'ci'],
    'yuanqu': ['元曲'],
    'wudai': ['五代诗词', 'wudai'],
    'nalanxingde': ['纳兰性德'],
}
TEXT_KEYS = ('paragraphs', 'content', 'para', 'poem', 'text')


def resolve(corpus, pattern):
    """Match a group pattern against either the upstream or the 2026 local layout."""
    head, tail = pattern.split('/', 1)
    for name in [head] + LAYOUT_ALIASES.get(head, []):
        hits = sorted(glob.glob(os.path.join(corpus, name, tail)))
        if hits:
            return hits
    return []


def poem_texts(path):
    """Yield the text of every poem in one corpus file."""
    try:
        data = json.load(open(path, encoding='utf-8'))
    except Exception as exc:
        print(f'  !! skipped {os.path.basename(path)}: {exc}', file=sys.stderr)
        return
    if isinstance(data, dict):
        data = data.get('poems') or data.get('content') or []
    for poem in data:
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
            yield text


def scan(corpus, extended=False):
    rows, manifest = [], []
    for key, (label, pattern) in GROUPS.items():
        files = resolve(corpus, pattern)
        if not files:
            print(f'  !! no files matched for {label} ({pattern})', file=sys.stderr)
        poems = hits = chars = numeral_chars = ext_hits = 0
        per_char = Counter()
        for path in files:
            manifest.append({
                'file': os.path.relpath(path, corpus),
                'sha256': hashlib.sha256(open(path, 'rb').read()).hexdigest(),
                'bytes': os.path.getsize(path),
            })
            for text in poem_texts(path):
                poems += 1
                chars_in = set(text)
                # A poem counts once, however many numerals it contains.
                if chars_in & NUMERAL_CHARS:
                    hits += 1
                if extended:
                    chars += len(text)
                    for ch in text:
                        if ch in NUMERAL_CHARS:
                            numeral_chars += 1
                            per_char[ch] += 1
                    if chars_in & (NUMERAL_CHARS | EXTENDED_QUANTITY_CHARS):
                        ext_hits += 1
        row = {
            'group_id': key,
            'group_label_zh': label,
            'files': len(files),
            'poems': poems,
            'poems_with_numeral': hits,
            'poem_level_rate': round(hits / poems, 6) if poems else None,
        }
        if extended:
            row.update({
                'EXT_total_chars': chars,
                'EXT_numeral_chars': numeral_chars,
                'EXT_char_level_rate': round(numeral_chars / chars, 6) if chars else None,
                'EXT_poems_with_numeral_or_quantity': ext_hits,
                'EXT_top_numerals': ' '.join(f'{c}:{n}' for c, n in per_char.most_common(10)),
            })
        rows.append(row)
        print(f'{label:14s} {poems:7d} poems  {hits:7d} with numeral'
              + (f'  ({hits/poems*100:.1f}%)' if poems else ''))
    return rows, manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--corpus', required=True, help='root of the chinese-poetry corpus')
    ap.add_argument('--out', default='results', help='output directory')
    ap.add_argument('--mode', choices=['replicate', 'extended'], default='replicate')
    args = ap.parse_args()

    extended = args.mode == 'extended'
    print(f'mode = {args.mode}\n')
    rows, manifest = scan(args.corpus, extended=extended)

    total_poems = sum(r['poems'] for r in rows)
    total_hits = sum(r['poems_with_numeral'] for r in rows)
    rate = total_hits / total_poems if total_poems else 0
    print(f'\nTOTAL {total_poems} poems, {total_hits} contain a numeral ({rate*100:.2f}%)')
    if args.mode == 'replicate':
        ok = (total_poems, total_hits) == (175355, 103885)
        print('reference totals 175355 / 103885 (59.24%): '
              + ('match' if ok else 'no match, different corpus snapshot'))

    os.makedirs(args.out, exist_ok=True)
    suffix = '' if args.mode == 'replicate' else '_extended'
    csv_path = os.path.join(args.out, f'numeral_rates_by_group{suffix}.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        'title': 'Numerals in Classical Chinese Poetry',
        'author': 'Zizheng Lv',
        'mode': args.mode,
        'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'unit_of_analysis': 'poem (a poem counts once if it contains any numeral character)',
        'numeral_chars': ''.join(sorted(NUMERAL_CHARS)),
        'extended_quantity_chars': (
            ''.join(sorted(EXTENDED_QUANTITY_CHARS)) if extended else None),
        'totals': {
            'poems': total_poems,
            'poems_with_numeral': total_hits,
            'poem_level_rate': round(rate, 6),
        },
        'groups': rows,
        'corpus_files': len(manifest),
    }
    with open(os.path.join(args.out, f'summary{suffix}.json'), 'w', encoding='utf-8') as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(args.out, 'corpus_manifest.json'), 'w', encoding='utf-8') as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
    print(f'\nwrote {csv_path} and summary{suffix}.json')


if __name__ == '__main__':
    main()
