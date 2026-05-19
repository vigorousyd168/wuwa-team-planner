## 1. 项目骨架

- [x] 1.1 创建 `index.html` 单文件，定义 HTML 基础结构（head、body 区域划分）
- [x] 1.2 在 `<style>` 标签中建立 CSS 变量体系（主题色、字体、间距）和全局重置样式
- [x] 1.3 在 `<script>` 标签中定义应用状态结构（teams 数组、notes 对象）

## 2. 角色数据抓取（一次性初始化）

- [x] 2.1 用 DevTools 探查 `https://wiki.kurobbs.com/mc/catalogue/list` 的底层 API 端点和响应 JSON 结构，记录字段名（角色名、属性、头像 URL 等）
- [x] 2.2 实现 IndexedDB 初始化逻辑：打开 `wuwa-deck` 库，创建 `characters` 对象仓库（keyPath: `id`）
      > 改为直接嵌入：用户已预先下载 Wiki 页面，通过 Python 脚本解析 HTML + 本地图片，生成 base64 数据内嵌在 HTML 中，无需 IndexedDB
- [x] 2.3 实现 `fetchAndStoreCharacters()` 函数：fetch Wiki API → 解析角色列表 → 遍历每个角色
      > 由 generate.py 完成：解析保存的 HTML，提取53个角色的名称、属性、头像
- [x] 2.4 对每个角色的头像 URL，执行 `fetch → arrayBuffer → base64` 转换，将 `{ id, name, element, imageBase64 }` 写入 IndexedDB
      > 由 generate.py 完成：读取本地图片文件，resize 到 240×320 JPEG，base64 编码后嵌入 HTML
- [x] 2.5 实现初始化进度条 UI：显示"正在抓取 X / Y"，完成后自动隐藏初始化界面并进入主界面
      > 不需要：数据已预嵌，页面打开即可用
- [x] 2.6 实现 `loadCharactersFromDB()` 函数：从 IndexedDB 读取全部角色，失败时返回空数组并显示"请重新初始化"提示
      > 数据直接读取 CHARACTERS 常量，无需 DB 查询
- [x] 2.7 在页面加载时检测 IndexedDB 是否有角色数据：有则直接加载，无则显示初始化界面
      > 不需要：数据已预嵌
- [x] 2.8 提供"刷新角色库"按钮，允许用户重新执行初始化流程（覆盖旧数据）
      > 不需要：数据已预嵌，更新角色只需重新运行 generate.py

## 3. 角色卡牌库

- [x] 3.1 实现角色卡牌库区域的 HTML 结构（标题、搜索框、卡牌网格容器）
- [x] 3.2 实现 `renderRoster()` 函数，根据 IndexedDB 加载的角色数据动态生成卡牌 DOM（头像使用 base64 data URI）
- [x] 3.3 为每张卡牌添加 `draggable="true"` 及 `dragstart` 事件，携带角色 ID
- [x] 3.4 实现 base64 图片缺失时的回退（显示首字圆形徽标，不依赖外部 URL）
- [x] 3.5 实现搜索框的 `input` 事件监听，实时过滤卡牌库显示

## 4. 队伍面板

- [x] 4.1 实现队伍列表区域的 HTML 结构（队伍容器、添加队伍按钮）
- [x] 4.2 实现 `renderTeams()` 函数，根据状态渲染所有队伍行
- [x] 4.3 每行队伍包含：队伍编号、3个槽位、备注文本框、删除队伍按钮
- [x] 4.4 为每个槽位实现 `dragover`（阻止默认行为）和 `drop` 事件处理，更新状态并重新渲染
- [x] 4.5 拖拽悬停时为槽位添加高亮 CSS class，离开时移除
- [x] 4.6 实现槽位内角色卡牌的"×"移除按钮点击事件
- [x] 4.7 实现"添加队伍"按钮：追加空队伍，上限20队时禁用按钮
- [x] 4.8 实现"删除队伍"按钮：移除对应队伍及其备注数据

## 5. 备注功能

- [x] 5.1 为每行队伍的 textarea 绑定 `input` 事件，实时更新状态中的备注内容

## 6. 数据持久化

- [x] 6.1 实现 `saveState()` 函数，将 teams 和 notes 序列化为 JSON 存入 `localStorage['wuwa-deck-state']`
- [x] 6.2 实现 `loadState()` 函数，页面加载时从 localStorage 恢复队伍状态（无数据则初始化6支空队伍）
- [x] 6.3 在所有状态变更操作（槽位变更、队伍增删、备注输入）后调用 `saveState()`
- [x] 6.4 确认角色库（IndexedDB）与队伍状态（localStorage）相互独立：重新抓取角色库不清空编队数据
      > 角色数据已内嵌，不存在清空问题；队伍状态独立存于 localStorage['wuwa-deck-state']

## 7. 样式完善

- [x] 7.1 实现整体页面布局（角色库与队伍面板左右分栏或上下分区）
- [x] 7.2 为角色卡牌、槽位、队伍行设计视觉样式（参考鸣潮深色风格）
- [x] 7.3 为空槽位、悬停状态、已填充状态设计区分样式
- [x] 7.4 确保页面在常见桌面分辨率（1280px 以上）下布局合理，内容不溢出
