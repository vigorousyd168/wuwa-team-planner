## Context

`#teams` 目前是 `display:flex; flex-direction:column; gap:10px; overflow-y:auto` 的单列滚动容器（[index.html:173-176](../../../index.html#L173-L176)），`renderTeams()` 把 `state.teams` 直接 map 成一串平铺的 `.team-row`（[index.html:512-524](../../../index.html#L512-L524)）。

约束：

- 单个 `.team-row` 是横向 flex：50px 编号 + 3×74px 槽位 + `min-width:150px` 的备注 + 删除按钮 + gap，**最小可用宽度约 460px**。两列并排需要主区约 950px 以上。
- 页面已有 780px 断点用于移动端 tab 切换（[index.html:240](../../../index.html#L240)），主区在窄屏时占满全宽。
- 所有交互（槽位点击/拖放、备注、删除、队伍拖拽排序）的事件绑定都以 `container.querySelectorAll(...)` 从 `#teams` 向下查询，**不依赖 `.team-row` 是 `#teams` 的直接子元素**，也不依赖 DOM 顺序——排序用的是 `data-ti` 索引与 `moveTeam(from,to)`。

## Goals / Non-Goals

**Goals:**

- 宽屏下队伍列表以 2 列展示，同屏可见队伍数约翻倍。
- 窄屏自动回退单列，不出现挤压或横向滚动。
- 纯 CSS 实现，`renderTeams()` 的 DOM 结构与全部事件逻辑零改动。

**Non-Goals:**

- 不改变队伍数据结构、编号规则、拖拽排序语义、备注与持久化。
- 不做列数可配置（3 列、用户自选列数）。
- 不重新设计 `.team-row` 内部布局以适应更窄的列。

## 宽度实测（Playwright，决策依据）

角色库侧栏固定占 50% 宽度，队伍面板内容宽 = 视口/2 − 36：

| 视口 | 队伍面板内容宽 | 单列可容纳 |
|---|---|---|
| 1280px | 604px | 1 列 |
| 1440px | 684px | 1 列 |
| 1920px | 924px | 2 列（需列宽 ≤457px）|

原始 `.team-row` 不换行所需最小宽度实测 **≈513px**（21 手柄 + 50 编号 + 238 槽位 + 100 备注 + 30 删除 + gaps + padding），超出 1920px 下的 457px 列宽。**若不压缩行内尺寸，两列在任何现实视口下都无法成立**。

实测还证明"降低阈值、允许备注换行"不可行：换行后行高由 96px 涨到 178px，两列每队占 89px vs 单列 96px，仅省 7%。

## Decisions

### 决策 1：用 `@media (min-width: 1900px)` 门控两列，而非 `auto-fit` 自适应

```css
@media (min-width: 1900px) {
  #teams { display: grid; grid-template-columns: 1fr 1fr; align-content: start; }
  #teams:has(.no-teams) { display: flex; flex-direction: column; }
  .team-row { gap: 8px; padding: 10px; }
  .team-num { width: 42px; }
  .slot { width: 62px; height: 62px; }
  .team-note { height: 62px; }
}
```

用户主用 1920px 及以上屏幕，目标锁定在此档生效。显式媒体查询而非 `auto-fit`：两列所需的行内压缩（槽位、编号、间距）必须与列数切换**同时**发生，`auto-fit` 无法表达这种联动；且 1900px 以下不落入媒体查询，实测确认零回归。

**备选方案：**

- **`auto-fit` + `minmax`**：已实现并实测——1920px 下仍为单列（列宽 457 < 行需 513），无效，弃用。
- **CSS 多列（`columns: 2`）**：列优先填充更贴近"从中间劈开"，但会在列间分割元素，且 `overflow-y:auto` 下列高平衡跨浏览器差异大。不采用。
- **JS 分成两个 `.team-col` 容器**：可精确控制列优先顺序，但要改 `renderTeams()` 并处理跨列拖放。为纯视觉需求引入过多复杂度，不采用。

### 决策 2：接受行优先（row-major）的排列顺序

Grid 按行优先填充，即 `01 02 / 03 04 / 05 06`。行优先下**视觉顺序与 `data-ti` 索引顺序一致**，队伍拖拽排序的落点心智模型不会错位。奇数支队伍时最后一行只占左列，满足"左列多 1 支"的均分描述。

### 决策 3：两列模式下压缩 `.team-row` 内部尺寸（推翻原"不调整内部布局"的判断）

为把行宽从 513px 压到 ≤457px：槽位 74→62px、编号列 50→42px、行 gap 12→8px、padding 14→10px、备注高度同步 74→62px。备注 `min-width` 150→100px 为**全局**改动（用户明确要求），其余压缩仅在 ≥1900px 内生效。

实测结果：1920px 下行高 84px、不换行，每队垂直占用 47px vs 单列 106px，**省 56%**；20 支队伍同屏可见 18 支（原约 8 支）。

## Risks / Trade-offs

- **[两列模式下角色头像由 74px 缩到 62px]** → 16% 缩小，实测截图确认头像与名称仍清晰可辨。这是让两列成立的必要代价。
- **[备注 `min-width` 全局降到 100px 影响窄屏]** → 实测 900/1280/1440px 下行高、槽位、换行行为与改动前完全一致；900px 下删除按钮的裁切反而消失。无回归。
- **[1900px 断点是硬编码的]** → 与 50% 侧栏宽度耦合；若日后调整侧栏比例需同步复算。已在本文档记录换算公式（面板内容宽 = 视口/2 − 36）。
- **[队伍拖拽排序在 2 列下的落点判断]** → 逻辑未改（`moveTeam` 基于 `data-ti`）。已实测：拖 01 到 04 位后顺序与单列时一致，无残留 `.tr-over` 高亮。
- **[`.no-teams` 空态在 grid 下失去垂直居中]** → 用 `#teams:has(.no-teams)` 回退到原 flex 布局，比 `grid-column: 1/-1` 更完整地保留原行为。实测横向纵向均居中。

## Migration Plan

无数据迁移、无依赖变更。改动集中在 `index.html` 的一段媒体查询加一处 `min-width`，删除即完全回滚。

## Open Questions

- 无。若日后希望 1440px 也能两列，需要进一步改造（收窄角色库侧栏，或把备注移出队伍行），属于后续变更。
