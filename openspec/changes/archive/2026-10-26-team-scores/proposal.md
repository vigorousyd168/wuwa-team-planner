## Why

Users plan teams to clear content scored per team, and want to record each team's score next to its lineup and see the overall total at a glance. The header's "已获得" pill duplicates information already shown in the roster count ("N 可用 / M 已获得"), so it can give way to a more useful total-score pill.

## What Changes

- Add a "得分 Score" input to every team row. It holds a non-negative integer (typical range 0–999999), defaults to 0, and shows the number in a large, prominent font.
- Make the team notes textarea narrower so the score box fits on the row.
- Persist scores in localStorage with the rest of the team state. Scores move with their team on reorder and are removed when their team is deleted. Teams saved before this change load with a score of 0.
- **Remove** the "已获得 N / M" pill from the upper-right header.
- Add a "总分 Total" pill to the upper-right header that shows the sum of all team scores and updates live as scores change or teams are added or removed.

## Capabilities

### New Capabilities
- `team-scores`: per-team score input (default 0, persisted, follows reorder/delete) and the header total-score pill that sums all team scores.

### Modified Capabilities
<!-- None: the 已获得 header pill is not covered by any existing spec, and the notes box resize is a layout change only (the notes requirements are unchanged). -->

## Impact

- `index.html`: replace the 已获得 stat pill with a 总分 Total pill.
- `js/app.js`: add `state.scores` (load/save/migration, add/delete/reorder), render the score input per team, compute the total, and drop the owned-count header rendering.
- `css/style.css`: styles for the score box (large numeric font) and the narrower notes box, including the ≥1900px two-column layout.
- No new dependencies. The localStorage key `wuwa-deck-state` gains a `scores` array, and older saves stay compatible.
