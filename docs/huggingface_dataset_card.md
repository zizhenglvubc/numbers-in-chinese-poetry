---
license: cc-by-4.0
language:
  - zh
tags:
  - digital-humanities
  - classical-chinese
  - poetry
  - computational-literary-studies
  - corpus-linguistics
pretty_name: Numerals in Classical Chinese Poetry (Tang–Qing)
size_categories:
  - 100K<n<1M
---

# Numerals in Classical Chinese Poetry (Tang–Qing)

**Zizheng Lv** · ORCID [0009-0004-0327-4477](https://orcid.org/0009-0004-0327-4477) · DOI [10.5281/zenodo.22734274](https://doi.org/10.5281/zenodo.22734274)
Code and documentation: https://github.com/zizhenglvubc/numbers-in-chinese-poetry

## Dataset summary

Numeral counts for 175,355 classical Chinese poems from the Tang dynasty through
the Qing. Two files:

- `poem_level_numerals.csv.gz` — one row per poem, 175,355 rows.
- `numeral_rates_by_group.csv` — one row per collection, 7 rows including a total.

59.24% of the poems contain at least one numeral character. Numerals make up
2.15% of all 11,571,489 characters.

**Poem text is not included.** This is a derived dataset of counts and
bibliographic metadata.

## Languages

Classical Chinese (`lzh`), written in Chinese script. Metadata fields are in
Chinese; column names are in English.

## Data sources

Derived from [`chinese-poetry/chinese-poetry`](https://github.com/chinese-poetry/chinese-poetry)
(MIT License), snapshot downloaded 2026-07-21. A SHA-256 manifest of all 182
corpus files scanned is published with the code, so any copy of the corpus can
be checked against the one used here.

## Temporal coverage

| Collection | Period | Genre | Poems |
|---|---|---|---:|
| *Quan Tang shi* | Tang, 618–907 | shi | 57,603 |
| *Huajian ji* + Southern Tang | Five Dynasties, 907–979 | shi and ci | 543 |
| *Quan Song shi* (1/3 subset) | Song, 960–1279 | shi | 84,984 |
| *Quan Song ci* | Song, 960–1279 | ci | 21,053 |
| *Yuan qu* | Yuan, 1271–1368 | qu | 10,914 |
| Nalan Xingde | Qing, 1644–1912 | ci | 258 |

## Data structure

`poem_level_numerals.csv.gz`

| Field | Type | Description |
|---|---|---|
| `group_id` | string | Collection identifier |
| `source_file` | string | Path of the corpus file the poem came from |
| `poem_index` | int | Position of the poem within that file |
| `author` | string | Author as recorded in the corpus |
| `title` | string | Title, or tune name for *ci* and *qu* |
| `chars` | int | Characters in the poem text |
| `numeral_chars` | int | Numeral character occurrences |
| `distinct_numerals` | string | The distinct numerals present, e.g. `千百` |
| `has_numeral` | 0/1 | Whether any numeral is present |
| `has_numeral_or_quantity_word` | 0/1 | Numeral **or** one of 半 双 雙 几 幾 数 數 无 無 |

## Numeral definition

A character counts as a numeral if it is one of:

```
一 二 三 四 五 六 七 八 九 十 百 千 万 萬 亿 億 两 兩 零 廿 卅
```

The unit of analysis for `has_numeral` is the poem: a poem is counted once
whether it contains one numeral or twenty.

`has_numeral_or_quantity_word` additionally covers approximate and indefinite
quantity words (半 双 雙 几 幾 数 數 无 無). This column was added in September
2026 and was not part of the original analysis; including it raises the
poem-level rate from 59.24% to 73.4%.

## Processing

Corpus JSON is read, poem text is assembled from whichever of `paragraphs`,
`content`, `para`, `poem` or `text` is present, and characters are tested by set
intersection against the numeral set. Poems with no text are skipped. The full
pipeline is `src/numeral_scan.py` and `src/build_poem_level_dataset.py` in the
code repository.

## Limitations

- The Song shi figure is a 1/3 subset of *Quan Song shi*, not the complete collection.
- The Qing period is represented by Nalan Xingde alone (258 poems).
- The character set covers integers; approximate and indefinite quantity words
  are carried in a separate column.

## Licence

CC BY 4.0. The source corpus is MIT-licensed and belongs to the `chinese-poetry`
project; it is not redistributed here.

## Citation

```bibtex
@software{lv_numbers_chinese_poetry_2026,
  author  = {Lv, Zizheng},
  title   = {Numbers in Chinese Poetry from the Tang Dynasty Onward},
  version = {1.0.0},
  year    = {2026},
  doi     = {10.5281/zenodo.22734274},
  url     = {https://github.com/zizhenglvubc/numbers-in-chinese-poetry}
}
```
