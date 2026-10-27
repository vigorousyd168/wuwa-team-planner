## Why

Teams now record scores. Users clear a sequence of bosses, each needing a set score, and want to see at a glance which bosses their teams' scores clear and where each boss falls in the team lineup. The current list shows only a total, so users have to add up cumulative scores by hand to work out which team finishes which boss.

## What Changes

- Add a view toggle to the teams bar that switches between the normal view and a new **对照模式 (Compare)** view. The chosen mode is persisted.
- In 对照模式, teams are always listed in a **single column**, even at widths ≥1900px where the normal view uses two columns.
- In 对照模式, a **boss column** appears to the left of the team column. Each boss card's vertical extent matches the cumulative score range it needs. Boss boundaries are placed using the cumulative team scores: the point at cumulative score S falls inside the team card where the running total reaches S, at a proportional height within that card. Example: Boss 1 needs 5000 and Boss 2 needs 2000, Team 1 has 4000 and Team 2 has 2000. Boss 1 spans from the top of Team 1 down to 50% of Team 2's height.
- Team cards keep their normal fixed height in 对照模式. Only the boss cards stretch to fit.
- Bosses that the total team score does not fully cover are shown as uncleared. The part of a boss card past the last team's score extends below the team list and is styled differently.
- Add a **periodic boss setup**. Bosses come in rounds of exactly 5. All rounds share the same 5 bosses, with the same names and resistances in the same order. Only the required scores differ per round.
  - A boss's name and resistances are edited once and apply to every round.
  - Each round has its own 5 required scores.
  - Two rounds exist by default. A "＋ 轮次" button adds a new round, and the last round can be deleted (at least one round always remains).
  - The boss column lists them in order: round 1 bosses 1–5, then round 2 bosses 1–5, and so on.
- Each boss has **resistance tags** chosen from the 6 elements (冷凝, 气动, 导电, 热熔, 湮灭, 衍射). A boss can have 0, 1 or several resistances; 1 is most common. Tags appear as element icons on the boss cards.
- All boss data is persisted in localStorage.
- The boss column re-lays out live as team scores, team order, team count or boss data change.

## Capabilities

### New Capabilities
- `boss-compare-mode`: the 普通/对照 view toggle, the periodic boss setup (5 shared boss definitions with names and resistance tags, plus per-round required scores, 3 preset rounds by default, and add/delete round), and the score-aligned boss column beside a single-column team list that shows clear progress.

### Modified Capabilities
- `team-slots`: the "宽屏下队伍列表分两列展示" requirement gains an exception: in 对照模式 the team list stays single-column at every width.

## Impact

- `index.html`: add the mode toggle to `.teams-bar`, and wrap `#teams` in a container that can hold the boss column alongside it.
- `js/app.js`: new state `bossDefs: [{name, resists}] × 5`, `rounds: [[score × 5], …]` and `viewMode`, with load, save and migration. Render the boss editor table and the boss column, and compute boundary positions from rendered team card positions. Re-lay out on score input, render and resize. Add and delete rounds.
- `css/style.css`: compare-mode layout (boss column plus single team column, overriding the ≥1900px grid), boss card styles (cleared and uncleared states), and toggle styles. The mobile layout must stay usable.
- No new dependencies. The localStorage key `wuwa-deck-state` gains `bossDefs`, `rounds` and `viewMode`. Older saves load in normal mode with 5 default bosses (BOSS 1–5, no resistances) and the 3 preset rounds.
