## Context

wuwa-deck is a static, framework-free page (`index.html` + `js/app.js` + `css/style.css`). All state lives in one object, `state = { teams, notes, unavailableIds, doubleId }`, which is saved to localStorage under `wuwa-deck-state`. `state.notes` is a parallel array indexed by team, and every team mutation (add, delete, reorder in `moveTeam`) keeps it in sync by hand. Team rows are re-rendered wholesale through `innerHTML` in `renderTeams()`. The notes textarea avoids that path: its `input` handler writes to state and calls `save()` without re-rendering, so focus is kept.

The header holds a single `.stat-pill` showing "已获得 N / M", which `renderHeader()` fills in.

## Goals / Non-Goals

**Goals:**
- A per-team score input that is prominent, persisted, and stays attached to its team on add, delete and reorder.
- A live "总分 Total" header pill that replaces the 已获得 pill.
- Old saves load without errors.

**Non-Goals:**
- Sorting or ranking teams by score, score history, or importing and exporting scores.
- Hard validation of the 0–999999 "typical" range (see the decisions below).

## Decisions

**1. Store scores in a parallel `state.scores` array (numbers), mirroring `state.notes`.**
This matches the existing pattern, so add, delete and `moveTeam` each get one extra line. The alternative was restructuring teams into objects (`{slots, note, score}`), which would be cleaner long-term but would touch every reader of `state.teams` and need a bigger migration. That is not worth it for this change.

**2. Migration in `load()`: pad `scores` with 0 to `teams.length` and coerce entries to non-negative integers.**
This is the same pattern `load()` already uses for notes. Saves that have no `scores` key get all zeros.

**3. Input is `<input type="text" inputmode="numeric">` with digits-only sanitising, not `type="number"`.**
`type="number"` shows spinner arrows, accepts `e`, `-` and `.`, and is awkward to style at large sizes. On `input`, the handler strips non-digits, caps the length at 9 digits (a generous ceiling above the typical 999999, so ordinary scores are never rejected), stores `parseInt || 0`, and saves. An empty field counts as 0 and is shown as `0` again on `blur`.

**4. Score input updates the total without re-rendering the team list.**
Like notes, the `input` handler calls `save()` and then `renderHeader()` only, so the caret and focus stay put. Structural changes (add or delete team) already call `renderAll()`, which includes `renderHeader()`, so the total stays correct there too.

**5. Header: replace the 已获得 pill's markup with `<div class="stat-pill"><span>总分 Total</span><b id="h-score">0</b></div>`.**
The existing `.stat-pill` styling is reused. `renderHeader()` loses the owned and total lookups and sets `h-score` to the sum formatted with `toLocaleString('en-US')` (for example `1,234,567`), because six or more six-digit scores are hard to read without separators. The per-team input shows raw digits so editing stays simple.

**6. Layout: the score box sits between the slots and the notes, at a fixed width of 120px and the slot height (112px, or 110×96px at ≥1900px).**
A small "得分 SCORE" label sits on top and the number below it in Rajdhani 700 at 30px (26px at ≥1900px) in the accent cyan `#3fd6e4`, matching `.team-num-val`. "Smaller notes" means the score box takes width from the notes' flexible share. The notes textarea and the delete ✕ are wrapped in a `.team-tail` flex group (`flex: 1; min-width: 142px`) so they always wrap together. Without the group, there was a band of viewport widths (about 1366–1440px) where the notes stayed on the first line but the ✕ dropped onto a line of its own.

## Risks / Trade-offs

- [The row overflows on narrow desktop widths] → `.team-row` already has `flex-wrap: wrap`. On a single-column layout below about a 1420px viewport (before this change it was about 1150px), the notes and ✕ move to a full-width second line. Below about 800px the score box wraps too. This is accepted, because the slots and score box have fixed widths.
- [Sum precision] → With a 9-digit cap and a few dozen teams the sum stays far below `Number.MAX_SAFE_INTEGER`.
- [Losing the 已获得 count] → The same number is still shown in the roster count label ("M 已获得"), so no information is lost.
