## Context

The app is a static single page with three files: `index.html`, `js/app.js` and `css/style.css`. It has no framework or build step. All state lives in one `state` object saved to localStorage under `wuwa-deck-state`. `renderTeams()` rebuilds `#teams` with `innerHTML` and rebinds its events. Score inputs deliberately call only `save()` and `renderHeader()` so the input keeps focus. At ≥1900px, `#teams` becomes a two-column grid.

Team rows have a nominal fixed height (112px slots, or 96px at ≥1900px). At narrow widths the row wraps, though, so actual heights vary. Any score-to-pixel mapping therefore has to read the rendered layout instead of assuming a constant height.

## Goals / Non-Goals

**Goals:**
- Add a persisted 普通 / 对照 view toggle.
- In 对照模式, show teams in one column with a boss column on the left. Boss boundaries map onto team cards by cumulative score, so the bottom of Boss 1 (5000) sits at 50% of Team 2 when the teams have 4000 and 2000.
- Model bosses as a period of 5. Five shared definitions (name and resistance tags) apply to every round, and each round has its own 5 required scores. There are 3 preset rounds by default (see D5), and users can add a round or delete the last one. Everything is persisted.
- Keep the column aligned live while scores are typed, teams are reordered, added or deleted, bosses are edited, or the window is resized.

**Non-Goals:**
- Scaling team card heights to their scores. Team cards keep their normal size.
- Built-in boss presets or game data, a configurable period length (fixed at 5), reordering bosses, and deleting a round from the middle.
- Any gameplay logic from resistances, such as warning when a team's element matches a boss's resistance. The tags are informational only.
- Multiple boss sets or seasons, or a boss-clear summary in the header.

## Decisions

### D1. Piecewise mapping from cumulative score to y position
Let `c_k` be the cumulative score before team k, with `c_0 = 0`, and `T` the total. For a score point `S` with `0 < S ≤ T`, find the first team k with `score_k > 0` and `c_k < S ≤ c_k + score_k`. Then `y(S) = top_k + (S − c_k) / score_k × height_k`, where `top_k` and `height_k` are the team row's `offsetTop` and `offsetHeight` relative to the compare wrapper. `y(0)` is the top of the first team row.
- Teams with a score of 0 hold no score range, so a boundary never lands inside them. They still display normally.
- A boundary exactly at `c_k + score_k` sits at the bottom edge of team k, not in the gap after it. The 10px gaps between rows belong to no team, and a boss card that spans them is drawn continuously.
- *Alternative:* a global px-per-score scale with team heights proportional to score. The user rejected this because low-score teams would be unreadable.

### D2. Boss ranges and the uncovered tail
The column sequence is flattened round-major: `seq = rounds.flatMap((r, ri) => r.map((score, bi) => ({ri, bi, score})))`. So round 1 bosses 1–5 come first, then round 2 bosses 1–5, and so on. Each entry takes its name and resistances from `bossDefs[bi]`. Entry j covers the cumulative range `[B_{j-1}, B_j)`, where `B_j` is the sum of the scores of entries 1 through j. Entries with a score of 0 are skipped in the column.
- **Cleared** (`B_j ≤ T`): the card spans `y(B_{j-1})` to `y(B_j)`.
- **Partially cleared** (`B_{j-1} < T < B_j`): the covered part spans `y(B_{j-1})` to the bottom of the last scored team. It is followed by an uncovered tail of fixed height `TAIL_PX` (80px) below the team list.
- **Not reached** (`B_{j-1} ≥ T`): the card is stacked below the previous card's tail with height `TAIL_PX`.

A fixed tail height keeps the uncovered part readable, since scaling it to its true score could make it enormous or tiny. The visual is honest because only the covered segment is to scale. If `T = 0`, every boss is "not reached" and stacks from the top.

### D3. DOM structure and measurement
In 对照模式, `renderTeams()` outputs:
```
#teams.compare
  .cmp-wrap  (position:relative; display:grid; grid-template-columns: <boss-w> 1fr)
    .boss-col  (position:relative; absolutely positioned .boss-card children)
    .cmp-teams (flex column, gap 10px; the existing .team-row markup unchanged)
```
`#teams` stays the scroll container, so both columns scroll together. Existing event binding uses `container.querySelectorAll(...)`, so it keeps working on the nested rows unchanged.

A separate `layoutBosses()` reads row geometry and writes `top` and `height` on the boss cards. It also sets `.boss-col`'s `min-height` so tails extend the scroll area. It is called:
- at the end of `renderTeams()`, when in compare mode;
- from the score `input` handler, next to `renderHeader()`, so typing never re-renders the inputs;
- from the boss editor `input` handlers;
- from a `ResizeObserver` on `.cmp-teams`, which covers window resizes and row wrapping.

*Alternative:* compute positions from constants. This was rejected because rows wrap at narrow and mobile widths.

