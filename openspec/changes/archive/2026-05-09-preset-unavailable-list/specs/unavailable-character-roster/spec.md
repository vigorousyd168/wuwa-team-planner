# Spec: Unavailable Character Roster (Delta)

## MODIFIED Requirements

### Requirement: 展示未获得角色库
系统 SHALL 在左侧侧栏、主角色卡牌库下方展示"未获得"库区域，用户可在此看到所有被标记为未获得的角色。首次打开时（无 localStorage 数据），使用内置预设列表初始化"未获得"库。

#### Scenario: 初始加载时未获得库显示预设角色
- **WHEN** 用户首次打开工具（无 localStorage 数据）
- **THEN** "未获得"库展示预设的 15 个角色，标签显示"未获得 15 / 53"

#### Scenario: 拖拽角色到未获得库后更新计数
- **WHEN** 用户将角色卡牌从主角色库拖入"未获得"库
- **THEN** 该角色出现在"未获得"库中，计数标签更新

#### Scenario: 已保存状态优先于预设列表
- **WHEN** 用户已有保存的 localStorage 状态（包含 unavailableIds 字段）
- **THEN** 加载已保存的 unavailableIds，不应用预设列表
