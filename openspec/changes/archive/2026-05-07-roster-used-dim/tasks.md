## 1. CSS 样式

- [x] 1.1 在 `generate.py` 的 CSS 中为 `.char-card.used` 添加置灰规则（`opacity: 0.35; filter: grayscale(60%);`）

## 2. 角色数据标记

- [x] 2.1 在 `generate.py` 构建 `characters` 数组时，为守岸人、莫宁、维里奈、卜灵、白芷添加 `"sustain": true` 字段，其余角色无此字段（默认 false）

## 3. 渲染逻辑

- [x] 3.1 在 `renderRoster()` 的 JS 模板中，从 `CHARACTERS` 构建 `SUSTAIN_IDS`（`sustain: true` 的角色 ID 集合）
- [x] 3.2 计算 `useCount`：遍历 `state.teams.flat()` 统计每个角色 ID 的出现次数
- [x] 3.3 卡牌生成时，按 `SUSTAIN_IDS.has(c.id) ? 2 : 1` 取阈值，`useCount[c.id] >= threshold` 时追加 `.used` class

## 4. 状态同步

- [x] 4.1 在 `drop` 事件处理（放入角色）后追加调用 `renderRoster()`
- [x] 4.2 在 `slot-clear` 点击事件（移除角色）后追加调用 `renderRoster()`
- [x] 4.3 在 `team-delete` 点击事件（删除队伍）后追加调用 `renderRoster()`

## 5. 重新生成

- [x] 5.1 运行 `python generate.py` 重新生成 `index.html`
