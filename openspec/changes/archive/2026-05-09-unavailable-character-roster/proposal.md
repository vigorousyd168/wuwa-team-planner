## Why

Players in Wuthering Waves may not have obtained all characters yet. Currently, the tool displays all characters equally, making it hard to distinguish between owned and unowned characters. This leads to accidental team configurations with characters the player doesn't actually have.

## What Changes

- Add an "Unavailable Characters" section in the left sidebar below the character roster
- Enable drag-and-drop: users can drag characters from the roster to the "Unavailable Characters" area to mark them as unowned
- Prevent unavailable characters from being dropped into team slots (block invalid drops)
- Persist unavailable character list to localStorage alongside team state
- Visual feedback: unavailable characters should be visually distinct in the roster when marked

## Capabilities

### New Capabilities
- `unavailable-character-roster`: A secondary roster area below the main character library where users can collect characters they haven't obtained. Unavailable characters are excluded from team slot drops.

### Modified Capabilities
- `character-roster`: Extend roster filtering to account for unavailable character status; support drag-to-mark-unavailable workflow
- `team-slots`: Prevent dropped characters if they are marked as unavailable

## Impact

- UI: Adds new section to left sidebar (~80px height for container + scrollable grid)
- State: Extends localStorage schema to include `unavailableCharacters` array (character IDs)
- Drag-drop: Modifies drop validation in team slots to check unavailable status
- Filtering: Roster rendering considers unavailable status for visual styling
