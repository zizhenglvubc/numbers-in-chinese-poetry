# Changelog

## [1.0.0] — 2026-09-13

First public release.

### Original analysis (July 2026)
- Corpus scan of 175,355 poems, Tang through Qing: 103,885 poems (59.24%)
  contain at least one numeral character.
- Numeral character set, poem-level counting logic, and per-collection rates.
- Presentation, *有数之形，无数之意：隋唐至明清诗词中的数字文化观*, 15 slides.

### Added for this release (September 2026)
- `src/numeral_scan.py`, a reproducible re-implementation with CSV and JSON
  output and a SHA-256 corpus manifest. Reproduces the July 2026 totals exactly.
- Character-level rates: numerals account for 2.15% of all 11,571,489 characters.
- Extended character set covering approximate and indefinite quantity words
  (半 双 雙 几 幾 数 數 无 無), which raises the poem-level rate to 73.4%.
- Figures, derived dataset, and documentation.

### Preserved unchanged
- `archive/original/本地验证脚本.py`, the July 2026 script, exactly as written
  (SHA-256 `b63d062b8d8e45c72524bf5d191bdb5d497f473ce383930c73375202c71f4450`).
