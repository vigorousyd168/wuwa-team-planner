import json, sys, os, re, pathlib
sys.stdout.reconfigure(encoding='utf-8')

BASE     = pathlib.Path(__file__).parent
IMG_DIR  = BASE / 'wuwa-wiki' / 'images'
HTML_OUT = BASE / 'index.html'
IMG_REL  = './wuwa-wiki/images'

# ── Character data ────────────────────────────────────────────────────────────
with open(BASE / 'wuwa-wiki' / 'characters.json', encoding='utf-8') as f:
    chars = json.load(f)

SUSTAIN_NAMES = {'守岸人', '莫宁', '维里奈', '卜灵', '白芷'}

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

# ── HTML template ─────────────────────────────────────────────────────────────
HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>鸣潮编队小助手</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
<style>
html, body { margin: 0; padding: 0; height: 100%; background: #0a0e17; }
* { box-sizing: border-box; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #283655; border-radius: 3px; }
input::placeholder, textarea::placeholder { color: #5d6f96; }
button { font-family: inherit; }
@keyframes ccPulse {
  0%, 100% { box-shadow: 0 0 0 1.5px rgba(63,214,228,.95), 0 0 12px rgba(63,214,228,.35); }
  50%       { box-shadow: 0 0 0 1.5px rgba(63,214,228,.95), 0 0 24px rgba(63,214,228,.8); }
}
#app {
  height: 100vh; display: flex; flex-direction: column; overflow: hidden;
  background: radial-gradient(1100px 560px at 82% -12%, #15233f 0%, #0a0e17 58%);
  color: #e4ecfc; font-family: 'Rajdhani','PingFang SC','Microsoft YaHei',sans-serif; font-size: 13px;
}
header {
  display: flex; align-items: center; gap: 14px; padding: 0 20px; height: 58px;
  flex-shrink: 0; background: rgba(13,19,35,.85); border-bottom: 1px solid #1f2b47;
}
.hdr-diamond {
  width: 12px; height: 12px; background: linear-gradient(135deg,#3fd6e4,#1690a4);
  transform: rotate(45deg); box-shadow: 0 0 10px rgba(63,214,228,.6); flex-shrink: 0;
}
.hdr-titles { display: flex; flex-direction: column; gap: 1px; min-width: 0; }
.hdr-title  { font-size: 16px; font-weight: 600; letter-spacing: 2px; color: #eef4ff; white-space: nowrap; }
.hdr-sub    { font-size: 10px; font-weight: 600; letter-spacing: 3px; color: #3fd6e4;  white-space: nowrap; }
.hdr-stats  { margin-left: auto; display: flex; gap: 8px; align-items: center; }
.stat-pill  {
  display: flex; align-items: baseline; gap: 5px; padding: 4px 12px;
  border: 1px solid #243154; border-radius: 999px; background: rgba(15,22,40,.7);
  font-size: 12px; color: #8294b8; white-space: nowrap;
}
.stat-pill b { color: #3fd6e4; font-weight: 700; font-size: 14px; }
#mob-tabs {
  display: none; flex-shrink: 0; border-bottom: 1px solid #1f2b47;
  background: rgba(13,19,35,.85);
}
.mob-tab {
  flex: 1; text-align: center; padding: 11px 8px; font-size: 13px; font-weight: 600;
  letter-spacing: 1px; cursor: pointer; color: #8294b8; border-bottom: 2px solid transparent;
  user-select: none;
}
.mob-tab.active { color: #3fd6e4; border-bottom-color: #3fd6e4; }
#layout { display: flex; flex: 1; overflow: hidden; min-height: 0; }
aside {
  display: flex; flex-direction: column; width: 372px; flex-shrink: 0; min-width: 0;
  border-right: 1px solid #1f2b47; background: rgba(13,19,33,.6); overflow: hidden;
}
.sb-top { display: flex; flex-direction: column; gap: 10px; padding: 14px 14px 12px; border-bottom: 1px solid #1f2b47; }
.sb-row { display: flex; align-items: baseline; gap: 8px; }
.sb-title { font-size: 14px; font-weight: 600; letter-spacing: 1px; color: #dfe9fb; }
.sb-sub   { font-size: 10px; font-weight: 600; letter-spacing: 2px; color: #5d6f96; }
.sb-count { margin-left: auto; font-size: 11px; color: #8294b8; white-space: nowrap; }
#search {
  width: 100%; background: #0e1526; border: 1px solid #243154; border-radius: 8px;
  padding: 8px 12px; font-size: 13px; color: #e4ecfc; outline: none;
  font-family: inherit; transition: border-color .15s;
}
#search:focus { border-color: #3fd6e4; }
#elem-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.chip {
  display: flex; align-items: center; gap: 5px; padding: 4px 10px; border-radius: 999px;
  font-size: 12px; cursor: pointer; user-select: none; transition: all .15s;
}
.chip img { width: 13px; height: 13px; display: block; }
#roster {
  flex: 1; overflow-y: auto; padding: 12px;
  display: grid; grid-template-columns: repeat(auto-fill, minmax(96px, 1fr));
  grid-auto-rows: max-content; gap: 10px; align-content: start; transition: background .15s;
}
#roster.rz-over { background: rgba(63,214,228,.05); }
.cc {
  position: relative; aspect-ratio: 3/4; border-radius: 10px; overflow: hidden;
  border: 1px solid #26334f; background: linear-gradient(180deg,#16213c 0%,#0d1426 100%);
  cursor: pointer; user-select: none; transition: border-color .15s, transform .12s;
}
.cc:not(.used):hover { border-color: #3fd6e4; transform: translateY(-2px); }
.cc.selected { border-color: #3fd6e4; animation: ccPulse 1.6s ease-in-out infinite; }
.cc.used { opacity: .38; filter: grayscale(.7); cursor: default; }
.cc img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
.cc .cc-star {
  position: absolute; top: 6px; left: 6px; padding: 1px 6px; border-radius: 4px;
  font-size: 11px; font-weight: 700; color: #131725;
}
.cc.s5 .cc-star { background: linear-gradient(135deg,#ffd87a,#e8a93c); }
.cc.s4 .cc-star { background: linear-gradient(135deg,#cfa8ff,#9f6cf0); }
.cc .cc-sustain {
  position: absolute; top: 6px; right: 6px; padding: 1px 6px; border-radius: 4px;
  font-size: 10px; font-weight: 700; background: rgba(63,220,171,.92); color: #06281e;
}
.cc .cc-foot {
  position: absolute; bottom: 0; left: 0; right: 0;
  display: flex; align-items: center; gap: 4px; padding: 14px 7px 5px;
  background: linear-gradient(180deg,rgba(5,8,16,0) 0%,rgba(5,8,16,.92) 55%);
}
.cc .cc-name { flex: 1; font-size: 12px; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cc .cc-elem { width: 14px; height: 14px; flex-shrink: 0; }
.unavail-sec {
  flex-shrink: 0; display: flex; flex-direction: column; gap: 8px;
  padding: 10px 14px 12px; border-top: 1px solid #1f2b47; background: rgba(10,14,26,.55);
}
.unavail-sec-row { display: flex; align-items: baseline; gap: 8px; }
.unavail-title  { font-size: 13px; font-weight: 600; letter-spacing: 1px; color: #aab8d6; }
.unavail-sub    { font-size: 10px; font-weight: 600; letter-spacing: 2px; color: #5d6f96; }
.unavail-cnt    { margin-left: auto; font-size: 11px; color: #8294b8; }
#unavail-zone {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
  grid-auto-rows: max-content; gap: 8px; max-height: 138px; overflow-y: auto;
  min-height: 56px; border: 1px dashed #2a3858; border-radius: 10px; padding: 7px;
  transition: border-color .15s, background .15s;
}
#unavail-zone.uz-over { border-color: #3fd6e4; background: rgba(63,214,228,.07); }
.uz-empty {
  grid-column: 1 / -1; min-height: 40px; display: flex; align-items: center;
  justify-content: center; color: #5d6f96; font-size: 12px; pointer-events: none;
}
.uc {
  position: relative; aspect-ratio: 3/4; border-radius: 8px; overflow: hidden;
  border: 1px solid #243154; background: #0d1426; opacity: .62;
  cursor: pointer; user-select: none; transition: opacity .15s, border-color .15s;
}
.uc:hover { opacity: 1; border-color: #3fd6e4; }
.uc img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; filter: grayscale(.75); }
.uc .uc-name {
  position: absolute; bottom: 0; left: 0; right: 0; padding: 8px 4px 3px;
  font-size: 10px; text-align: center; color: #cfdbf3; white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis;
  background: linear-gradient(180deg,rgba(5,8,16,0) 0%,rgba(5,8,16,.95) 60%);
}
.unavail-hint { font-size: 11px; color: #5d6f96; }
main { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 0; }
.teams-bar {
  display: flex; align-items: center; gap: 12px; padding: 12px 18px;
  border-bottom: 1px solid #1f2b47; flex-shrink: 0;
}
.teams-bar-left { display: flex; align-items: baseline; gap: 8px; }
.teams-bar-title { font-size: 14px; font-weight: 600; letter-spacing: 1px; color: #dfe9fb; }
.teams-bar-sub   { font-size: 10px; font-weight: 600; letter-spacing: 2px; color: #5d6f96; }
.teams-bar-hint  { font-size: 12px; color: #8294b8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
#add-btn {
  margin-left: auto; padding: 8px 18px; border-radius: 8px; border: none;
  background: linear-gradient(135deg,#2ed3e2,#149aac); color: #03171b;
  font-size: 13px; font-weight: 700; letter-spacing: 1px;
  cursor: pointer; transition: filter .15s; white-space: nowrap; flex-shrink: 0;
}
#add-btn:hover:not(:disabled) { filter: brightness(1.12); }
#add-btn:disabled { opacity: .4; cursor: not-allowed; }
#sel-banner {
  display: none; align-items: center; gap: 12px; padding: 9px 18px; flex-shrink: 0;
  background: rgba(63,214,228,.07); border-bottom: 1px solid rgba(63,214,228,.3); font-size: 12px;
}
.sel-dia { width: 8px; height: 8px; background: #3fd6e4; transform: rotate(45deg); flex-shrink: 0; box-shadow: 0 0 8px rgba(63,214,228,.8); }
.sel-text { color: #bfeef4; }
.sel-actions { margin-left: auto; display: flex; gap: 8px; }
.sel-btn {
  padding: 5px 12px; border-radius: 6px; border: 1px solid #3a4a6e;
  background: rgba(15,22,40,.8); color: #aab8d6; font-size: 12px; cursor: pointer;
  transition: border-color .15s, color .15s;
}
.sel-btn.mark:hover   { border-color: #ff5e7a; color: #ff8aa0; }
.sel-btn.cancel:hover { border-color: #3fd6e4; color: #fff; }
#teams {
  flex: 1; overflow-y: auto; padding: 14px 18px 24px;
  display: flex; flex-direction: column; gap: 10px;
}
.no-teams {
  flex: 1; display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 8px; color: #5d6f96;
}
.no-teams-t { font-size: 15px; letter-spacing: 1px; }
.no-teams-s { font-size: 12px; }
.team-row {
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap; padding: 10px 14px;
  border-radius: 12px; border: 1px solid #22304e;
  background: linear-gradient(180deg,rgba(21,30,54,.85) 0%,rgba(14,21,38,.85) 100%);
  transition: border-color .15s, box-shadow .15s;
}
.team-row.tr-over { border-color: #3fd6e4; box-shadow: 0 0 0 1px rgba(63,214,228,.7), 0 0 18px rgba(63,214,228,.25); }
.drag-handle {
  cursor: grab; color: #51638f; font-size: 17px; padding: 6px 2px;
  user-select: none; line-height: 1; flex-shrink: 0; transition: color .15s;
}
.drag-handle:hover { color: #3fd6e4; }
.team-num { display: flex; flex-direction: column; align-items: center; width: 50px; flex-shrink: 0; }
.team-num-label { font-size: 9px; font-weight: 600; letter-spacing: 2.5px; color: #5d6f96; }
.team-num-val   { font-size: 22px; font-weight: 700; color: #3fd6e4; line-height: 1.1; }
.slots { display: flex; gap: 8px; flex-shrink: 0; }
.slot {
  position: relative; width: 74px; height: 74px; border-radius: 10px; overflow: hidden;
  border: 1px dashed #2a3858; background: #0c1322; cursor: pointer;
  transition: border-color .15s, background .15s;
}
.slot.s-over   { border-color: #3fd6e4; border-style: solid; background: rgba(63,214,228,.1); }
.slot.s-place  { border-color: rgba(63,214,228,.55); }
.slot.s-filled { border-style: solid; border-color: #2a3858; background: #0d1426; }
.slot-plus {
  position: absolute; inset: 0; display: flex; align-items: center;
  justify-content: center; font-size: 24px; color: #2a3858; user-select: none;
}
.slot.s-over .slot-plus, .slot.s-place .slot-plus { color: #3fd6e4; }
.slot img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
.slot-name {
  position: absolute; bottom: 0; left: 0; right: 0; padding: 8px 4px 3px;
  font-size: 10px; text-align: center; color: #fff; white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis;
  background: linear-gradient(180deg,rgba(5,8,16,0) 0%,rgba(5,8,16,.92) 60%);
}
.slot-clear {
  position: absolute; top: 3px; right: 3px; width: 17px; height: 17px; border-radius: 50%;
  border: none; background: rgba(4,7,14,.7); color: #cfdbf3; font-size: 10px; line-height: 1;
  cursor: pointer; display: none; align-items: center; justify-content: center; padding: 0;
  transition: background .15s, color .15s;
}
.slot.s-filled:hover .slot-clear { display: flex; }
.slot-clear:hover { background: #ff4d6d; color: #fff; }
.team-note {
  flex: 1; min-width: 150px; height: 74px; background: #0d1424; border: 1px solid #243154;
  border-radius: 8px; padding: 8px 10px; font-size: 12px; color: #cfdbf3; resize: none;
  outline: none; line-height: 1.5; transition: border-color .15s;
}
.team-note:focus { border-color: #3fd6e4; }
.team-del {
  flex-shrink: 0; width: 30px; height: 30px; background: transparent;
  border: 1px solid transparent; color: #5d6f96; font-size: 14px; cursor: pointer;
  border-radius: 8px; display: flex; align-items: center; justify-content: center; padding: 0;
  transition: color .15s, border-color .15s;
}
.team-del:hover { color: #ff5e7a; border-color: #ff5e7a; }
@media (max-width: 780px) {
  #mob-tabs { display: flex; }
  aside { width: 100%; border-right: none; }
  aside.m-hide, main.m-hide { display: none; }
}
</style>
</head>
<body>
<div id="app">
  <header>
    <div class="hdr-diamond"></div>
    <div class="hdr-titles">
      <div class="hdr-title">鸣潮编队小助手</div>
      <div class="hdr-sub">WUTHERING WAVES · TEAM BUILDER</div>
    </div>
    <div class="hdr-stats">
      <div class="stat-pill"><span>已获得</span><b id="h-owned">0</b><span>/ <span id="h-total">0</span></span></div>
      <div class="stat-pill"><span>队伍</span><b id="h-teams">0</b><span>/ 20</span></div>
    </div>
  </header>
  <div id="mob-tabs">
    <div class="mob-tab" id="tab-roster" onclick="setTab('roster')">角色库 ROSTER</div>
    <div class="mob-tab active" id="tab-teams" onclick="setTab('teams')">队伍 TEAMS</div>
  </div>
  <div id="layout">
    <aside id="sidebar">
      <div class="sb-top">
        <div class="sb-row">
          <span class="sb-title">角色库</span>
          <span class="sb-sub">ROSTER</span>
          <span class="sb-count" id="roster-count"></span>
        </div>
        <input type="text" id="search" placeholder="搜索角色 Search…">
        <div id="elem-chips"></div>
      </div>
      <div id="roster"></div>
      <div class="unavail-sec">
        <div class="unavail-sec-row">
          <span class="unavail-title">未获得</span>
          <span class="unavail-sub">UNOBTAINED</span>
          <span class="unavail-cnt" id="unavail-count"></span>
        </div>
        <div id="unavail-zone"></div>
        <div class="unavail-hint">点击卡片取回 · Click a card to restore</div>
      </div>
    </aside>
    <main id="main">
      <div class="teams-bar">
        <div class="teams-bar-left">
          <span class="teams-bar-title">队伍配置</span>
          <span class="teams-bar-sub">TEAMS</span>
        </div>
        <span class="teams-bar-hint">拖动 ⠿ 调整顺序</span>
        <button id="add-btn">＋ 添加队伍 ADD</button>
      </div>
      <div id="sel-banner">
        <span class="sel-dia"></span>
        <span class="sel-text">已选择 <strong id="sel-name"></strong> — 点击队伍空位放入 · Tap an empty slot to place</span>
        <div class="sel-actions">
          <button class="sel-btn mark" id="sel-mark">标记为未获得</button>
          <button class="sel-btn cancel" id="sel-cancel">取消 ✕</button>
        </div>
      </div>
      <div id="teams"></div>
    </main>
  </div>
</div>
<script>
const CHARACTERS = """ + "<<<CHARS>>>" + """;
const ELEM_ICONS = """ + "<<<ICONS>>>" + """;

const ELEM_MAP = {
  '冰凝': { key: 'bingning', color: '#56b7ff' },
  '气动': { key: 'qidong',   color: '#3fdcab' },
  '导电': { key: 'daodian',  color: '#b88cff' },
  '热熔': { key: 'rerong',   color: '#ff8a4d' },
  '湮灭': { key: 'jielin',   color: '#ff6597' },
  '衍射': { key: 'yanshe',   color: '#ffd35e' }
};
const ELEM_ORDER = ['冰凝','气动','导电','热熔','湮灭','衍射'];
const BY_ID = new Map(CHARACTERS.map(c => [c.id, c]));
const PRESET_UNAVAIL = [4,5,6,9,10,11,13,16,17,18,19,21,22,25,29];

let state = { teams: [], notes: [], unavailableIds: [] };
let unavailSet = new Set();
let dragId = null, dragFrom = null, dragTeam = null;
let selId = null;
let searchQ = '', elemF = null;
let activeTab = 'teams';

function save() {
  localStorage.setItem('wuwa-deck-state', JSON.stringify(state));
}
function load() {
  try {
    const raw = localStorage.getItem('wuwa-deck-state');
    if (raw) {
      const p = JSON.parse(raw);
      if (Array.isArray(p.teams) && p.teams.length) {
        state.teams = p.teams.map(r => [r[0]??null, r[1]??null, r[2]??null]);
        state.notes = Array.isArray(p.notes) ? p.notes.slice() : [];
        while (state.notes.length < state.teams.length) state.notes.push('');
        state.unavailableIds = Array.isArray(p.unavailableIds) ? p.unavailableIds.slice() : PRESET_UNAVAIL.slice();
        return;
      }
    }
  } catch(e) { console.warn('wuwa-deck: load failed', e); }
  state.teams = Array.from({length: 6}, () => [null,null,null]);
  state.notes = Array(6).fill('');
  state.unavailableIds = PRESET_UNAVAIL.slice();
}
function useCounts() {
  const m = {};
  state.teams.flat().forEach(id => { if (id != null) m[id] = (m[id]||0) + 1; });
  return m;
}
function threshold(c) { return c.sustain ? 2 : 1; }
function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function place(ti, si, id) {
  state.teams[ti][si] = id; selId = null; save(); renderAll();
}
function clearSlot(ti, si) {
  state.teams[ti][si] = null; save(); renderAll();
}
function markUnavailable(id) {
  if (unavailSet.has(id)) return;
  state.unavailableIds.push(id); unavailSet.add(id);
  if (selId === id) selId = null;
  save(); renderAll();
}
function restore(id) {
  const i = state.unavailableIds.indexOf(id);
  if (i > -1) state.unavailableIds.splice(i, 1);
  unavailSet.delete(id); save(); renderAll();
}
function moveTeam(from, to) {
  if (from === to) return;
  const [t] = state.teams.splice(from, 1);
  const [n] = state.notes.splice(from, 1);
  state.teams.splice(to, 0, t);
  state.notes.splice(to, 0, n);
  save(); renderAll();
}
function renderHeader() {
  const owned = CHARACTERS.filter(c => !unavailSet.has(c.id)).length;
  document.getElementById('h-owned').textContent = owned;
  document.getElementById('h-total').textContent = CHARACTERS.length;
  document.getElementById('h-teams').textContent = state.teams.length;
}
function renderElemChips() {
  const el = document.getElementById('elem-chips');
  el.innerHTML = ELEM_ORDER.map(name => {
    const e = ELEM_MAP[name];
    const active = elemF === name;
    const border = active ? e.color : '#243154';
    const bg     = active ? e.color + '26' : '#0e1526';
    const color  = active ? '#ffffff' : '#8294b8';
    const ic = ELEM_ICONS[e.key] || '';
    return `<div class="chip" data-elem="${esc(name)}" style="border:1px solid ${border};background:${bg};color:${color}">` +
      (ic ? `<img src="${esc(ic)}" alt="">` : '') +
      `<span>${esc(name)}</span></div>`;
  }).join('');
  el.querySelectorAll('.chip').forEach(ch => {
    ch.addEventListener('click', () => {
      elemF = elemF === ch.dataset.elem ? null : ch.dataset.elem;
      renderElemChips(); renderRoster();
    });
  });
}
function renderRoster() {
  const counts = useCounts();
  const owned = CHARACTERS.filter(c => !unavailSet.has(c.id));
  const avail = owned.filter(c => (counts[c.id]||0) < threshold(c));
  document.getElementById('roster-count').textContent = avail.length + ' 可用 / ' + owned.length + ' 已获得';
  const filtered = owned
    .filter(c => !searchQ || c.name.includes(searchQ))
    .filter(c => !elemF || c.element === elemF);
  const grid = document.getElementById('roster');
  grid.innerHTML = filtered.map(c => {
    const e = ELEM_MAP[c.element] || {};
    const ic = ELEM_ICONS[e.key] || '';
    const full = (counts[c.id]||0) >= threshold(c);
    const sel  = selId === c.id;
    let cls = 'cc s' + c.star;
    if (full) cls += ' used';
    if (sel)  cls += ' selected';
    return `<div class="${cls}" data-id="${c.id}" ${!full ? 'draggable="true"' : ''}
      title="${esc(c.name)}（${esc(c.element)} · ${c.star}★）${full ? '已编入上限' : '点击选择或拖入队伍'}">
      <img src="${esc(c.img)}" alt="${esc(c.name)}" draggable="false">
      <span class="cc-star">${c.star}★</span>
      ${c.sustain ? '<span class="cc-sustain">辅 ×2</span>' : ''}
      <div class="cc-foot">
        <span class="cc-name">${esc(c.name)}</span>
        ${ic ? `<img class="cc-elem" src="${esc(ic)}" alt="">` : ''}
      </div>
    </div>`;
  }).join('');
  grid.querySelectorAll('.cc:not(.used)').forEach(card => {
    card.addEventListener('dragstart', e => {
      dragId = parseInt(card.dataset.id); dragFrom = 'roster';
      e.dataTransfer.effectAllowed = 'move';
      try { e.dataTransfer.setData('text/plain', String(dragId)); } catch(_) {}
    });
    card.addEventListener('dragend', () => {
      dragId = null; dragFrom = null; grid.classList.remove('rz-over');
    });
    card.addEventListener('click', () => {
      const id = parseInt(card.dataset.id);
      selId = selId === id ? null : id;
      if (selId !== null && isMobile()) setTab('teams');
      renderRoster(); renderTeams(); renderSelBanner();
    });
  });
}
function renderUnavail() {
  const chars = CHARACTERS.filter(c => unavailSet.has(c.id));
  document.getElementById('unavail-count').textContent = chars.length + ' / ' + CHARACTERS.length;
  const zone = document.getElementById('unavail-zone');
  if (chars.length === 0) {
    zone.innerHTML = '<div class="uz-empty">拖入角色以标记为未获得</div>';
    return;
  }
  zone.innerHTML = chars.map(c =>
    `<div class="uc" data-id="${c.id}" draggable="true" title="${esc(c.name)} — 点击取回到角色库">
      <img src="${esc(c.img)}" alt="${esc(c.name)}" draggable="false">
      <div class="uc-name">${esc(c.name)}</div>
    </div>`
  ).join('');
  zone.querySelectorAll('.uc').forEach(card => {
    card.addEventListener('click', () => restore(parseInt(card.dataset.id)));
    card.addEventListener('dragstart', e => {
      dragId = parseInt(card.dataset.id); dragFrom = 'unavail';
      e.dataTransfer.effectAllowed = 'move';
      try { e.dataTransfer.setData('text/plain', String(dragId)); } catch(_) {}
    });
    card.addEventListener('dragend', () => {
      dragId = null; dragFrom = null; zone.classList.remove('uz-over');
    });
  });
}
function renderSelBanner() {
  const banner = document.getElementById('sel-banner');
  if (selId != null) {
    const c = BY_ID.get(selId);
    document.getElementById('sel-name').textContent = c ? c.name : '';
    banner.style.display = 'flex';
  } else {
    banner.style.display = 'none';
  }
}
function renderSlot(ti, si, cid) {
  const c = cid != null ? BY_ID.get(cid) : null;
  if (!c) return `<div class="slot" data-si="${si}"><div class="slot-plus">＋</div></div>`;
  return `<div class="slot s-filled" data-si="${si}">
    <img src="${esc(c.img)}" alt="${esc(c.name)}">
    <div class="slot-name">${esc(c.name)}</div>
    <button class="slot-clear" data-ti="${ti}" data-si="${si}">✕</button>
  </div>`;
}
function renderTeams() {
  const container = document.getElementById('teams');
  const addBtn = document.getElementById('add-btn');
  if (state.teams.length === 0) {
    container.innerHTML = `<div class="no-teams">
      <div class="no-teams-t">还没有队伍</div>
      <div class="no-teams-s">点击右上角「添加队伍」开始编队</div>
    </div>`;
    addBtn.disabled = false; addBtn.style.opacity = '1';
    return;
  }
  container.innerHTML = state.teams.map((slots, ti) => {
    const num = ('0' + (ti + 1)).slice(-2);
    return `<div class="team-row" data-ti="${ti}">
      <div class="drag-handle" draggable="true" data-ti="${ti}" title="拖动排序">⠿</div>
      <div class="team-num">
        <span class="team-num-label">TEAM</span>
        <span class="team-num-val">${num}</span>
      </div>
      <div class="slots">${slots.map((cid, si) => renderSlot(ti, si, cid)).join('')}</div>
      <textarea class="team-note" data-ti="${ti}" placeholder="队伍备注 Notes…">${esc(state.notes[ti]||'')}</textarea>
      <button class="team-del" data-ti="${ti}" title="删除此队伍">✕</button>
    </div>`;
  }).join('');
  container.querySelectorAll('.slot').forEach(slot => {
    const row = slot.closest('.team-row');
    slot.addEventListener('click', () => {
      if (selId != null) place(parseInt(row.dataset.ti), parseInt(slot.dataset.si), selId);
    });
    slot.addEventListener('dragover', e => {
      if (dragId != null && dragFrom === 'roster') {
        e.preventDefault(); e.dataTransfer.dropEffect = 'move';
        slot.classList.add('s-over');
      }
    });
    slot.addEventListener('dragleave', e => {
      if (!slot.contains(e.relatedTarget)) slot.classList.remove('s-over');
    });
    slot.addEventListener('drop', e => {
      e.preventDefault(); slot.classList.remove('s-over');
      if (dragId != null && dragFrom === 'roster')
        place(parseInt(row.dataset.ti), parseInt(slot.dataset.si), dragId);
      dragId = null; dragFrom = null;
    });
  });
  container.querySelectorAll('.slot-clear').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      clearSlot(parseInt(btn.dataset.ti), parseInt(btn.dataset.si));
    });
  });
  container.querySelectorAll('.team-note').forEach(ta => {
    ta.addEventListener('input', () => { state.notes[parseInt(ta.dataset.ti)] = ta.value; save(); });
  });
  container.querySelectorAll('.team-del').forEach(btn => {
    btn.addEventListener('click', () => {
      const ti = parseInt(btn.dataset.ti);
      state.teams.splice(ti, 1); state.notes.splice(ti, 1);
      save(); renderAll();
    });
  });
  container.querySelectorAll('.drag-handle').forEach(handle => {
    handle.addEventListener('dragstart', e => {
      dragTeam = parseInt(handle.dataset.ti);
      e.dataTransfer.effectAllowed = 'move';
      try { e.dataTransfer.setData('text/plain', 'team-' + dragTeam); } catch(_) {}
    });
    handle.addEventListener('dragend', () => {
      dragTeam = null;
      container.querySelectorAll('.team-row').forEach(r => r.classList.remove('tr-over'));
    });
  });
  container.querySelectorAll('.team-row').forEach(row => {
    row.addEventListener('dragover', e => {
      if (dragTeam != null) {
        e.preventDefault(); e.dataTransfer.dropEffect = 'move';
        container.querySelectorAll('.team-row').forEach(r => r.classList.remove('tr-over'));
        row.classList.add('tr-over');
      }
    });
    row.addEventListener('dragleave', e => {
      if (!row.contains(e.relatedTarget)) row.classList.remove('tr-over');
    });
    row.addEventListener('drop', e => {
      e.preventDefault(); row.classList.remove('tr-over');
      if (dragTeam != null) { moveTeam(dragTeam, parseInt(row.dataset.ti)); dragTeam = null; }
    });
  });
  if (selId != null)
    container.querySelectorAll('.slot:not(.s-filled)').forEach(s => s.classList.add('s-place'));
  addBtn.disabled = state.teams.length >= 20;
  addBtn.style.opacity = state.teams.length >= 20 ? '0.4' : '1';
}
function renderAll() {
  renderHeader(); renderElemChips(); renderRoster();
  renderUnavail(); renderSelBanner(); renderTeams();
}
function isMobile() { return window.matchMedia('(max-width:780px)').matches; }
function setTab(tab) {
  activeTab = tab;
  const sidebar = document.getElementById('sidebar');
  const main    = document.getElementById('main');
  if (isMobile()) {
    sidebar.classList.toggle('m-hide', tab !== 'roster');
    main.classList.toggle('m-hide', tab !== 'teams');
  } else {
    sidebar.classList.remove('m-hide');
    main.classList.remove('m-hide');
  }
  document.getElementById('tab-roster').classList.toggle('active', tab === 'roster');
  document.getElementById('tab-teams').classList.toggle('active', tab === 'teams');
}
window.matchMedia('(max-width:780px)').addEventListener('change', () => setTab(activeTab));
const rosterGrid  = document.getElementById('roster');
const unavailZone = document.getElementById('unavail-zone');
rosterGrid.addEventListener('dragover', e => {
  if (dragId != null && dragFrom === 'unavail') {
    e.preventDefault(); e.dataTransfer.dropEffect = 'move';
    rosterGrid.classList.add('rz-over');
  }
});
rosterGrid.addEventListener('dragleave', e => {
  if (!rosterGrid.contains(e.relatedTarget)) rosterGrid.classList.remove('rz-over');
});
rosterGrid.addEventListener('drop', e => {
  e.preventDefault(); rosterGrid.classList.remove('rz-over');
  if (dragId != null && dragFrom === 'unavail') restore(dragId);
  dragId = null; dragFrom = null;
});
unavailZone.addEventListener('dragover', e => {
  if (dragId != null && dragFrom === 'roster') {
    e.preventDefault(); e.dataTransfer.dropEffect = 'move';
    unavailZone.classList.add('uz-over');
  }
});
unavailZone.addEventListener('dragleave', e => {
  if (!unavailZone.contains(e.relatedTarget)) unavailZone.classList.remove('uz-over');
});
unavailZone.addEventListener('drop', e => {
  e.preventDefault(); unavailZone.classList.remove('uz-over');
  if (dragId != null && dragFrom === 'roster') markUnavailable(dragId);
  dragId = null; dragFrom = null;
});
document.getElementById('sel-cancel').addEventListener('click', () => {
  selId = null; renderRoster(); renderTeams(); renderSelBanner();
});
document.getElementById('sel-mark').addEventListener('click', () => {
  if (selId != null) markUnavailable(selId);
});
document.getElementById('search').addEventListener('input', e => {
  searchQ = e.target.value.trim(); renderRoster();
});
document.getElementById('add-btn').addEventListener('click', () => {
  if (state.teams.length >= 20) return;
  state.teams.push([null,null,null]); state.notes.push('');
  save(); renderAll();
  setTimeout(() => { const t = document.getElementById('teams'); t.scrollTop = t.scrollHeight; }, 0);
});
document.addEventListener('dragover', e => e.preventDefault());
document.addEventListener('drop',     e => e.preventDefault());
load();
unavailSet = new Set(state.unavailableIds);
setTab('teams');
renderAll();
</script>
</body>
</html>"""

JS = HTML.replace('<<<CHARS>>>', chars_json).replace('<<<ICONS>>>', icons_json)

with open(HTML_OUT, 'w', encoding='utf-8') as f:
    f.write(JS)

size = os.path.getsize(HTML_OUT)
print(f'Written: {HTML_OUT}')
print(f'File size: {size/1024:.1f} KB')
