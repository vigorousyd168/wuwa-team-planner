## Context

置灰阈值目前由 `threshold(c)` 决定：`c.sustain ? 2 : 1`，`sustain` 标记来自 `generate.py` 生成的 `js/data.js`，是只读的内置数据。卡牌在使用次数达到阈值后加 `.used` 类并失去 `draggable`，也不再响应点击选择。所有用户状态集中在 `state`（`teams` / `notes` / `unavailableIds`），整体序列化到 localStorage 键 `wuwa-deck-state`。

## Goals / Non-Goals

**Goals:**
- 用户可指定 0 或 1 名非生存治疗角色，使其阈值变为 2
- 指定结果随其他状态一起持久化，旧存档兼容
- 改动集中在 `threshold()` 一处判断，其余置灰/可拖入逻辑自动生效

**Non-Goals:**
- 不支持同时指定多名角色
- 不支持修改生存治疗角色本身的阈值，也不支持 ×3 等其他次数
- 不修改 `generate.py` / `characters.json` 中的 `sustain` 数据
- 不在取消指定时自动清理已编入的超额槽位

## Decisions

**1. 状态字段：`state.doubleId: number | null`**
存入现有 `state` 对象，随 `save()` 一并写入。`load()` 中若字段不存在或不是数字，则置为 `null`。
备选：单独的 localStorage 键——会让存读逻辑分散，否决。

**2. 阈值判断：`threshold(c)` 返回 `(c.sustain || c.id === state.doubleId) ? 2 : 1`**
所有使用阈值的地方（计数标签、`.used`、`draggable`、点击选择）都已经走 `threshold()`，只需改这一处。

**3. 选择器：原生 `<select id="double-pick">`，放在 `.sb-top` 的属性筛选下方**
选项为"无"（value 为空）+ 已获得且非 `sustain` 的角色，按 `CHARACTERS` 原顺序。每次 `renderAll()` 时重新生成选项并设置选中值，这样标记未获得/取回后列表自动更新。`change` 事件写入 `state.doubleId`，然后 `save(); renderAll()`。
备选：在卡牌上加切换按钮——用户选择了下拉框方案。

**4. 与未获得标记联动**
`markUnavailable(id)` 中若 `id === state.doubleId`，则将 `doubleId` 置为 `null`。未获得角色不能编入队伍，保留它的 ×2 指定没有意义，而且它也不在下拉选项里，会导致选择框显示状态与实际状态不一致。

**5. 卡牌角标**
被指定角色的卡牌显示与生存治疗角色相同位置的角标，文案为"体 ×2"，复用 `.cc-sustain` 的绿色样式，仅通过文案区分内置 ×2 与用户指定的 ×2。

**6. 更换/取消指定时不改动槽位**
若原角色已出现在 2 个槽位，取消后它只是保持置灰（2 ≥ 1），槽位不会被修改。这与现有"多槽位保持置灰"的行为一致，并且不会悄悄删除用户的编队。

## Risks / Trade-offs

- [取消指定后某角色"超额"占用 2 个槽位，用户可能没注意到] → 对使用次数超过 `threshold()` 的角色所在槽位加 `.s-warn` 红色描边与"编入次数超出上限"提示；重新指定该角色或移除多余槽位后警告自动消失
- [存档中的 `doubleId` 指向已不存在的角色 id（角色数据更新后被移除）] → `threshold()` 只做 id 比较，不会出错；渲染时若 `BY_ID` 中找不到该 id，则视为"无"并在下拉框中显示"无"
- [存档中的 `doubleId` 指向后来被设为 `sustain` 的角色] → 阈值本来就是 2，不影响结果；下拉框中没有该选项，显示"无"，用户下次选择时会被覆盖
