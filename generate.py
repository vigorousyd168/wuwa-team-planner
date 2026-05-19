import json, sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

IMG_DIR  = 'C:/MyWorkspace/wuwa-deck/wuwa-wiki/images'
HTML_OUT = 'C:/MyWorkspace/wuwa-deck/index.html'
IMG_REL  = './wuwa-wiki/images'  # relative path from index.html

# ── Character data ────────────────────────────────────────────────────────────
with open('C:/MyWorkspace/wuwa-deck/wuwa-wiki/characters.json', encoding='utf-8') as f:
    chars = json.load(f)

SUSTAIN_NAMES = {'守岸人', '莫宁', '维里奈', '卜灵', '白芷'}

# Strip imageBase64 if present; keep only lightweight fields + relative path
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

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = """
:root {
  --bg: #0b0f1a; --bg2: #131928; --bg3: #1a2235;
  --border: #2a3550; --accent: #00c8d4; --accent2: #0099a8;
  --text: #e0e8f8; --text2: #8a9bc0; --danger: #ff4d6d; --slot-empty: #111827;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg); color: var(--text);
  font-family: "Microsoft YaHei","PingFang SC",sans-serif;
  font-size: 13px; height: 100vh; overflow: hidden;
  display: flex; flex-direction: column;
}
header {
  background: var(--bg2); border-bottom: 1px solid var(--border);
  padding: 10px 16px; display: flex; align-items: center; gap: 12px; flex-shrink: 0;
}
header h1 { font-size: 16px; color: var(--accent); letter-spacing: 1px; font-weight: 600; }
header .subtitle { color: var(--text2); font-size: 12px; }
.layout { display: flex; flex: 1; overflow: hidden; }
.sidebar {
  flex: 1; min-width: 300px; background: var(--bg2);
  border-right: 1px solid var(--border); display: flex; flex-direction: column; overflow: hidden;
}
.sidebar-header {
  padding: 10px 12px; border-bottom: 1px solid var(--border);
  display: flex; flex-direction: column; gap: 8px;
}
.sidebar-header .row { display: flex; align-items: center; gap: 8px; }
.sidebar-title { font-size: 13px; color: var(--text2); font-weight: 600; }
#search {
  flex: 1; background: var(--bg3); border: 1px solid var(--border);
  color: var(--text); padding: 5px 10px; border-radius: 4px; font-size: 12px; outline: none;
}
#search:focus { border-color: var(--accent); }
#search::placeholder { color: var(--text2); }
.roster-grid {
  flex: 1; overflow-y: auto; padding: 10px;
  display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  gap: 8px; align-content: start;
}
.roster-grid::-webkit-scrollbar { width: 4px; }
.roster-grid::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
.char-card {
  position: relative; cursor: grab; border-radius: 6px; overflow: hidden;
  border: 1px solid var(--border); background: var(--bg3);
  transition: border-color .15s, transform .1s; user-select: none;
}
.char-card:hover { border-color: var(--accent); transform: translateY(-2px); }
.char-card:active { cursor: grabbing; }
.char-card img.char-portrait { width: 100%; height: auto; display: block; }
.char-card .char-initial {
  display: none; width: 100%; aspect-ratio: 3/4; background: var(--bg3);
  align-items: center; justify-content: center; font-size: 24px; font-weight: bold; color: var(--accent);
}
.char-card .char-footer {
  padding: 3px 4px; display: flex; align-items: center; justify-content: space-between; gap: 2px;
}
.char-card .char-name {
  font-size: 11px; color: var(--text); white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis; flex: 1;
}
.char-card .elem-icon { width: 14px; height: 14px; flex-shrink: 0; }
.char-card .star-badge {
  position: absolute; top: 3px; right: 3px; font-size: 9px;
  padding: 1px 3px; border-radius: 2px; font-weight: bold;
}
.char-card.star-5 .star-badge { background: rgba(255,215,0,.85); color: #000; }
.char-card.star-4 .star-badge { background: rgba(192,144,255,.85); color: #000; }
.char-card.star-1 .star-badge { background: rgba(180,200,255,.7); color: #000; }
.char-card.used { opacity: 0.4; filter: grayscale(50%); }
.char-card.unavailable { opacity: 0.5; filter: grayscale(100%) brightness(0.7); }
.elem-filters { display: flex; gap: 4px; flex-wrap: wrap; }
.elem-chip {
  display: flex; align-items: center; gap: 3px; padding: 2px 7px; border-radius: 10px;
  border: 1px solid var(--border); background: var(--bg3); cursor: pointer;
  font-size: 11px; color: var(--text2); transition: all .15s;
}
.elem-chip.active,.elem-chip:hover { border-color: var(--accent); color: var(--text); }
.elem-chip img { width: 12px; height: 12px; }
.unavailable-section {
  flex: 0 0 auto; border-top: 1px solid var(--border);
  padding: 8px 12px; display: flex; flex-direction: column; gap: 6px;
}
.unavailable-header {
  display: flex; align-items: center; gap: 8px;
  font-size: 12px; color: var(--text2); font-weight: 600;
}
.unavailable-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  gap: 8px; max-height: 140px; overflow-y: auto;
}
.unavailable-grid::-webkit-scrollbar { width: 4px; }
.unavailable-grid::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
.char-card.unavailable { opacity: 0.6; filter: grayscale(40%); }
.main { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.teams-header {
  padding: 10px 16px; border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 10px; background: var(--bg2); flex-shrink: 0;
}
.teams-header .title { font-size: 13px; color: var(--text2); font-weight: 600; flex: 1; }
.teams-header .count { font-size: 12px; color: var(--text2); }
.btn {
  padding: 5px 12px; border-radius: 4px; border: 1px solid var(--border);
  background: var(--bg3); color: var(--text); cursor: pointer; font-size: 12px;
  transition: background .15s, border-color .15s;
}
.btn:hover { background: var(--accent2); border-color: var(--accent); color: #fff; }
.btn:disabled { opacity: .4; cursor: not-allowed; }
.btn.primary { background: var(--accent2); border-color: var(--accent); color: #fff; }
.btn.primary:hover { background: var(--accent); }
#teams {
  flex: 1; overflow-y: auto; padding: 10px 16px;
  display: flex; flex-direction: column; gap: 8px;
}
#teams::-webkit-scrollbar { width: 4px; }
#teams::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
.team-row {
  background: var(--bg2); border: 1px solid var(--border); border-radius: 8px;
  padding: 10px 12px; display: flex; align-items: center; gap: 10px; min-height: 88px;
}
.team-row:hover { border-color: #3a4a6a; }
.team-label {
  font-size: 12px; color: var(--text2); width: 46px;
  flex-shrink: 0; text-align: center; line-height: 1.4;
}
.slot-group { display: flex; gap: 6px; flex-shrink: 0; }
.slot {
  width: 66px; height: 66px; border-radius: 6px; border: 1px dashed var(--border);
  background: var(--slot-empty); position: relative; overflow: hidden;
  transition: border-color .15s, background .15s;
}
.slot.drag-over { border-color: var(--accent); background: rgba(0,200,212,.08); border-style: solid; }
.slot.empty { display: flex; align-items: center; justify-content: center; cursor: default; }
.slot.empty .slot-plus { font-size: 22px; color: var(--border); line-height: 1; }
.slot.empty.drag-over .slot-plus { color: var(--accent); }
.slot.filled { border-style: solid; border-color: var(--border); }
.slot.filled img { width: 100%; height: 100%; object-fit: cover; display: block; }
.slot .slot-name {
  position: absolute; bottom: 0; left: 0; right: 0;
  background: rgba(0,0,0,.75); font-size: 10px; text-align: center;
  padding: 2px; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.slot-clear {
  position: absolute; top: 2px; right: 2px; width: 16px; height: 16px;
  background: rgba(0,0,0,.7); border: none; color: #fff; font-size: 10px;
  border-radius: 50%; cursor: pointer; display: none;
  align-items: center; justify-content: center; padding: 0; line-height: 1;
}
.slot.filled:hover .slot-clear { display: flex; }
.slot-clear:hover { background: #ff4d6d; }
.team-note {
  width: 160px; flex-shrink: 0; background: var(--bg3); border: 1px solid var(--border); color: var(--text);
  border-radius: 4px; padding: 6px 8px; font-size: 12px; resize: none; height: 66px;
  outline: none; font-family: inherit; line-height: 1.5;
}
.team-note:focus { border-color: var(--accent); }
.team-note::placeholder { color: var(--text2); }
.team-delete {
  flex-shrink: 0; width: 28px; height: 28px; background: transparent;
  border: 1px solid transparent; color: var(--text2); font-size: 14px;
  cursor: pointer; border-radius: 4px; display: flex; align-items: center; justify-content: center;
  transition: color .15s, border-color .15s;
}
.team-delete:hover { color: #ff4d6d; border-color: #ff4d6d; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
"""

