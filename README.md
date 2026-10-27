# Wuthering Waves Team Planner

A local team-planning tool for Wuthering Waves (鸣潮编队小助手). Build and organize teams by drag-and-dropping characters from your owned roster.

## Features

- **Character roster** — all characters with portraits, element icons, and star ratings
- **Unavailable list** — mark characters you haven't obtained; drag them back when you pull them
- **Team slots** — teams of 3, with per-team notes
- **Team scores** — enter a score for each team; the header shows the live total (总分 Total)
- **Sustain logic** — healer/support characters (守岸人, 莫宁, 维里奈, 卜灵, 白芷) can appear in up to 2 teams before being dimmed; one extra non-sustain character can also be given ×2 via the "当期2体力角色" dropdown
- **Search & filter** — search by name or click an element chip to filter the roster
- **Compare mode (对照模式)** — switch the team list to 对照 to see boss clear progress: a boss column beside the teams lines each boss up against the cumulative team scores, marked cleared, partly cleared, or not reached. Bosses repeat in rounds of 5 that share names and resistance tags, and each round has its own required scores (3 preset rounds; add more with "＋ 轮次")
- **Persistent state** — teams, notes, scores, unavailable list, view mode, and boss setup are saved to `localStorage`

## Usage

Open `index.html` in any modern browser — no server needed.

## Project structure

```
wuwa-team-planner/
├── index.html           # app markup (open this in a browser)
├── css/
│   └── style.css        # app styles
├── js/
│   ├── app.js           # app logic
│   └── data.js          # generated character/icon data (do not edit by hand)
├── generate.py          # builds js/data.js from character data
└── wuwa-wiki/
    ├── characters.json  # character data (id, name, element, star, img)
    └── images/          # character portraits and element icons
```

## Updating character data

Edit `wuwa-wiki/characters.json` to add or remove characters, then re-run `python generate.py` to rebuild `js/data.js`.
