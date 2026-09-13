# -*- coding: utf-8 -*-
"""
make_figures.py — figures for "Numbers in Chinese Poetry from the Tang Dynasty Onward"
Author: Zizheng Lv

Figure 1 plots poem-level rates, figure 2 character-level rates.
"""
import argparse, json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

LABELS = {
    'tang_shi': 'Tang shi\n(Complete Tang Poems)',
    'song_shi_1_3': 'Song shi\n(1/3 subset)',
    'song_ci': 'Song ci',
    'yuan_qu': 'Yuan qu',
    'wudai': 'Five Dynasties',
    'nalan_qing_ci': 'Qing ci\n(Nalan Xingde)',
}
INK, ACCENT, MUTED = '#1a1a1a', '#8c4a2f', '#9a9a9a'
AUTHOR = 'Zizheng Lv'


def style(ax):
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(colors=INK, labelsize=9)
    ax.set_axisbelow(True)
    ax.grid(axis='y', color='#e6e6e6', lw=.8)


def bars(ax, groups, values, title, subtitle, fmt, ylabel):
    xs = range(len(groups))
    ax.bar(xs, values, color=ACCENT, width=.62)
    for x, v in zip(xs, values):
        ax.text(x, v, fmt(v), ha='center', va='bottom', fontsize=9, color=INK)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([LABELS.get(g, g) for g in groups], fontsize=8.5)
    ax.set_ylabel(ylabel, fontsize=9, color=INK)
    ax.set_ylim(0, max(values) * 1.22)
    ax.set_title(title, fontsize=12, color=INK, loc='left', pad=26, weight='bold')
    ax.text(0, 1.015, subtitle, transform=ax.transAxes, fontsize=8.5, color=MUTED)
    style(ax)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', default='results')
    ap.add_argument('--out', default='figures')
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    base = json.load(open(os.path.join(args.results, 'summary.json'), encoding='utf-8'))
    groups = [g['group_id'] for g in base['groups']]

    # Figure 1 — poem-level rate
    fig, ax = plt.subplots(figsize=(9, 4.6))
    bars(ax, groups, [g['poem_level_rate'] * 100 for g in base['groups']],
         'Share of poems containing at least one numeral character',
         f"{base['totals']['poems']:,} poems · "
         f"overall {base['totals']['poem_level_rate']*100:.2f}%",
         lambda v: f'{v:.1f}%', 'Poems with a numeral (%)')
    fig.tight_layout()
    fig.savefig(os.path.join(args.out, 'fig1_poem_level_rate.png'), dpi=200,
                metadata={'Software': AUTHOR})
    fig.savefig(os.path.join(args.out, 'fig1_poem_level_rate.svg'),
                metadata={'Creator': AUTHOR, 'Date': None})
    plt.close(fig)

    # Figure 2 — character-level rate
    ext_path = os.path.join(args.results, 'summary_extended.json')
    if os.path.exists(ext_path):
        ext = json.load(open(ext_path, encoding='utf-8'))
        chars = sum(g['EXT_total_chars'] for g in ext['groups'])
        nums = sum(g['EXT_numeral_chars'] for g in ext['groups'])
        fig, ax = plt.subplots(figsize=(9, 4.6))
        bars(ax, groups, [g['EXT_char_level_rate'] * 100 for g in ext['groups']],
             'Numeral characters as a share of all characters',
             f'Extended analysis · overall {nums/chars*100:.2f}% '
             f'({nums:,} of {chars:,} characters)',
             lambda v: f'{v:.2f}%', 'Numeral characters (%)')
        fig.tight_layout()
        fig.savefig(os.path.join(args.out, 'fig2_character_level_rate.png'), dpi=200,
                    metadata={'Software': AUTHOR})
        fig.savefig(os.path.join(args.out, 'fig2_character_level_rate.svg'),
                    metadata={'Creator': AUTHOR, 'Date': None})
        plt.close(fig)
    print('figures written to', args.out)


if __name__ == '__main__':
    main()