# ── JS ────────────────────────────────────────────────────────────────────────
JS_TEMPLATE = """
const CHARACTERS = <<<CHARS>>>;
const ELEM_ICONS = <<<ICONS>>>;

const ELEM_KEY = {
  '冰凝':'bingning','气动':'qidong','导电':'daodian',
  '热熔':'rerong','湮灭':'jielin','衍射':'yanshe'
};
const ELEM_LIST = ['冰凝','气动','导电','热熔','湮灭','衍射'];

const PRESET_UNAVAILABLE_IDS = [4, 5, 6, 9, 10, 11, 13, 16, 17, 18, 19, 21, 22, 25, 29];

let state = { teams: [], notes: [], unavailableIds: [] };
let draggingId = null;
let searchQ = '';
let elemF = null;

function saveState() {
  localStorage.setItem('wuwa-deck-state', JSON.stringify(state));
}

function loadState() {
  try {
    const raw = localStorage.getItem('wuwa-deck-state');
    if (raw) {
      const p = JSON.parse(raw);
      if (Array.isArray(p.teams) && p.teams.length) {
        state.teams = p.teams;
        state.notes = Array.isArray(p.notes) ? p.notes : Array(p.teams.length).fill('');
        while (state.notes.length < state.teams.length) state.notes.push('');
        state.unavailableIds = Array.isArray(p.unavailableIds) ? p.unavailableIds : PRESET_UNAVAILABLE_IDS.slice();
        return;
      }
    }
  } catch(e) {}
  state.teams = Array.from({length: 6}, () => [null, null, null]);
  state.notes = Array(6).fill('');
  state.unavailableIds = PRESET_UNAVAILABLE_IDS.slice();
}

function getChar(id) { return CHARACTERS.find(c => c.id === id); }

function isUnavailable(characterId) { return state.unavailableIds.includes(characterId); }

function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function renderElemFilters() {
  const el = document.getElementById('elemFilters');
  el.innerHTML = ELEM_LIST.map(e => {
    const ek = ELEM_KEY[e] || '';
    const ic = ELEM_ICONS[ek] || '';
    return `<div class="elem-chip${elemF===e?' active':''}" data-elem="${e}">`+
      (ic ? `<img src="${ic}" alt="${e}">` : '') + e + '</div>';
  }).join('');
  el.querySelectorAll('.elem-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      elemF = elemF === chip.dataset.elem ? null : chip.dataset.elem;
      renderElemFilters(); renderRoster();
    });
  });
}

function renderRoster() {
  const SUSTAIN_IDS = new Set(CHARACTERS.filter(c => c.sustain).map(c => c.id));
  const useCount = {};
  state.teams.flat().filter(Boolean).forEach(id => { useCount[id] = (useCount[id] || 0) + 1; });

  const obtainedCount = CHARACTERS.filter(c => !isUnavailable(c.id)).length;
  const list = CHARACTERS.filter(c =>
    !isUnavailable(c.id) && (!searchQ || c.name.includes(searchQ)) && (!elemF || c.element === elemF)
  );
  const grid = document.getElementById('roster');
  const availCount = list.filter(c => (useCount[c.id] || 0) < (SUSTAIN_IDS.has(c.id) ? 2 : 1)).length;
  document.getElementById('rosterCount').textContent = availCount + ' 名可用 / ' + obtainedCount + ' 名已获得';
  grid.innerHTML = list.map(c => {
    const ek = ELEM_KEY[c.element] || '';
    const ic = ELEM_ICONS[ek] || '';
    const init = c.name[0] || '?';
    const threshold = SUSTAIN_IDS.has(c.id) ? 2 : 1;
    const usedClass = (useCount[c.id] || 0) >= threshold ? ' used' : '';
    return `<div class="char-card star-${c.star}${usedClass}" draggable="true" data-id="${c.id}" data-source="roster" title="${esc(c.name)}（${esc(c.element)}）">
      <span class="star-badge">${c.star}★</span>
      <img class="char-portrait" src="${c.img}" alt="${esc(c.name)}"
        onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
      <div class="char-initial">${init}</div>
      <div class="char-footer">
        <span class="char-name">${esc(c.name)}</span>
        ${ic ? `<img class="elem-icon" src="${ic}" alt="${esc(c.element)}">` : ''}
      </div>
    </div>`;
  }).join('');
  grid.querySelectorAll('.char-card').forEach(card => {
    card.addEventListener('dragstart', e => {
      draggingId = parseInt(card.dataset.id);
      e.dataTransfer.effectAllowed = 'all';
      card.style.opacity = '.5';
    });
    card.addEventListener('dragend', () => { card.style.opacity = ''; });
  });
}

function renderUnavailableRoster() {
  const unavailChars = CHARACTERS.filter(c => isUnavailable(c.id));
  const grid = document.getElementById('unavailable');
  document.getElementById('unavailableCount').textContent = unavailChars.length + ' / ' + CHARACTERS.length;
  grid.innerHTML = unavailChars.map(c => {
    const ek = ELEM_KEY[c.element] || '';
    const ic = ELEM_ICONS[ek] || '';
    const init = c.name[0] || '?';
    return `<div class="char-card star-${c.star} unavailable" draggable="true" data-id="${c.id}" data-source="unavailable" title="${esc(c.name)}（${esc(c.element)}）">
      <span class="star-badge">${c.star}★</span>
      <img class="char-portrait" src="${c.img}" alt="${esc(c.name)}"
        onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
      <div class="char-initial">${init}</div>
      <div class="char-footer">
        <span class="char-name">${esc(c.name)}</span>
        ${ic ? `<img class="elem-icon" src="${ic}" alt="${esc(c.element)}">` : ''}
      </div>
    </div>`;
  }).join('');
  grid.querySelectorAll('.char-card').forEach(card => {
    card.addEventListener('dragstart', e => {
      draggingId = parseInt(card.dataset.id);
      e.dataTransfer.effectAllowed = 'all';
      card.style.opacity = '.5';
    });
    card.addEventListener('dragend', () => { card.style.opacity = ''; });
  });
}

function renderSlot(ti, si, cid) {
  const char = cid ? getChar(cid) : null;
  if (!char) return `<div class="slot empty" data-slot="${si}"><span class="slot-plus">+</span></div>`;
  return `<div class="slot filled" data-slot="${si}">
    <img src="${char.img}" alt="${esc(char.name)}" onerror="this.style.display='none'">
    <span class="slot-name">${esc(char.name)}</span>
    <button class="slot-clear" data-team="${ti}" data-slot="${si}">×</button>
  </div>`;
}

function renderTeams() {
  const container = document.getElementById('teams');
  container.innerHTML = state.teams.map((slots, ti) =>
    `<div class="team-row" data-team="${ti}">
      <div class="team-label">队伍<br>${ti + 1}</div>
      <div class="slot-group">${slots.map((cid,si) => renderSlot(ti,si,cid)).join('')}</div>
      <textarea class="team-note" data-team="${ti}" placeholder="队伍备注…">${esc(state.notes[ti]||'')}</textarea>
      <button class="team-delete" data-team="${ti}" title="删除此队伍">✕</button>
    </div>`
  ).join('');

  container.querySelectorAll('.slot').forEach(slot => {
    slot.addEventListener('dragover', e => {
      if (draggingId !== null && !isUnavailable(draggingId)) {
        e.preventDefault();
        slot.classList.add('drag-over');
        e.dataTransfer.dropEffect = 'move';
      } else if (draggingId !== null) {
        e.dataTransfer.dropEffect = 'none';
      }
    });
    slot.addEventListener('dragleave', e => {
      if (!slot.contains(e.relatedTarget)) slot.classList.remove('drag-over');
    });
    slot.addEventListener('drop', e => {
      e.preventDefault();
      slot.classList.remove('drag-over');
      if (draggingId !== null && !isUnavailable(draggingId)) {
        const ti = parseInt(slot.closest('.team-row').dataset.team);
        const si = parseInt(slot.dataset.slot);
        state.teams[ti][si] = draggingId;
        draggingId = null;
        saveState(); renderTeams(); renderRoster();
      }
    });
  });

  container.querySelectorAll('.slot-clear').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      state.teams[+btn.dataset.team][+btn.dataset.slot] = null;
      saveState(); renderTeams(); renderRoster();
    });
  });

  container.querySelectorAll('.team-note').forEach(ta => {
    ta.addEventListener('input', () => {
      state.notes[+ta.dataset.team] = ta.value;
      saveState();
    });
  });

  container.querySelectorAll('.team-delete').forEach(btn => {
    btn.addEventListener('click', () => {
      const ti = +btn.dataset.team;
      state.teams.splice(ti, 1); state.notes.splice(ti, 1);
      saveState(); renderTeams(); renderRoster(); updateAddBtn();
    });
  });

  document.getElementById('teamCount').textContent = state.teams.length + ' / 20 队';
  updateAddBtn();
}

function updateAddBtn() {
  document.getElementById('addTeam').disabled = state.teams.length >= 20;
}

loadState();
renderElemFilters();
renderRoster();
renderUnavailableRoster();
renderTeams();

const rosterGrid = document.getElementById('roster');
const unavailGrid = document.getElementById('unavailable');

rosterGrid.addEventListener('dragover', e => { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; });
rosterGrid.addEventListener('drop', e => {
  e.preventDefault();
  if (draggingId !== null && isUnavailable(draggingId)) {
    const idx = state.unavailableIds.indexOf(draggingId);
    if (idx > -1) state.unavailableIds.splice(idx, 1);
    draggingId = null;
    saveState(); renderRoster(); renderUnavailableRoster();
  }
});

unavailGrid.addEventListener('dragover', e => { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; });
unavailGrid.addEventListener('drop', e => {
  e.preventDefault();
  if (draggingId !== null && !isUnavailable(draggingId)) {
    state.unavailableIds.push(draggingId);
    draggingId = null;
    saveState(); renderRoster(); renderUnavailableRoster();
  }
});

document.getElementById('search').addEventListener('input', e => {
  searchQ = e.target.value.trim(); renderRoster();
});

document.getElementById('addTeam').addEventListener('click', () => {
  if (state.teams.length >= 20) return;
  state.teams.push([null, null, null]); state.notes.push('');
  saveState(); renderTeams();
  const t = document.getElementById('teams');
  t.scrollTop = t.scrollHeight;
});

document.addEventListener('dragover', e => e.preventDefault());
document.addEventListener('drop', e => e.preventDefault());
"""

