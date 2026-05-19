## 1. State Management

- [x] 1.1 Add `unavailableIds` Set to state object initialization
- [x] 1.2 Update `loadState()` to restore `unavailableIds` from localStorage
- [x] 1.3 Update `saveState()` to persist `unavailableIds` array to localStorage
- [x] 1.4 Add helper function `isUnavailable(characterId)` to check if character is in unavailableIds set

## 2. UI Structure

- [x] 2.1 Add "未获得 (N / 53)" section container below main roster in sidebar HTML
- [x] 2.2 Create `renderUnavailableRoster()` function to display unavailable characters grid
- [x] 2.3 Add CSS styles for unavailable roster section (fixed height, scrollable, border)
- [x] 2.4 Add CSS styles for unavailable character cards (reduced opacity ~0.6, gray tint)

## 3. Drag-and-Drop: Roster ↔ Unavailable

- [x] 3.1 Modify character card drag handlers to track source (main roster vs unavailable)
- [x] 3.2 Add dragover handler to unavailable section to accept drops and show visual feedback
- [x] 3.3 Add drop handler to unavailable section: move character to unavailable, update state
- [x] 3.4 Add dragover handler to main roster area to accept drops from unavailable
- [x] 3.5 Add drop handler to main roster area: move character back to available, update state
- [x] 3.6 Call `saveState()`, then `renderRoster()` and `renderUnavailableRoster()` after drops

## 4. Team Slot Validation

- [x] 4.1 Update team slot dragover handler to check `isUnavailable(draggingId)`
- [x] 4.2 Set `cursor: not-allowed` style and skip `.drag-over` class if character is unavailable
- [x] 4.3 Update team slot drop handler to reject drops from unavailable characters
- [x] 4.4 Add tooltip or visual hint when hovering unavailable character over slots (optional: CSS title or title attribute)

## 5. Character Roster Styling

- [x] 5.1 Modify `renderRoster()` to apply CSS class to cards if character is unavailable
- [x] 5.2 Add `.char-card.unavailable` CSS rule for visual distinction (reduced opacity, grayscale filter)
- [x] 5.3 Update `renderUnavailableRoster()` to apply same unavailable styling for consistency

## 6. State Synchronization

- [x] 6.1 Update roster and unavailable roster render calls whenever `unavailableIds` changes
- [x] 6.2 Ensure character usage counting in `renderRoster()` still works with unavailable characters marked

## 7. Integration & Testing

- [x] 7.1 Generate index.html via `generate.py` and verify all functionality works
- [ ] 7.2 Test drag character from main roster to unavailable section
- [ ] 7.3 Test drag character from unavailable section back to main roster
- [ ] 7.4 Test that unavailable characters show reduced opacity in main roster
- [ ] 7.5 Test drag unavailable character to team slot (should be blocked, cursor shows not-allowed)
- [ ] 7.6 Test drag available character to team slot (should work normally)
- [ ] 7.7 Test localStorage persistence: mark unavailable, refresh page, verify marks persist
- [ ] 7.8 Test counter updates: verify "N / 53" counter updates as characters are marked/unmarked
- [ ] 7.9 Test interaction with existing features (search, filters, team notes) still work
