## Why

随着游戏版本更新，三名新角色（洛瑟菈、露西、丽贝卡）已加入游戏，需将其收录进角色库，使用户可以在队伍规划工具中使用这些角色。

## What Changes

- 在 `wuwa-wiki/characters.json` 中新增三条角色数据记录
- 新增对应角色头像图片已存在于 `wuwa-wiki/images/` 目录（由用户提供）
- 重新运行 `generate.py` 生成包含新角色的 HTML 输出

## Capabilities

### New Capabilities
<!-- 无新能力，属于对现有角色数据的扩展 -->

### Modified Capabilities
- `character-roster`: 角色库数据集扩展——新增 3 名角色条目（洛瑟菈、露西、丽贝卡），无行为变更，仅数据层面增加

## Impact

- `wuwa-wiki/characters.json`：新增 3 个角色对象（id 54、55、56）
- `generate.py` 及生成的 HTML：无代码改动，重新执行脚本即可自动包含新角色
