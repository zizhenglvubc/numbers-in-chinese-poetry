# -*- coding: utf-8 -*-
# 用法:把本脚本放在解压出的 cp 文件夹【旁边】(不是里面),终端运行: python3 本地验证脚本.py
import json, glob, os, time
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cp')
NUM = set('一二三四五六七八九十百千万萬亿億两兩零廿卅')
groups = {
 '唐诗':          sorted(glob.glob(f'{BASE}/全唐诗/poet.tang.*.json')),
 '宋诗(1/3抽样)': sorted(glob.glob(f'{BASE}/全唐诗/poet.song.*.json')),
 '宋词':          sorted(glob.glob(f'{BASE}/宋词/ci.song.*.json')),
 '元曲':          glob.glob(f'{BASE}/元曲/yuanqu.json'),
 '五代诗词':      glob.glob(f'{BASE}/五代诗词/*/*.json'),
 '清词(纳兰)':    glob.glob(f'{BASE}/纳兰性德/*.json'),
}
t0 = time.time(); W = H = 0
if not os.path.isdir(BASE):
    print('!! 没找到 cp 文件夹,请确认脚本和解压出的 cp 在同一目录'); raise SystemExit
for name, files in groups.items():
    tot = hit = 0
    print(f'\n=== {name} ({len(files)} 个文件) ===')
    for f in files:
        n = h = 0
        try: data = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            print(f'  跳过 {os.path.basename(f)}: {e}'); continue
        if isinstance(data, dict): data = data.get('poems') or data.get('content') or []
        for p in data:
            if not isinstance(p, dict): continue
            v = None
            for k in ('paragraphs','content','para','poem','text'):
                v = p.get(k)
                if v: break
            t = ''.join(v) if isinstance(v, list) else (str(v) if v else '')
            if not t: continue
            n += 1
            if set(t) & NUM: h += 1
        tot += n; hit += h
        print(f'  {os.path.basename(f):28s} {n:5d} 首, 含数字 {h:5d}')
    W += tot; H += hit
    if tot: print(f'  -- {name} 小计: {tot} 首, 含数字 {hit} ({hit/tot*100:.1f}%)')
print(f'\n================ 总计 ================')
print(f'{W} 首, 含数字 {H} ({H/W*100:.2f}%), 用时 {time.time()-t0:.1f} 秒')
print('对照参考值: 175355 首, 含数字 103885 (59.24%)')
