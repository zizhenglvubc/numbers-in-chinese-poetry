# Provenance

## Timeline

| Date | Event |
|---|---|
| 2026-07-16 to 07-19 | Slides prepared. The author's section, *有数之形，无数之意：隋唐至明清诗词中的数字文化观*, dated 2026-07-19. |
| 2026-07-21 | Corpus downloaded; `本地验证脚本.py` written; scan run. Result: 175,355 poems, 103,885 with a numeral, 59.24%. |
| 2026-07-22 | Presentation delivered; PDF export dated. |
| 2026-07-25 | Combined group deck (65 slides) assembled. |
| 2026-09-13 | Repository built. Original script re-run and reproduced exactly. |

All dates are filesystem timestamps on the author's own machine. No commit dates
have been backdated: the git history of this repository begins on 2026-09-13,
which is when the repository was created, not when the analysis was done.

## What is original and what was added

**July 2026, by the author:** the research question, the corpus selection and
grouping, the numeral character set, the counting logic, the poem as unit of
analysis, the per-collection rates, the 59.24% headline figure, and the close
readings in the slides.

**September 2026, while preparing this release:** `src/numeral_scan.py` (a
re-implementation that emits CSV and JSON and a corpus manifest), character-level
rates, the extended quantity-word character set, the figures, the derived
dataset, and this documentation. Every added measurement is labelled in the
files that carry it.

The original script is preserved unmodified at
`archive/original/本地验证脚本.py`
(SHA-256 `b63d062b8d8e45c72524bf5d191bdb5d497f473ce383930c73375202c71f4450`).
Running it reproduces the July 2026 output exactly, including its own hard-coded
reference line.

## Group context

The presentation was one section of a four-person group presentation on numerals
in the Chinese language. Each member prepared an independent section; the
sections were combined into a single 65-slide deck at the end. The corpus scan
and the counting code were the author's own contribution and were not part of
any other member's section. Only the author's section and code are released
here. See [`../AUTHORS.md`](../AUTHORS.md).


## Prior scholarship

Quantitative study of Tang and Song poetry has an established literature, and
word-frequency work has repeatedly found `一` among the highest-frequency
characters in the corpus — consistent with what this scan finds. What is offered
here is not the discovery of that fact but a specific implementation: a stated
numeral character set, a stated unit of analysis, per-collection rates across
six collections from the Tang to the Qing, and code and derived data that let
the numbers be checked.
