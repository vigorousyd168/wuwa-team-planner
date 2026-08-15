## Context

`renderRoster()` currently includes ALL characters and applies `.used` or `.unavailable` CSS classes to them. There is only one dimming style (`.char-card.used { opacity:0.35; filter:grayscale(60%) }`) — no distinct style exists for "not obtained" cards in the roster. Unavailable characters thus appear in both the main roster and the unavailable section simultaneously.

## Goals / Non-Goals

**Goals:**
- Main roster only shows obtained characters (i.e., `!isUnavailable(c.id)`)
- "Used up" cards (`.char-card.used`) and "not obtained" cards (`.char-card.unavailable`) have clearly different visual styles
- Roster count is meaningful after filtering

**Non-Goals:**
- Changing drag-and-drop behavior or drop targets
- Search/filter affecting the unavailable section

## Decisions

### Filter `isUnavailable` in `renderRoster()`
Add `!isUnavailable(c.id)` to the `list` filter in `renderRoster()`. Characters in the unavailable section are removed from the main grid entirely.

**Why:** The section separation already communicates the state. Showing the same card in two places adds confusion, not information.

**Alternative considered:** Keep unavailable characters in the main roster but show a stronger visual indicator — rejected because it still requires the user to mentally filter across the full list.

### Remove `unavailClass` from `renderRoster()` card HTML
Since unavailable characters are no longer rendered in the roster, the `unavailClass` variable and its application to card HTML are now dead code and should be removed.

### Roster count: show "available / obtained"
Change from `N / total` to `N 名可用 / M 名已获得`. "Available" = obtained and not used up. "Obtained" = not in unavailable list.

**Why:** The previous "N / total" conflated all characters. Now the roster only shows obtained characters, so count should reflect that context.

### Distinct CSS for the two states

| State | Class | Style |
|-------|-------|-------|
| Used up (配队次数用完) | `.char-card.used` | `opacity:0.4; filter:grayscale(50%)` — faded but still recognizable, color hint retained |
| Not obtained (未获得) | `.char-card.unavailable` | `opacity:0.5; filter:grayscale(100%) brightness(0.7)` — fully desaturated, darker, clearly "locked" |

**Why:** "Used up" characters are still accessible for future reference and may be freed; retain some color to show they're part of the active pool. "Not obtained" characters are not yet part of the pool at all; full grayscale + darkening signals they are locked.

## Risks / Trade-offs

- [Risk] User searches for an unavailable character by name → it won't appear in the main roster → Mitigation: search behavior in the unavailable section is unaffected; the unavailable section below the roster remains visible
- [Risk] Count label "可用 / 已获得" may be unfamiliar → small label change, low risk
