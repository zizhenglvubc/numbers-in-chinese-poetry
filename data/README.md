# Data

## What is here

`derived/numeral_rates_by_group.csv` — the released dataset. One row per
collection plus a total row, with poem counts, numeral counts, poem-level and
character-level rates, and the ten most frequent numerals in each collection.
CC BY 4.0.

Machine-readable run output is in [`../results/`](../results/):
`summary.json`, `numeral_rates_by_group.csv`, their `_extended` counterparts,
and `corpus_manifest.json`.

## What is not here

The source corpus is **not redistributed**. It belongs to the
[`chinese-poetry/chinese-poetry`](https://github.com/chinese-poetry/chinese-poetry)
project and is available there under the MIT License.

## Obtaining the corpus

```bash
git clone https://github.com/chinese-poetry/chinese-poetry.git data/corpus
python3 src/numeral_scan.py --corpus data/corpus --out results/
```

The script accepts both the current upstream directory layout and the layout of
the July 2026 local copy (`全唐诗/`, `宋词/`, `元曲/`, `五代诗词/`, `纳兰性德/`).

## Verifying you have the same corpus

The July 2026 analysis used a snapshot downloaded on 2026-07-21. The upstream
commit was not recorded at the time, so `results/corpus_manifest.json` lists a
SHA-256 hash and byte size for every one of the 182 corpus files actually
scanned. To check whether your copy matches:

```bash
python3 - <<'PY'
import hashlib, json, os, sys
manifest = json.load(open('results/corpus_manifest.json', encoding='utf-8'))
root = sys.argv[1] if len(sys.argv) > 1 else 'data/corpus'
same = diff = missing = 0
for entry in manifest:
    path = os.path.join(root, entry['file'])
    if not os.path.exists(path):
        missing += 1
    elif hashlib.sha256(open(path, 'rb').read()).hexdigest() == entry['sha256']:
        same += 1
    else:
        diff += 1
print(f'identical {same}, differing {diff}, missing {missing}, of {len(manifest)}')
PY
```

If files differ, the scan still runs; the totals will reflect your snapshot
rather than the July 2026 one. `--mode replicate` prints whether the
175,355 / 103,885 reference totals were reproduced.

## Data dictionary

| Column | Meaning |
|---|---|
| `group_id` | Machine-readable collection identifier |
| `group_label_zh` | Collection name as used in the original analysis |
| `period` | Dynasty and years |
| `genre` | shi, ci, or qu |
| `source_collection` | Anthology the texts come from |
| `poems` | Poems scanned |
| `poems_with_numeral` | Poems containing at least one numeral character |
| `poem_level_rate` | `poems_with_numeral / poems` |
| `total_chars` | Characters in the collection's poem texts |
| `numeral_chars` | Numeral character occurrences |
| `char_level_rate` | `numeral_chars / total_chars` |
| `poems_with_numeral_or_quantity_word` | Poems containing a numeral **or** one of 半 双 雙 几 幾 数 數 无 無 |
| `top_numerals` | Ten most frequent numerals, `character:count` |

`total_chars`, `numeral_chars`, `char_level_rate`, `poems_with_numeral_or_quantity_word`
and `top_numerals` were added in September 2026. The remaining columns are the
July 2026 analysis.
