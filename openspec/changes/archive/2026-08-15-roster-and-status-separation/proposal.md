## Why

主卡牌库中同时显示"未获得"角色造成视觉噪音，用户无法快速判断哪些角色可以被编入队伍。"配队次数用完"和"未获得"是性质不同的两种状态，但当前缺乏视觉区分。

## What Changes

- `renderRoster()` 过滤掉 `isUnavailable` 的角色，主卡牌库只展示已获得的角色
- 主卡牌库的角色计数改为展示"可用角色数 / 已获得角色数"
- `.char-card.used`（配队次数用完）保留当前半透明灰度样式，代表"已被队伍占用"
- 未获得区域的角色卡改为更重的灰度 + 降低饱和度样式，并增加锁定视觉提示，代表"尚未解锁"

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
- `character-roster`: 主库过滤逻辑变更——未获得的角色不再出现在主库，计数随之更新
- `unavailable-character-roster`: 未获得区域的卡牌视觉样式明确区别于"已用完"状态

## Impact

- `generate.py`: 修改 `renderRoster()` 的过滤条件；修改计数逻辑；更新 CSS 中 `.char-card.used` 与未获得卡牌的样式
