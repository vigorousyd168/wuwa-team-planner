## Context

`renderRoster()` 目前在页面初始化、搜索框输入、属性筛选时被调用，但在队伍状态变更（放入角色、移除角色、删除队伍）后只调用 `renderTeams()`，不重新渲染卡牌库。置灰功能需要卡牌库与队伍状态保持同步。

## Goals / Non-Goals

**Goals:**
- 卡牌库中，普通角色使用 ≥ 1 次置灰，生存治疗角色使用 ≥ 2 次置灰
- 状态同步：每次队伍变更后卡牌库即时更新
- 视觉设计不影响卡牌的可拖拽性（置灰卡牌仍可拖入新槽位）

**Non-Goals:**
- 不阻止同一角色被拖入多支队伍（已有规则不变）
- 不在槽位内做任何视觉标记（只改卡牌库侧）

## Decisions

### 决策 1：用使用次数计数 + 阈值判断控制置灰，逻辑在 `renderRoster()` 内计算

**选择：** 在 `renderRoster()` 中统计每个角色在所有槽位中出现的次数（`useCount`），并与该角色对应的阈值（`dimThreshold`）比较，超过则添加 `.used` class。

```js
const SUSTAIN_IDS = new Set([/* 守岸人、莫宁、维里奈、卜灵、白芷 的 id */]);
const useCount = {};
state.teams.flat().filter(Boolean).forEach(id => {
  useCount[id] = (useCount[id] || 0) + 1;
});
// 卡牌生成时：
const threshold = SUSTAIN_IDS.has(c.id) ? 2 : 1;
const isUsed = (useCount[c.id] || 0) >= threshold;
// class="char-card ... ${isUsed ? 'used' : ''}"
```

```css
.char-card.used { opacity: 0.35; filter: grayscale(60%); }
```

**原因：** 在原有集合方案上做最小扩展——将"是否存在"改为"计数 ≥ 阈值"，无需新状态字段，逻辑自包含在 `renderRoster()` 中。

**`SUSTAIN_IDS` 的维护：** 生存治疗角色名单（守岸人、莫宁、维里奈、卜灵、白芷）在 `generate.py` 生成 `CHARACTERS` 数组时写入 `sustain: true` 字段，JS 运行时据此构建 `SUSTAIN_IDS`，避免硬编码 ID 数字。

**替代方案：** 维护独立的 `usedIds` 状态变量并在 DOM 上动态切换 class（不完整重渲染）→ 复杂度高，收益不明显，放弃。

### 决策 2：在所有队伍状态变更后追加调用 `renderRoster()`

**选择：** 在 `drop`、`slot-clear`、`team-delete` 三处事件处理中，`renderTeams()` 之后追加 `renderRoster()`。

**原因：** `renderRoster()` 已有完整的过滤逻辑（搜索词、属性筛选），直接复用不引入冗余代码。53 张卡牌的 DOM 重建对性能无实质影响。

## Risks / Trade-offs

- **重渲染卡牌库有轻微闪烁风险** → 卡牌数量少（53张），实测不可感知；如有问题可改为仅切换 class。
- **同一角色出现在多个槽位时只显示一次置灰** → 符合预期，集合自动去重。
