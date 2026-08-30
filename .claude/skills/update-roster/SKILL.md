---
name: update-roster
description: Use when new Wuthering Waves characters are released and the roster needs updating from the kurobbs wiki (更新角色库 / 添加新角色 / 同步wiki), or when characters.json is out of date.
---

# Update Roster from Kurobbs Wiki

## Overview

Sync `wuwa-wiki/characters.json` and portraits with the official character
catalogue at https://wiki.kurobbs.com/mc/catalogue/list?fid=1099&sid=1105.

That page is a JS-rendered SPA — fetching its HTML returns no character data.
The bundled script instead calls the underlying API
(`POST api.kurobbs.com/wiki/core/catalogue/item/getPage`, header `wiki_type: 9`,
`catalogueId=1105`) and maps its `skillAttr` codes to elements
(2=气动 3=导电 4=冷凝 5=热熔 6=衍射 7=湮灭).

## Workflow

1. Dry run — lists new characters and image changes, modifies nothing:

   ```
   python .claude/skills/update-roster/update_roster.py
   ```

2. **Confirm with the user which characters to add.** The wiki can contain
   entries the user doesn't want (e.g. extra 漂泊者 element variants). Never
   `--add-all` without confirmation.

3. Apply (downloads portraits, appends to characters.json, reruns generate.py):

   ```
   python .claude/skills/update-roster/update_roster.py --add 名字A 名字B
   ```

4. Ask the user whether any added character is a sustain/healer (辅助). If so,
   add its name to `SUSTAIN_NAMES` in `generate.py` and rerun it.

5. Verify: open `index.html`, search for each new name, confirm the card and
   portrait render.

## Gotchas

- Name matching normalizes 「·」 to 「-」 (wiki: 秧秧·玄翎, local: 秧秧-玄翎).
  A "new" character that looks like a rename of an existing one probably needs
  the same treatment — check before adding a duplicate.
- This project's canonical name for the ice element is 冷凝. The wiki calls it
  冰凝 — always translate to 冷凝 (the script's ATTR_ELEMENT already does).
- Portrait filenames come from the wiki CDN URL and are kept verbatim — they
  double as change detection (`IMG-CHANGED` lines in the dry run).
