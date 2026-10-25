## 1. 状态与阈值

- [x] 1.1 `state` 初始值新增 `doubleId: null`；`load()` 读取 `p.doubleId`（不是数字则为 `null`），默认分支也置为 `null`
- [x] 1.2 `threshold(c)` 改为 `(c.sustain || c.id === state.doubleId) ? 2 : 1`
- [x] 1.3 `markUnavailable(id)` 中若 `id === state.doubleId` 则将 `state.doubleId` 置为 `null`

## 2. 选择器 UI

- [x] 2.1 `index.html` 的 `.sb-top` 中、`#elem-chips` 下方新增带标签"当期2体力角色"的 `<select id="double-pick">`
- [x] 2.2 新增 `renderDoublePick()`：生成"无" + 已获得非 sustain 角色的选项（按 `CHARACTERS` 顺序），选中值为 `state.doubleId`（若不在选项中则选中"无"）；在 `renderAll()` 中调用
- [x] 2.3 绑定 `change` 事件：写入 `state.doubleId`（空值为 `null`），然后 `save(); renderAll()`
- [x] 2.4 `css/style.css` 中为下拉框添加与搜索框一致的深色样式

## 3. 卡牌角标

- [x] 3.1 `renderRoster()` 中被指定角色的卡牌渲染 `<span class="cc-sustain">体 ×2</span>`
- [x] 3.2 `css/style.css` 中无需新增样式，复用 `.cc-sustain` 的绿色角标

## 4. 文档与验证

- [x] 4.1 `README.md` 的 Sustain logic 一条补充额外 ×2 角色说明
- [x] 4.2 在浏览器中验证：指定普通角色后第一次使用不置灰、第二次使用置灰，计数标签正确
- [x] 4.3 验证更换/取消指定不会修改已有槽位；刷新后指定仍保留；清空 localStorage 中的 `doubleId` 字段后正常加载为"无"
- [x] 4.4 验证将指定角色标记为未获得后下拉框变为"无"，取回后指定不恢复

## 5. 超额槽位警告

- [x] 5.1 `renderSlot()` 接收 `useCounts()` 结果，使用次数大于 `threshold(c)` 的已填槽位加 `.s-warn` 类和"编入次数超出上限"提示
- [x] 5.2 `css/style.css` 中新增 `.slot.s-warn` 红色描边样式
- [x] 5.3 验证：取消已用两次的指定角色后两个槽位显示警告；重新指定或移除一个槽位后警告消失
