## 1. 更新角色数据

- [x] 1.1 在 `wuwa-wiki/characters.json` 末尾追加洛瑟菈（id: 54，冷凝，5星，img: 02cc3035c22145f586b11efae12055f220260610.png）
- [x] 1.2 在 `wuwa-wiki/characters.json` 末尾追加露西（id: 55，衍射，5星，img: 244760076f714546a0e79ecb75f8b5c920260608.png）
- [x] 1.3 在 `wuwa-wiki/characters.json` 末尾追加丽贝卡（id: 56，导电，5星，img: b2b4eee99f294ee8b1296c09f7063e3e20260608.png）

## 2. 验证

- [x] 2.1 验证 `wuwa-wiki/characters.json` JSON 格式合法（`python -c "import json; json.load(open('wuwa-wiki/characters.json'))"` 无报错）
- [x] 2.2 运行 `generate.py` 生成最新 HTML，确认三名新角色出现在角色卡牌库中
