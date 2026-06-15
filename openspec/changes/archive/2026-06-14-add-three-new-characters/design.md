## Context

本项目通过 `wuwa-wiki/characters.json` 集中管理角色数据，`generate.py` 读取该 JSON 文件并生成静态 HTML。三名新角色的头像图片已由用户提供并放置在 `wuwa-wiki/images/` 目录中。

## Goals / Non-Goals

**Goals:**
- 将洛瑟菈、露西、丽贝卡追加到 `characters.json` 末尾
- 确保图片文件名与 JSON 中的 `img` 字段一一对应

**Non-Goals:**
- 不修改 `generate.py` 或 HTML 模板
- 不变更任何置灰逻辑、拖拽逻辑或搜索逻辑

## Decisions

**直接编辑 JSON 数据文件**

唯一的实现路径：在 `characters.json` 末尾追加三个新对象。ID 依次为 54、55、56（沿用现有自增方式）。元素名称使用用户提供的原文（冷凝、衍射、导电），与 JSON 中现有条目格式一致。

| 字段 | 洛瑟菈 | 露西 | 丽贝卡 |
|------|--------|------|--------|
| id | 54 | 55 | 56 |
| name | 洛瑟菈 | 露西 | 丽贝卡 |
| element | 冷凝 | 衍射 | 导电 |
| star | 5 | 5 | 5 |
| img | 02cc3035c22145f586b11efae12055f220260610.png | 244760076f714546a0e79ecb75f8b5c920260608.png | b2b4eee99f294ee8b1296c09f7063e3e20260608.png |

## Risks / Trade-offs

- [风险] `冷凝` 与现有 `冰凝` 是否为同一元素 → 按用户提供的原文 `冷凝` 录入，若需统一元素名再单独处理
- [风险] JSON 格式损坏 → 追加后需验证 JSON 合法性（可用 `python -c "import json; json.load(open('wuwa-wiki/characters.json'))"` 检查）