### D4. The boss editor is a table, and boss cards are display-only
The boss cards can be just a few pixels tall when a boss's required score is small compared with the teams' scores, so inputs inside the cards would break. In compare mode, the editor appears as a panel below `.teams-bar`, above `#teams` (`#boss-bar`). It is a table with one row per boss definition (always 5) and one score column per round:

```
         名称        抗性                  R1      R2   ✕   ＋ 轮次
  1  [ 鸣钟之龟 ]  [冷][气][导][热][湮][衍]  [5000]  [8000]
  2  [ ……      ]  …                     [2000]  [3500]
  …
```

- **Name input:** edits `bossDefs[bi].name`, which every round shares.
- **Resistance toggles:** six small element-icon chips that reuse `ELEM_MAP` colours and `ELEM_ICONS`. Clicking one toggles that element in `bossDefs[bi].resists`. There is no minimum or maximum, because a boss can have 0, 1 or several resistances (1 is most common). Toggling re-renders only that row's chips and the boss cards.
- **Score inputs:** one per round per boss, editing `rounds[ri][bi]`, digits only, with the same rules as team scores.
- **Rounds:** the "＋ 轮次" button appends `[0,0,0,0,0]`. A ✕ on the last round's column header removes that round, and is hidden when only 1 round remains.
- **Collapse:** a 收起 / 展开 toggle collapses the panel to a single summary line ("BOSS 设置 · N 轮"), so it doesn't take up the teams' vertical space. This is not persisted.

Text and score inputs call `save()` and then `renderBossCards()`, which re-labels the cards and runs `layoutBosses()`. The table is never rebuilt on input, so focus is kept. Adding or deleting a round rebuilds the table and the column.

Boss cards show `R{ri+1}-{bi+1}`, the name, resistance icons, the required score, and a status (✓ for cleared, or `X / Y` for partial). Text is clipped by `overflow:hidden`, and a `title` tooltip carries the full text, including resistance names. A thin, stronger divider marks the top of each round's first card, so the period boundary is visible.

*Alternative:* store a flat list of bosses, each with its own name. This was rejected because the user wants names and resistances synced across rounds, and editing them once removes duplicated data entry.

### D5. State and persistence
New state, saved with the rest:
- `state.bossDefs: [{name: string, resists: string[]}]`, always length 5 (the period, `BOSS_PERIOD = 5`).
- `state.rounds: number[][]`, where each inner array has length 5 and there is at least 1 round.
- `state.viewMode: 'normal' | 'compare'`.

`load()` coerces each field:
- `bossDefs` is padded or truncated to 5. Each `name` becomes a string trimmed to 20 characters, defaulting to `BOSS n`. `resists` keeps only valid element names in `ELEM_ORDER`, de-duplicated.
- Each round is padded or truncated to 5 integers of at least 0. If no rounds are present, the default is `DEFAULT_ROUNDS`: R1 `[4680, 4680, 4680, 4680, 5668]`, R2 `[9160, 9160, 9160, 9160, 13458]`, R3 `[20223, 20223, 20223, 20223, 22239]`.
- `viewMode` falls back to `'normal'`.

Old saves, and the no-save fallback branch, get the defaults. `load()` currently returns early only when teams exist, so the defaults must also be set in that fallback branch.

### D6. The view toggle
A two-button segmented control (`普通 | 对照`) sits in `.teams-bar`. Clicking a button sets `viewMode`, then calls `save()` and `renderAll()`. CSS keys off `#teams.compare` and `#boss-bar` visibility. The ≥1900px two-column grid rule is scoped to `#teams:not(.compare)`, so compare mode is always one column. In compare mode the rows use the normal (non-compact) size, because the compact sizing exists only for two-column mode.

### D7. Mobile
The boss column narrows to about 64px at ≤780px. Card text drops to the name and a short status. The layout is otherwise unchanged. Rows can wrap taller there, and the mapping handles that through measurement.

## Risks / Trade-offs

- [Layout thrash: reading `offsetTop` on every keystroke] → Only N rows are read, with N small (6–30), and in a single pass of reads before writes. This is negligible.
- [ResizeObserver feedback loop: setting the boss column height changes the wrapper size] → Observe `.cmp-teams`, not the wrapper. The boss column sits in a separate grid cell and does not affect `.cmp-teams`' size.
- [Tiny boss cards are unreadable] → Clip the text, add a tooltip, and keep a 2px minimum visual height so every boss still shows as a sliver. All editing happens in the strip.
- [Fixed-height tails could be misread as being to scale] → Give tails a distinct dashed or dimmed style and an explicit `X / Y` label.
- [The boss editor table takes vertical space above the teams, about 6 rows] → Make it collapsible. Wide round counts scroll horizontally inside the panel (`overflow-x:auto`).
- [Many rounds make the boss column long] → The column scrolls with the teams. Entries with a score of 0, such as unused future rounds, are skipped.
- [The `#teams` innerHTML structure differs between modes] → `#teams` stays the only container, and selectors are unchanged. Drag-reorder and slot drops are verified in both modes.
