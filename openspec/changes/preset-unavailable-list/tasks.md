## 1. Implementation

- [x] 1.1 Add `PRESET_UNAVAILABLE_IDS` JS constant in generate.py with the 15 character IDs: `[4, 5, 6, 9, 10, 11, 13, 16, 17, 18, 19, 21, 22, 25, 29]`
- [x] 1.2 Modify `loadState()` in JS_TEMPLATE to use the preset when no prior localStorage state exists (replace `state.unavailableIds = []` with `state.unavailableIds = PRESET_UNAVAILABLE_IDS.slice()`)
- [x] 1.3 Run `generate.py` to regenerate `index.html`

## 2. Verification

- [x] 2.1 Open index.html and verify "未获得" section shows 15 characters on fresh load (clear localStorage first)
- [x] 2.2 Verify existing localStorage state is not overwritten (save some state, reload — preset should not re-apply)
- [x] 2.3 Verify the 15 characters display correctly in the unavailable roster with the expected names
