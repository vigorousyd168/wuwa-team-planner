## Why

玩家在规划鸣潮（Wuthering Waves）多队伍阵容时，缺乏可视化工具来拖拽角色卡牌、分配队伍，导致只能依靠脑记或手写笔记来管理多达6支以上的队伍搭配。本工具提供一个轻量、离线可用的 HTML 小工具，让玩家直观地完成编队可视化。

## What Changes

- 新增独立 HTML 单文件工具 `index.html`，无需后端或构建工具
- 从鸣潮 Wiki 抓取角色数据（头像、名称、属性等），展示在角色卡牌库中
- 支持将角色卡牌拖拽到队伍槽位，实现编队可视化
- 默认展示 6 支队伍（每队 3 个槽位），可通过按钮增减，最多 20 队
- 每支队伍右侧提供文本输入框，供玩家填写笔记

## Capabilities

### New Capabilities

- `character-roster`: 角色卡牌库——从 Wiki 加载角色列表，以卡牌形式展示，供玩家点选或拖拽
- `team-slots`: 队伍槽位——每队 3 个卡牌槽，支持拖拽放入/移出角色，队伍数量可增减（6～20队）
- `team-notes`: 队伍备注——每队右侧文本框，供玩家输入队伍笔记，内容实时保存在 localStorage

### Modified Capabilities

## Impact

- 纯前端单文件（HTML + CSS + JS），无外部依赖框架
- 通过 fetch 请求 `https://wiki.kurobbs.com/mc/catalogue/list` 获取角色数据（需处理 CORS 或采用静态内嵌数据方案）
- 数据持久化依赖浏览器 localStorage
