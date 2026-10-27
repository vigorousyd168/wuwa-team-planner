const ELEM_MAP = {
  '冷凝': { key: 'bingning', color: '#56b7ff' },
  '气动': { key: 'qidong',   color: '#3fdcab' },
  '导电': { key: 'daodian',  color: '#b88cff' },
  '热熔': { key: 'rerong',   color: '#ff8a4d' },
  '湮灭': { key: 'jielin',   color: '#ff6597' },
  '衍射': { key: 'yanshe',   color: '#ffd35e' }
};
const ELEM_ORDER = ['冷凝','气动','导电','热熔','湮灭','衍射'];
const BY_ID = new Map(CHARACTERS.map(c => [c.id, c]));
const BOSS_PERIOD = 5;
const TAIL_PX = 80;
const DEFAULT_ROUNDS = [
  [4680, 4680, 4680, 4680, 5668],
  [9160, 9160, 9160, 9160, 13458],
  [20223, 20223, 20223, 20223, 22239]
];

let state = { teams: [], notes: [], scores: [], unavailableIds: [], doubleId: null,
              bossDefs: [], rounds: [], viewMode: 'normal' };
let unavailSet = new Set();
let dragId = null, dragFrom = null, dragTeam = null;
let selId = null;
let searchQ = '', elemF = null;
let activeTab = 'teams';
let bossBarCollapsed = false;
let bossRO = null;

function defaultBossDefs() {
  return Array.from({length: BOSS_PERIOD}, (_, i) => ({ name: 'BOSS ' + (i + 1), resists: [] }));
}
function loadBosses(p) {
  const defs = Array.isArray(p.bossDefs) ? p.bossDefs : [];
  state.bossDefs = defaultBossDefs().map((d, i) => {
    const b = defs[i] && typeof defs[i] === 'object' ? defs[i] : {};
    const name = typeof b.name === 'string' ? b.name.trim().slice(0, 20) : '';
    const resists = Array.isArray(b.resists) ? ELEM_ORDER.filter(e => b.resists.includes(e)) : [];
    return { name: name || d.name, resists };
  });
  const rounds = (Array.isArray(p.rounds) ? p.rounds : []).filter(Array.isArray);
  state.rounds = rounds.length
    ? rounds.map(r => Array.from({length: BOSS_PERIOD}, (_, i) => Math.max(0, parseInt(r[i]) || 0)))
    : DEFAULT_ROUNDS.map(r => r.slice());
  state.viewMode = p.viewMode === 'compare' ? 'compare' : 'normal';
}

