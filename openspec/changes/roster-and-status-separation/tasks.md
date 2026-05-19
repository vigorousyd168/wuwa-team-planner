## 1. 主卡牌库过滤

- [x] 1.1 在 `renderRoster()` 的 `list` 过滤条件中添加 `!isUnavailable(c.id)`，将未获得角色排除在主库之外
- [x] 1.2 删除 `renderRoster()` 中 `unavailClass` 变量及其在卡牌 HTML 中的引用（已成为死代码）
- [x] 1.3 修改主库计数逻辑：改为"N 名可用 / M 名已获得"格式，其中 M = 已获得角色数，N = 已获得且未被占满的角色数

## 2. 视觉样式区分

- [x] 2.1 修改 `.char-card.used` CSS：`opacity:0.4; filter:grayscale(50%)` （半灰度，保留部分颜色）
- [x] 2.2 修改 `.char-card.unavailable` CSS：`opacity:0.5; filter:grayscale(100%) brightness(0.7)` （全灰度 + 降低亮度）

## 3. 构建与验证

- [x] 3.1 运行 `generate.py` 重新生成 `index.html`
- [x] 3.2 验证主卡牌库不再显示已标记为"未获得"的角色
- [x] 3.3 验证"未获得"库的角色卡牌样式（全灰度暗色）与主库已用完卡牌样式（半灰度）视觉上明显不同
- [x] 3.4 验证计数标签格式正确："N 名可用 / M 名已获得"
