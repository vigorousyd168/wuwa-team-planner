"""Sync the character roster from the kurobbs wiki.

Usage:
    python update_roster.py                 # dry run: list new/changed characters
    python update_roster.py --add 名字A 名字B  # add the named characters
    python update_roster.py --add-all       # add every new character

Fetches the character catalogue from the kurobbs API (the wiki page itself is
a JS-rendered SPA and returns no data to a plain fetch), diffs it against
wuwa-wiki/characters.json, and on --add: downloads portraits, appends entries,
and reruns generate.py.
"""
import argparse, json, pathlib, subprocess, sys, urllib.parse, urllib.request

sys.stdout.reconfigure(encoding='utf-8')

BASE = pathlib.Path(__file__).resolve().parents[3]  # repo root
CHARS_JSON = BASE / 'wuwa-wiki' / 'characters.json'
IMG_DIR = BASE / 'wuwa-wiki' / 'images'

API_URL = 'https://api.kurobbs.com/wiki/core/catalogue/item/getPage'
CATALOGUE_ID = 1105  # 共鸣者 catalogue (from wiki URL ?fid=1099&sid=1105)

# skillAttr codes, verified against all pre-existing characters.
# The wiki calls attr 4 冰凝; this project standardizes on 冷凝.
ATTR_ELEMENT = {'2': '气动', '3': '导电', '4': '冷凝', '5': '热熔', '6': '衍射', '7': '湮灭'}


def norm(name):
    """Wiki uses 「·」 where local data uses 「-」 (e.g. 秧秧·玄翎 vs 秧秧-玄翎)."""
    return name.replace('·', '-')


def fetch_wiki():
    body = urllib.parse.urlencode({'catalogueId': CATALOGUE_ID, 'page': 1, 'limit': 500}).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        'wiki_type': '9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0',
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.load(r)
    if d.get('code') != 200:
        sys.exit(f'API error: code={d.get("code")} msg={d.get("msg")}')
    entries = []
    for rec in d['data']['results']['records']:
        c = rec.get('content', {})
        url = c.get('contentUrl', '')
        attr = str(c.get('skillAttr', ''))
        if not url or attr not in ATTR_ELEMENT:
            continue
        entries.append({
            'name': rec['name'],
            'element': ATTR_ELEMENT[attr],
            'star': int(c.get('star', 0)),
            'img': url.rsplit('/', 1)[-1],
            'url': url,
        })
    return entries


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--add', nargs='+', metavar='NAME', help='add these characters (wiki name)')
    ap.add_argument('--add-all', action='store_true', help='add every new character')
    args = ap.parse_args()

    local = json.loads(CHARS_JSON.read_text(encoding='utf-8'))
    local_by_name = {norm(c['name']): c for c in local}
    wiki = fetch_wiki()

    new = [w for w in wiki if norm(w['name']) not in local_by_name]
    print(f'wiki: {len(wiki)} characters, local: {len(local)}, new: {len(new)}')
    for w in new:
        print(f"  NEW  {w['name']}  {w['element']}  {w['star']}★  {w['img']}")
    for w in wiki:
        known = local_by_name.get(norm(w['name']))
        if known and known['img'] != w['img']:
            print(f"  IMG-CHANGED  {w['name']}  local={known['img']}  wiki={w['img']}")

    if not (args.add or args.add_all):
        print('\nDry run — rerun with --add NAME... or --add-all to apply.')
        return
    wanted = {norm(n) for n in args.add} if args.add else {norm(w['name']) for w in new}
    missing = wanted - {norm(w['name']) for w in new}
    if missing:
        sys.exit(f'Not found among new wiki characters: {missing}')

    next_id = max(c['id'] for c in local) + 1
    for w in new:
        if norm(w['name']) not in wanted:
            continue
        dest = IMG_DIR / w['img']
        if dest.exists():
            print(f"image exists, keeping: {w['img']}")
        else:
            req = urllib.request.Request(w['url'], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as r:
                dest.write_bytes(r.read())
            print(f"downloaded: {w['img']} ({dest.stat().st_size/1024:.0f} KB)")
        local.append({'id': next_id, 'name': w['name'], 'element': w['element'],
                      'star': w['star'], 'img': w['img']})
        print(f"added: id={next_id} {w['name']} {w['element']} {w['star']}★")
        next_id += 1

    CHARS_JSON.write_text(json.dumps(local, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    subprocess.run([sys.executable, str(BASE / 'generate.py')], check=True)


if __name__ == '__main__':
    main()
