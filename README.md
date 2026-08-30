# wuwa-deck

A local team-planning tool for Wuthering Waves (鸣潮编队小助手). Build and organize up to 20 teams by drag-and-dropping characters from your owned roster.

## Features

- **Character roster** — all characters with portraits, element icons, and star ratings
- **Unavailable list** — mark characters you haven't obtained; drag them back when you pull them
- **Team slots** — up to 20 teams of 3, with per-team notes
- **Sustain logic** — healer/support characters (守岸人, 莫宁, 维里奈, 卜灵, 白芷) can appear in up to 2 teams before being dimmed
- **Search & filter** — search by name or click an element chip to filter the roster
- **Persistent state** — teams, notes, and unavailable list are saved to `localStorage`

## Usage

Open `index.html` in any modern browser — no server needed.

## Project structure

```
wuwa-deck/
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