JS = JS_TEMPLATE.replace('<<<CHARS>>>', chars_json).replace('<<<ICONS>>>', icons_json)

# ── HTML ──────────────────────────────────────────────────────────────────────
HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>鸣潮编队小助手</title>
<style>""" + CSS + """</style>
</head>
<body>
<header>
  <h1>鸣潮编队小助手</h1>
  <span class="subtitle">Wuthering Waves Team Builder</span>
</header>
<div class="layout">
  <aside class="sidebar">
    <div class="sidebar-header">
      <div class="row">
        <span class="sidebar-title">角色库</span>
        <span id="rosterCount" style="font-size:11px;color:var(--text2);margin-left:auto"></span>
      </div>
      <div class="row">
        <input type="text" id="search" placeholder="搜索角色名称…">
      </div>
      <div class="elem-filters" id="elemFilters"></div>
    </div>
    <div id="roster" class="roster-grid"></div>
    <div class="unavailable-section">
      <div class="unavailable-header">
        未获得 <span id="unavailableCount" style="margin-left:auto"></span>
      </div>
      <div id="unavailable" class="unavailable-grid"></div>
    </div>
  </aside>
  <main class="main">
    <div class="teams-header">
      <span class="title">队伍配置</span>
      <span class="count" id="teamCount"></span>
      <button class="btn primary" id="addTeam">+ 添加队伍</button>
    </div>
    <div id="teams"></div>
  </main>
</div>
<script>""" + JS + """</script>
</body>
</html>"""

with open(HTML_OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)

size = os.path.getsize(HTML_OUT)
print(f'Written: {HTML_OUT}')
print(f'File size: {size/1024:.1f} KB')
