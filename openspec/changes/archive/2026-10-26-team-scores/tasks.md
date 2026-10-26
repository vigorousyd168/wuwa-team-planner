## 1. State & persistence

- [x] 1.1 Add `scores: []` to `state` in `js/app.js`. In `load()`, read `p.scores`, coerce entries to non-negative integers, and pad with 0 to `teams.length`. The default state is 6 zeros.
- [x] 1.2 Keep `state.scores` in sync with teams: push 0 in the add-team handler, splice in the team-delete handler, and splice-move in `moveTeam()`.

## 2. Header total pill

- [x] 2.1 In `index.html`, replace the 已获得 stat pill with `<div class="stat-pill"><span>总分 Total</span><b id="h-score">0</b></div>`.
- [x] 2.2 Rewrite `renderHeader()` to set `#h-score` to the sum of `state.scores`, formatted with `toLocaleString('en-US')`. Remove the `h-owned` and `h-total` lookups.

## 3. Score input per team

- [x] 3.1 In `renderTeams()`, render a score box between `.slots` and `.team-note`: a "得分 SCORE" label plus `<input class="team-score" type="text" inputmode="numeric" maxlength="9" data-ti>` with the team's score as its value.
- [x] 3.2 Bind `input`: strip non-digits, update `state.scores[ti]` (empty counts as 0), `save()`, then `renderHeader()` only, with no team re-render. Bind `blur`: if the field is empty, show `0`.

## 4. Styling

- [x] 4.1 In `css/style.css`, style the score box: fixed width of 120px, height matching the slots (112px), the same border and background as `.team-note`, a small muted label, and the number in Rajdhani 700 at about 30px, `#3fd6e4`, with a cyan focus border.
- [x] 4.2 Shrink the notes box: wrap the notes and ✕ in a `.team-tail` flex group (min-width 142px) so the score box fits and the ✕ never wraps alone. In the `@media (min-width: 1900px)` block, set the score box to about 110px wide, 96px high, with a slightly smaller number font.

## 5. Verification

- [x] 5.1 In the browser: new and old saves load with 0 scores, typing updates the total live without losing focus, non-digits are rejected, and clearing the field then blurring shows 0.
- [x] 5.2 Reorder two scored teams and confirm the scores follow them. Delete a team and confirm the total drops. Refresh and confirm the scores persist.
- [x] 5.3 Check the layout at a normal desktop width, at ≥1900px (two columns) and on mobile: rows fit or wrap cleanly, and the 已获得 pill is gone.
