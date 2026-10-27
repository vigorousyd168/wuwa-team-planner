## 1. State & persistence

- [x] 1.1 Add `BOSS_PERIOD = 5` to `js/app.js`. Add `bossDefs`, `rounds` and `viewMode: 'normal'` to `state`. Write `defaultBossDefs()`, which returns 5 entries of `{name: 'BOSS n', resists: []}`.
- [x] 1.2 In `load()`, coerce the boss fields as described in D5 of design.md:
  - `bossDefs`: pad or truncate to 5, trim names to 20 characters, and filter and de-duplicate `resists` against `ELEM_ORDER`.
  - `rounds`: pad or truncate each round to 5 integers of at least 0. Default to `DEFAULT_ROUNDS` (3 preset rounds) when missing or empty.
  - `viewMode`: accept only `'compare'`, otherwise use `'normal'`.
  - Set the same defaults in the fallback, no-save branch.

## 2. Markup & toggle

- [x] 2.1 In `index.html`, add a segmented toggle to `.teams-bar`: `<div id="view-toggle"><button data-mode="normal">普通</button><button data-mode="compare">对照</button></div>`. Add an empty `<div id="boss-bar"></div>` between `#sel-banner` and `#teams`.
- [x] 2.2 Bind the toggle buttons: set `state.viewMode`, then `save()` and `renderAll()`. Add `renderViewToggle()`, called from `renderAll()`, to set the `.active` class, toggle the `compare` class on `#teams`, and show or hide `#boss-bar`.

## 3. Boss editor panel

- [x] 3.1 Implement `renderBossBar()`, called from `renderAll()`. In normal mode it renders nothing. In compare mode it renders:
  - a header with "BOSS 设置 · N 轮", a 收起/展开 toggle (an in-memory flag, not persisted) and a "＋ 轮次" button;
  - a table with 5 rows, each holding: the index, a name `<input maxlength="20">`, 6 resistance chips (element icon plus name, coloured via `ELEM_MAP` when active), and one score `<input inputmode="numeric" maxlength="9">` per round;
  - round column headers R1…Rn, with ✕ only on the last header and only when n > 1.
  - When collapsed, only the header line shows.
- [x] 3.2 Bind the name and score inputs. Name `input`: update `bossDefs[bi].name`, `save()`, then `renderBossCards()`. Score `input`: strip non-digits, set `rounds[ri][bi]`, `save()`, then `renderBossCards()`. Score `blur`: if empty, show `0`. None of these handlers rebuild the panel, so focus is kept.
- [x] 3.3 Bind the resistance chips. Clicking one toggles the element in `bossDefs[bi].resists`, then calls `save()`, re-renders only that row's chips, and calls `renderBossCards()`.
- [x] 3.4 Bind "＋ 轮次" to push `Array(5).fill(0)`, and the last-round ✕ to pop that round. Each then calls `save()` and `renderAll()`. Bind 收起/展开 to flip the flag and call `renderBossBar()`.

## 4. Compare layout & boss column

- [x] 4.1 In `renderTeams()`, when `viewMode === 'compare'` and teams exist, wrap the row markup as `.cmp-wrap > .boss-col + .cmp-teams > .team-row…`. Leave all existing `container.querySelectorAll` bindings unchanged, and confirm they still bind.
- [x] 4.2 Implement `layoutBosses()`, following D1 and D2 in design.md:
  - Read each `.team-row`'s `offsetTop` and `offsetHeight` relative to `.cmp-wrap`.
  - Build `y(S)` by piecewise mapping that skips 0-score teams.
  - Compute each boss's state (cleared, partial or unreached) and its segment positions, using `TAIL_PX = 80` for uncovered parts.
  - Write `top` and `height` on the `.boss-card` elements, with a 2px minimum.
  - Set `.boss-col` `min-height` so the tails extend the scroll area.
  - Show an empty hint ("设置 BOSS 分数以对照进度") when no entry has a score above 0.
- [x] 4.3 Implement `renderBossCards()`:
  - Flatten the bosses round-major into `seq` (D2), skipping entries with a score of 0.
  - Build a `.boss-card` for each entry: the `R{ri+1}-{bi+1}` label, the name from `bossDefs[bi]`, resistance icons, the required score, a ✓ or `X / Y` status, a `title` tooltip that includes the resistance names, and a state class. Add a `.round-start` class on each round's first visible card.
  - Then call `layoutBosses()`.
  - Call `renderBossCards()` at the end of `renderTeams()` when in compare mode.
- [x] 4.4 Re-layout on score typing: in the `.team-score` input handler, call `renderBossCards()` after `renderHeader()` when in compare mode, without re-rendering the teams.
- [x] 4.5 Attach a `ResizeObserver` to `.cmp-teams`, disconnecting any previous one on each render, so resizes and row wrapping trigger `layoutBosses()`.

## 5. Styling

- [x] 5.1 Style the `#view-toggle` segmented control in the `.teams-bar` look, with the active button in cyan. Style `#boss-bar` as a compact panel. Its table matches the existing input styles and uses `overflow-x:auto` for many rounds. Resistance chips are small and muted when off, and tinted with their element colour when on. The collapsed state is a single line.
- [x] 5.2 Add the compare layout: `.cmp-wrap` as a grid with `140px 1fr` columns and a 12px gap, `.boss-col` as `position:relative`, and `.cmp-teams` as a flex column with a 10px gap.
- [x] 5.3 Scope the `@media (min-width: 1900px)` two-column and compact rules to `#teams:not(.compare)` so compare mode stays one column at normal size.
- [x] 5.4 Style the boss cards as absolutely positioned, with `overflow:hidden` and a 1px inset gap between cards. Cleared cards get a cyan tint and ✓. Partial cards get a solid covered part plus a dashed or dimmed tail (for example a gradient stop at the covered height). Unreached cards get a dashed muted style. `.round-start` cards get a stronger top divider. Resistance icons are about 12px, in a row on the card. At ≤780px, narrow `.boss-col` to about 64px and shrink the card text.

## 6. Verification

- [x] 6.1 Run the example scenario: bosses of 5000 and 2000, teams of 4000 and 2000. Confirm that Boss 1's bottom sits at 50% of Team 2's card by measuring in DevTools. Also check an exact boundary (Boss 1 at 4000) and a 0-score team being skipped.
- [x] 6.2 Check the boss states: cleared, partial (tail and `1000 / 2000` label), unreached, and a total of 0. Check that the boss column scrolls together with the teams.
- [x] 6.3 Check live behaviour: typing team or boss scores re-aligns the column without losing focus. Adding, deleting and reordering teams re-aligns it. Resizing the window keeps it aligned.
- [x] 6.4 Check the period behaviour:
  - A fresh load shows 5 bosses and the 3 preset rounds.
  - Renaming boss 1 updates both R1-1 and R2-1.
  - R1 and R2 scores are independent.
  - "＋ 轮次" adds R3 with zeros, and ✕ removes the last round but never the only one.
  - R2-1 continues directly after R1-5 in the column.
  - Resistance chips toggle on and off, including two on one boss, and the icons appear on every round's card.
  - The panel collapses and expands.
- [x] 6.5 Check that the mode and boss data persist across a refresh, an old save without these fields loads in normal mode with the 5 default bosses and the 3 preset rounds, and normal mode looks unchanged (including two columns at ≥1900px). Check that compare mode stays one column at ≥1900px and works on mobile.
