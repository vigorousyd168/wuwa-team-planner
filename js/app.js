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
const PRESET_UNAVAIL = [5,6,9,10,11,13,16,17,18,19,21,22,25,29];

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
