## Context

Currently, the tool displays all 53 characters in a single roster. Players have no way to mark characters they haven't obtained, leading to potential team configurations with unavailable characters. The app uses HTML5 drag-and-drop with localStorage for persistence. The sidebar contains the character roster; the main area contains team slots.

## Goals / Non-Goals

**Goals:**
- Provide a secondary "Unavailable Characters" roster below the main roster where users can mark unowned characters
- Enable drag-and-drop from main roster to unavailable area (and vice versa)
- Prevent team slot drops of unavailable characters with clear visual feedback
- Persist unavailable character list to localStorage
- Visually distinguish unavailable characters in the main roster

**Non-Goals:**
- Automatic detection of obtained characters from game API (manual marking only)
- Bulk import/export of unavailable character lists
- Character acquisition tracking or history

## Decisions

### 1. State Storage Structure
**Decision:** Extend state object with `unavailableIds` (Set of character IDs) in addition to existing `teams` and `notes`.

**Rationale:** Mirrors existing state pattern; localStorage already handles persistence. Simple Set-based lookup for O(1) drop validation.

**Alternatives considered:**
- Store as part of character objects: would require re-encoding character data
- Use IndexedDB: unnecessary complexity for simple boolean flag per character

### 2. UI Layout
**Decision:** Add fixed "未获得" section below roster search with:
- Label row: "未获得 (N / 53)"
- Grid container with same card styling as main roster
- Scrollable area (max-height: 120px, flex: 0 0 auto)

**Rationale:** Maintains visual consistency; limited height prevents excessive sidebar bloat. Fixed height lets users see both rosters simultaneously.

**Alternatives considered:**
- Collapsible panel: adds interaction complexity; users might forget it exists
- Bottom sidebar panel: would require main layout restructure

### 3. Drag-Drop Validation
**Decision:** 
- Main roster → Unavailable: Always allow (mark as unavailable)
- Unavailable → Main roster: Always allow (unmark)
- Unavailable → Team slots: Block with `e.preventDefault()` and visual feedback (cursor not-allowed)

**Rationale:** Clear state transitions; no ambiguity. Blocks error-prone drops while allowing recovery.

**Alternatives considered:**
- Disable drag on unavailable cards: less flexible; can't recover without UI button
- Gray out unavailable cards in main roster: done, but dragging still allowed for reassignment

### 4. Visual Styling
**Decision:**
- Unavailable section: gray background container with border
- Cards in unavailable roster: reduced opacity (0.6) + muted colors
- Team slot drag-over with unavailable card: show red "not-allowed" cursor and tooltip hint "Cannot use unavailable character"

**Rationale:** Consistent with existing grayscale treatment for used characters. Red feedback is distinct from normal drag-over (cyan).

### 5. State Synchronization
**Decision:** Calls to `saveState()` after any unavailable list mutation; re-render unavailable roster and main roster (to update used-character styling).

**Rationale:** localStorage persists across sessions; roster re-render ensures UI consistency when crossing the unavailable/available boundary.

## Risks / Trade-offs

- [Risk] Unavailable marked character that's already in a team: The character remains in team slots but is marked unavailable. Could be confusing.
  - Mitigation: Update design doc / UX guidance to mention user should clean teams first, OR automatically remove from teams on mark-unavailable (more aggressive but less error-prone)

- [Risk] Performance: Re-rendering both rosters on every unavailable mutation could lag with 53 characters.
  - Mitigation: Use small character set (53 chars) → not a bottleneck. Defer optimization if needed.

- [Risk] Mobile/small screens: Two rosters in sidebar consumes vertical space.
  - Mitigation: Collapsible unavailable section (future enhancement); current fixed-height layout is acceptable for desktop-first tool.

## Migration Plan

No data migration needed. Existing localStorage state remains valid; new `unavailableIds` field defaults to empty array on first run. Users with existing team data can immediately start marking unavailable characters.

## Open Questions

1. Should marking a character as unavailable **automatically remove it from all team slots**, or just prevent new drops?
   - Current design: just prevent new drops (less disruptive; user has explicit control)
   - Alternative: auto-remove (cleaner state; may surprise users)
   - **Recommendation:** Keep current design; add optional "Clean Teams" button if user feedback indicates confusion
