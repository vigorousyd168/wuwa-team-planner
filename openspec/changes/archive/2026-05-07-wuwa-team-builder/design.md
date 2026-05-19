## Context

目标是交付一个**单文件 HTML 工具**，用户直接双击即可在浏览器中使用，无需安装任何依赖。工具用于鸣潮游戏的多队伍阵容规划，核心体验是拖拽角色卡牌到队伍槽位。

角色数据来源：`https://wiki.kurobbs.com/mc/catalogue/list`（光环游戏 Wiki）。角色图片和数据**只在首次初始化时抓取一次**，之后全部从本地存储读取，不再请求网络。

## Goals / Non-Goals

**Goals:**
- 单文件 HTML，零依赖，**初始化后完全离线可用**
- 首次启动时一键抓取所有角色数据和图片，存入本地
- 拖拽式角色分配，直观流畅
- 6～20 支队伍，每队 3 个槽位 + 备注文本框
- 队伍配置和备注通过 localStorage 持久化
- 角色卡牌展示头像、名称、属性信息

**Non-Goals:**
- 不在每次页面加载时请求 Wiki（初始化后无需联网）
- 不实现账号系统或云同步
- 不实现伤害计算、属性加成等游戏机制
- 不实现多语言切换

## Decisions

### 决策 1：首次初始化一键抓取，图片以 base64 存入 IndexedDB

**选择：**
- 首次打开工具时（IndexedDB 无角色数据），显示"初始化角色库"界面
- 用户点击"开始抓取"按钮，工具依次：
  1. fetch Wiki 角色列表页面或其底层 API，解析角色名称、属性、头像 URL
  2. 对每张头像图片执行 `fetch → arrayBuffer → base64` 转换
  3. 将角色元数据（id、name、element）和 base64 图片一并写入 IndexedDB（库名 `wuwa-deck`，表 `characters`）
  4. 显示进度条，全部完成后自动进入主界面
- 此后每次打开均从 IndexedDB 加载，无需联网

**为何用 IndexedDB 而非 localStorage：** 角色图片 base64 编码后每张约 30～100 KB，50 个角色约 2～5 MB，会触及 localStorage 的 5 MB 上限。IndexedDB 无实际容量限制，且原生支持 Blob/ArrayBuffer，更适合存储二进制数据。角色元数据（纯 JSON）仍放 localStorage，用于快速读取列表。

**CORS 处理：** Wiki 图片 CDN 通常允许跨域 fetch（`Access-Control-Allow-Origin: *`）。Wiki 角色列表页若为 SPA，需先探查其底层 JSON API 端点（通常有 CORS 头）；若 HTML 页面无 CORS，则改为解析 `fetch` 返回的 HTML 字符串（DOMParser 方式，不受同源限制）。

**替代方案：** 静态内嵌 CDN URL（每次加载都请求网络，图片可能失效）→ 放弃。Node 爬虫脚本（需要用户安装 Node.js）→ 放弃，破坏零依赖目标。

---

### 决策 2：使用原生 HTML5 Drag and Drop API

**选择：** 用 `draggable="true"` + `dragstart`/`dragover`/`drop` 事件实现卡牌拖拽。

**原因：** 无需引入 SortableJS 等库，保持零依赖。对于固定槽位（非排序列表）的拖拽场景，原生 API 足够。

**替代方案：** SortableJS → 需要外部脚本，单文件目标受损，放弃。

---

### 决策 3：点击卡牌槽位弹出角色选择器（补充拖拽交互）

**选择：** 除拖拽外，点击空槽位时弹出角色选择弹窗（模态框），提供搜索/筛选功能。

**原因：** 移动端/触屏设备拖拽体验差，点选是必要补充。同时，角色数量多时点选比拖拽更高效。

---

### 决策 4：持久化双轨方案（角色数据 → IndexedDB，队伍配置 → localStorage）

**选择：**
- **角色图片和数据**：IndexedDB（`wuwa-deck` 库，`characters` 表），一次写入，只读
- **队伍配置和备注**：`localStorage['wuwa-deck-state']`，每次变更时序列化写入

**原因：** 队伍配置是小型 JSON（< 10 KB），localStorage 同步 API 更简单。角色图片体积大，必须用 IndexedDB。两者分离，互不干扰。

---

### 决策 5：纯 CSS 实现样式，无 UI 框架

**选择：** 使用 CSS Grid/Flexbox 布局，配合 CSS 变量定义主题色（鸣潮风格深色调）。

**原因：** 引入 Tailwind CDN 或 Bootstrap 会增加网络依赖，破坏离线目标。手写 CSS 对本工具规模完全可控。

## Risks / Trade-offs

- **Wiki 角色列表 API 结构未知** → 实现前需用 DevTools Network 面板探查实际 API 端点和响应格式；若结构变更需重新适配解析逻辑。
- **Wiki 图片 CDN CORS 受限** → 初始化时若图片 fetch 被拒，回退为仅存储图片 URL（离线时显示文字头像）并提示用户。
- **IndexedDB 被浏览器清除（隐私模式/手动清除）** → 提供"重新抓取"按钮，允许用户随时重新初始化角色库；队伍配置和 IndexedDB 独立，重抓不影响已保存的编队。
- **新版本角色未纳入** → 提供"刷新角色库"按钮，重新执行初始化流程覆盖旧数据。
- **原生拖拽在 Firefox 的视觉差异** → 测试并用 CSS 统一 drag ghost 样式；必要时禁用 ghost 改用自定义预览。
