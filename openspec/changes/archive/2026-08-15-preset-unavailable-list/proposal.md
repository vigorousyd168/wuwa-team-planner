## Why

Manually dragging 15 characters into the unavailable roster one by one is tedious. The user's unavailable roster is known upfront and should be pre-populated on first load without manual interaction.

## What Changes

- Add a `PRESET_UNAVAILABLE_IDS` constant in generate.py listing the 15 character IDs that are unavailable
- Modify `loadState()` to seed `unavailableIds` from the preset list when no prior localStorage data exists

The preset characters are:
达妮娅 (4), 西格莉卡 (5), 陆·赫斯 (6), 千咲 (9), 仇远 (10), 嘉贝莉娜 (11), 弗洛洛 (13), 夏空 (16), 赞妮 (17), 坎特蕾拉 (18), 菲比 (19), 洛可可 (21), 珂莱塔 (22), 折枝 (25), 吟霖 (29)

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
- `unavailable-character-roster`: First-load behavior changes — unavailable list is seeded from a preset rather than starting empty

## Impact

- `generate.py`: Add constant `PRESET_UNAVAILABLE_IDS`, modify JS_TEMPLATE's `loadState()`
- No UI changes required
- Existing localStorage state is unaffected (preset only applies on first run, no saved data)