function save() {
  localStorage.setItem('wuwa-deck-state', JSON.stringify(state));
}
function load() {
  let p = {};
  try {
    const raw = localStorage.getItem('wuwa-deck-state');
    if (raw) {
      p = JSON.parse(raw) || {};
      loadBosses(p);
      if (Array.isArray(p.teams) && p.teams.length) {
        state.teams = p.teams.map(r => [r[0]??null, r[1]??null, r[2]??null]);
        state.notes = Array.isArray(p.notes) ? p.notes.slice() : [];
        while (state.notes.length < state.teams.length) state.notes.push('');
        state.scores = (Array.isArray(p.scores) ? p.scores : []).map(v => Math.max(0, parseInt(v) || 0));
        while (state.scores.length < state.teams.length) state.scores.push(0);
        state.unavailableIds = Array.isArray(p.unavailableIds) ? p.unavailableIds.slice() : [];
        state.doubleId = typeof p.doubleId === 'number' ? p.doubleId : null;
        return;
      }
    }
  } catch(e) { console.warn('wuwa-deck: load failed', e); p = {}; }
  loadBosses(p);
  state.teams = Array.from({length: 6}, () => [null,null,null]);
  state.notes = Array(6).fill('');
  state.scores = Array(6).fill(0);
  state.unavailableIds = [];
  state.doubleId = null;
}
function useCounts() {
  const m = {};
  state.teams.flat().forEach(id => { if (id != null) m[id] = (m[id]||0) + 1; });
  return m;
}
function threshold(c) { return (c.sustain || c.id === state.doubleId) ? 2 : 1; }
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
  if (state.doubleId === id) state.doubleId = null;
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
  const [s] = state.scores.splice(from, 1);
  state.teams.splice(to, 0, t);
  state.notes.splice(to, 0, n);
  state.scores.splice(to, 0, s);
  save(); renderAll();
}
function renderHeader() {
  const total = state.scores.reduce((a, b) => a + b, 0);
  document.getElementById('h-score').textContent = total.toLocaleString('en-US');
}
function fmt(n) { return n.toLocaleString('en-US'); }
function renderViewToggle() {
  const cmp = state.viewMode === 'compare';
  document.querySelectorAll('#view-toggle button').forEach(b =>
    b.classList.toggle('active', b.dataset.mode === state.viewMode));
  document.getElementById('teams').classList.toggle('compare', cmp);
  document.getElementById('boss-bar').style.display = cmp ? '' : 'none';
}
function resistChips(bi) {
  const rs = state.bossDefs[bi].resists;
  return ELEM_ORDER.map(name => {
    const e = ELEM_MAP[name];
    const on = rs.includes(name);
    const ic = ELEM_ICONS[e.key] || '';
    return `<span class="rz-chip${on ? ' on' : ''}" data-bi="${bi}" data-elem="${esc(name)}" title="${esc(name)}抗性"` +
      (on ? ` style="border-color:${e.color};background:${e.color}26"` : '') + '>' +
      (ic ? `<img src="${esc(ic)}" alt="">` : '') + `<span>${esc(name)}</span></span>`;
  }).join('');
}
function renderBossBar() {
  const bar = document.getElementById('boss-bar');
  if (state.viewMode !== 'compare') { bar.innerHTML = ''; return; }
  const n = state.rounds.length;
  const head = `<div class="bb-head">
    <span class="bb-title">BOSS 设置</span>
    <span class="bb-sub">${n} 轮 · 每轮 ${BOSS_PERIOD} 个</span>
    <button class="bb-btn" id="bb-collapse">${bossBarCollapsed ? '展开 ▾' : '收起 ▴'}</button>
    <button class="bb-btn add" id="bb-add-round">＋ 轮次</button>
  </div>`;
  if (bossBarCollapsed) { bar.innerHTML = head; return; }
  bar.innerHTML = head + `<div class="bb-scroll"><table class="bb-table">
    <thead><tr><th></th><th>名称</th><th>抗性</th>${state.rounds.map((_, ri) =>
      `<th class="bb-rh">R${ri + 1}${ri === n - 1 && n > 1 ? '<button class="bb-del-round" title="删除此轮">✕</button>' : ''}</th>`
    ).join('')}</tr></thead>
    <tbody>${state.bossDefs.map((d, bi) => `<tr>
      <td class="bb-idx">${bi + 1}</td>
      <td><input class="bb-name" data-bi="${bi}" maxlength="20" value="${esc(d.name)}"></td>
      <td class="bb-rz">${resistChips(bi)}</td>
      ${state.rounds.map((r, ri) =>
        `<td><input class="bb-score" data-ri="${ri}" data-bi="${bi}" type="text" inputmode="numeric" maxlength="9" value="${r[bi]}"></td>`
      ).join('')}
    </tr>`).join('')}</tbody>
  </table></div>`;
}
function renderBossCards() {
  const col = document.querySelector('#teams .boss-col');
  if (!col) return;
  const total = state.scores.reduce((a, b) => a + b, 0);
  const seq = [];
  state.rounds.forEach((r, ri) => r.forEach((score, bi) => { if (score > 0) seq.push({ri, bi, score}); }));
  let acc = 0, lastRi = -1;
  col.innerHTML = seq.length ? seq.map(b => {
    const start = acc, end = acc + b.score;
    acc = end;
    const st = end <= total ? 'cleared' : start < total ? 'partial' : 'unreached';
    const d = state.bossDefs[b.bi];
    const label = `R${b.ri + 1}-${b.bi + 1}`;
    const status = st === 'cleared' ? '✓' : st === 'partial' ? `${fmt(total - start)} / ${fmt(b.score)}` : '';
    const icons = d.resists.map(name => {
      const ic = ELEM_ICONS[ELEM_MAP[name].key] || '';
      return ic ? `<img src="${esc(ic)}" alt="${esc(name)}">` : '';
    }).join('');
    const title = `${label} ${d.name}\n所需 ${fmt(b.score)}` +
      (d.resists.length ? `\n抗性：${d.resists.join('、')}` : '') +
      (st === 'cleared' ? '\n已击破' : st === 'partial' ? `\n已打 ${status}` : '\n未到达');
    const rStart = b.ri !== lastRi;
    lastRi = b.ri;
    return `<div class="boss-card ${st}${rStart ? ' round-start' : ''}" data-start="${start}" data-end="${end}" title="${esc(title)}">
      ${st === 'partial' ? '<div class="bc-tail"></div>' : ''}
      <div class="bc-body">
        <div class="bc-top"><span class="bc-tag">${label}</span><span class="bc-rz">${icons}</span></div>
        <div class="bc-name">${esc(d.name)}</div>
        <div class="bc-score">${fmt(b.score)}</div>
        ${status ? `<div class="bc-status">${status}</div>` : ''}
      </div>
    </div>`;
  }).join('') : '<div class="boss-empty">设置 BOSS 分数以对照进度</div>';
  layoutBosses();
}
function layoutBosses() {
  const wrap = document.querySelector('#teams .cmp-wrap');
  if (!wrap) return;
  const col = wrap.querySelector('.boss-col');
  const rows = [...wrap.querySelectorAll('.team-row')].map((r, ti) =>
    ({ top: r.offsetTop, h: r.offsetHeight, s: state.scores[ti] || 0 }));
  const total = rows.reduce((a, r) => a + r.s, 0);
  const firstScored = rows.find(r => r.s > 0);
  // Cumulative score -> y: lands inside the team whose running total first reaches S.
  const y = S => {
    if (S <= 0) return firstScored ? firstScored.top : 0;
    let c = 0, last = 0;
    for (const r of rows) {
      if (r.s <= 0) continue;
      if (S <= c + r.s) return r.top + (S - c) / r.s * r.h;
      c += r.s; last = r.top + r.h;
    }
    return last;
  };
  let tailY = total > 0 ? y(total) : 0;
  col.querySelectorAll('.boss-card').forEach(card => {
    const start = +card.dataset.start, end = +card.dataset.end;
    let top, h;
    if (end <= total) {
      top = y(start); h = y(end) - top;
    } else if (start < total) {
      top = y(start);
      const cov = y(total) - top;
      h = cov + TAIL_PX;
      card.querySelector('.bc-tail').style.top = cov + 'px';
      tailY = top + h;
    } else {
      top = tailY; h = TAIL_PX; tailY += TAIL_PX;
    }
    card.style.top = (top + 1) + 'px';
    card.style.height = Math.max(2, h - 2) + 'px';
  });
  col.style.minHeight = tailY + 'px';
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
      ${c.id === state.doubleId ? '<span class="cc-sustain">体 ×2</span>' : ''}
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
function renderDoublePick() {
  const opts = CHARACTERS.filter(c => !c.sustain && !unavailSet.has(c.id));
  const sel = document.getElementById('double-pick');
  sel.innerHTML = '<option value="">无</option>' +
    opts.map(c => `<option value="${c.id}">${esc(c.name)}</option>`).join('');
  sel.value = opts.some(c => c.id === state.doubleId) ? String(state.doubleId) : '';
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
function renderSlot(ti, si, cid, counts) {
  const c = cid != null ? BY_ID.get(cid) : null;
  if (!c) return `<div class="slot" data-si="${si}"><div class="slot-plus">＋</div></div>`;
  const over = counts[c.id] > threshold(c);
  return `<div class="slot s-filled${over ? ' s-warn' : ''}" data-si="${si}"${over ? ' title="编入次数超出上限"' : ''}>
    <img src="${esc(c.img)}" alt="${esc(c.name)}">
    <div class="slot-name">${esc(c.name)}</div>
    <button class="slot-clear" data-ti="${ti}" data-si="${si}">✕</button>
  </div>`;
}
function renderTeams() {
  const container = document.getElementById('teams');
  if (bossRO) { bossRO.disconnect(); bossRO = null; }
  const cmp = state.viewMode === 'compare';
  if (state.teams.length === 0) {
    container.innerHTML = `<div class="no-teams">
      <div class="no-teams-t">还没有队伍</div>
      <div class="no-teams-s">点击右上角「添加队伍」开始编队</div>
    </div>`;
    return;
  }
  const counts = useCounts();
  const rowsHtml = state.teams.map((slots, ti) => {
    const num = ('0' + (ti + 1)).slice(-2);
    return `<div class="team-row" data-ti="${ti}">
      <div class="drag-handle" draggable="true" data-ti="${ti}" title="拖动排序">⠿</div>
      <div class="team-num">
        <span class="team-num-label">TEAM</span>
        <span class="team-num-val">${num}</span>
      </div>
      <div class="slots">${slots.map((cid, si) => renderSlot(ti, si, cid, counts)).join('')}</div>
      <label class="team-score-box">
        <span class="team-score-label">得分 SCORE</span>
        <input class="team-score" type="text" inputmode="numeric" maxlength="9" data-ti="${ti}" value="${state.scores[ti]||0}">
      </label>
      <div class="team-tail">
        <textarea class="team-note" data-ti="${ti}" placeholder="队伍备注 Notes…">${esc(state.notes[ti]||'')}</textarea>
        <button class="team-del" data-ti="${ti}" title="删除此队伍">✕</button>
      </div>
    </div>`;
  }).join('');
  container.innerHTML = cmp
    ? `<div class="cmp-wrap"><div class="boss-col"></div><div class="cmp-teams">${rowsHtml}</div></div>`
    : rowsHtml;
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
  container.querySelectorAll('.team-score').forEach(inp => {
    inp.addEventListener('input', () => {
      const digits = inp.value.replace(/\D/g, '').slice(0, 9);
      if (digits !== inp.value) inp.value = digits;
      state.scores[parseInt(inp.dataset.ti)] = parseInt(digits) || 0;
      save(); renderHeader();
      if (cmp) renderBossCards();
    });
    inp.addEventListener('blur', () => { if (inp.value === '') inp.value = '0'; });
  });
  container.querySelectorAll('.team-del').forEach(btn => {
    btn.addEventListener('click', () => {
      const ti = parseInt(btn.dataset.ti);
      state.teams.splice(ti, 1); state.notes.splice(ti, 1); state.scores.splice(ti, 1);
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
  if (cmp) {
    renderBossCards();
    bossRO = new ResizeObserver(() => layoutBosses());
    bossRO.observe(container.querySelector('.cmp-teams'));
  }
}
function renderAll() {
  renderHeader(); renderElemChips(); renderDoublePick(); renderRoster();
  renderUnavail(); renderSelBanner(); renderViewToggle(); renderBossBar(); renderTeams();
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
document.getElementById('double-pick').addEventListener('change', e => {
  state.doubleId = e.target.value ? parseInt(e.target.value) : null;
  save(); renderAll();
});
document.getElementById('view-toggle').addEventListener('click', e => {
  const btn = e.target.closest('button');
  if (!btn || btn.dataset.mode === state.viewMode) return;
  state.viewMode = btn.dataset.mode;
  save(); renderAll();
});
const bossBar = document.getElementById('boss-bar');
bossBar.addEventListener('input', e => {
  const t = e.target;
  if (t.classList.contains('bb-name')) {
    state.bossDefs[parseInt(t.dataset.bi)].name = t.value;
  } else if (t.classList.contains('bb-score')) {
    const digits = t.value.replace(/\D/g, '').slice(0, 9);
    if (digits !== t.value) t.value = digits;
    state.rounds[parseInt(t.dataset.ri)][parseInt(t.dataset.bi)] = parseInt(digits) || 0;
  } else return;
  save(); renderBossCards();
});
bossBar.addEventListener('focusout', e => {
  if (e.target.classList.contains('bb-score') && e.target.value === '') e.target.value = '0';
});
bossBar.addEventListener('click', e => {
  const chip = e.target.closest('.rz-chip');
  if (chip) {
    const bi = parseInt(chip.dataset.bi), el = chip.dataset.elem;
    const d = state.bossDefs[bi];
    const on = d.resists.includes(el);
    d.resists = ELEM_ORDER.filter(x => x === el ? !on : d.resists.includes(x));
    chip.parentElement.innerHTML = resistChips(bi);
    save(); renderBossCards();
  } else if (e.target.closest('#bb-add-round')) {
    state.rounds.push(Array(BOSS_PERIOD).fill(0));
    save(); renderAll();
  } else if (e.target.closest('.bb-del-round')) {
    if (state.rounds.length > 1) state.rounds.pop();
    save(); renderAll();
  } else if (e.target.closest('#bb-collapse')) {
    bossBarCollapsed = !bossBarCollapsed;
    renderBossBar();
  }
});
document.getElementById('search').addEventListener('input', e => {
  searchQ = e.target.value.trim(); renderRoster();
});
document.getElementById('add-btn').addEventListener('click', () => {
  state.teams.push([null,null,null]); state.notes.push(''); state.scores.push(0);
  save(); renderAll();
  setTimeout(() => { const t = document.getElementById('teams'); t.scrollTop = t.scrollHeight; }, 0);
});
document.addEventListener('dragover', e => e.preventDefault());
document.addEventListener('drop',     e => e.preventDefault());
load();
unavailSet = new Set(state.unavailableIds);
setTab('teams');
renderAll();
