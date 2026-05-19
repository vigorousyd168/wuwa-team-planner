## Context

`loadState()` currently seeds `unavailableIds` as `[]` on first run. Users must manually drag characters to the unavailable section. The user's unavailable list is static and known — embedding it as a one-time default eliminates setup friction.

## Goals / Non-Goals

**Goals:**
- Seed `unavailableIds` with 15 specific character IDs on first run (no existing localStorage)
- Leave existing saves untouched

**Non-Goals:**
- UI for editing the preset list
- Multi-user or per-profile presets

## Decisions

### Embed preset as JS constant in generate.py
The 15 IDs are baked into the generated HTML via a `PRESET_UNAVAILABLE_IDS` JS array in `generate.py`. `loadState()` uses this array when no prior state exists.

**Why:** Consistent with how character data is embedded. No runtime fetch needed. Changing the preset requires re-running `generate.py`, which is acceptable for a personal tool.

**Alternative considered:** Store preset in a separate JSON config file — unnecessary complexity for a static list that rarely changes.

## Risks / Trade-offs

- [Risk] User clears localStorage — preset re-applies on next load → This is the desired behavior (first-run default)
- [Risk] User adds a preset character back to available manually → State is correctly saved to localStorage; preset only runs when no saved state exists

## Migration Plan

No migration needed. Existing localStorage state is not modified. On fresh load, the preset populates `unavailableIds`.
