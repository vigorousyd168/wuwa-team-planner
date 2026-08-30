import json, sys, os, re, pathlib
sys.stdout.reconfigure(encoding='utf-8')

BASE    = pathlib.Path(__file__).parent
IMG_DIR = BASE / 'wuwa-wiki' / 'images'
JS_OUT  = BASE / 'js' / 'data.js'
IMG_REL = './wuwa-wiki/images'

# ── Character data ────────────────────────────────────────────────────────────
with open(BASE / 'wuwa-wiki' / 'characters.json', encoding='utf-8') as f:
    chars = json.load(f)

SUSTAIN_NAMES = {'守岸人', '莫宁', '维里奈', '卜灵', '白芷', '穗穗'}

characters = []
for c in chars:
    entry = {
        'id':      c['id'],
        'name':    c['name'],
        'element': c['element'],
        'star':    c['star'],
        'img':     f"{IMG_REL}/{c['img']}",
    }
    if c['name'] in SUSTAIN_NAMES:
        entry['sustain'] = True
    characters.append(entry)

# ── Element icon paths ────────────────────────────────────────────────────────
elem_icons = {}
for f in os.listdir(IMG_DIR):
    m = re.search(r'ico-catalog-role-attr-([a-z]+)', f)
    if m:
        elem_icons[m.group(1)] = f"{IMG_REL}/{f}"

chars_json = json.dumps(characters, ensure_ascii=False)
icons_json = json.dumps(elem_icons)

with open(JS_OUT, 'w', encoding='utf-8') as f:
    f.write(f'const CHARACTERS = {chars_json};\n')
    f.write(f'const ELEM_ICONS = {icons_json};\n')

print(f'Written: {JS_OUT}')
print(f'File size: {os.path.getsize(JS_OUT)/1024:.1f} KB')
