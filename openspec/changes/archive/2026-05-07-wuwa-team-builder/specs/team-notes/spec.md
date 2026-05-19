## ADDED Requirements

### Requirement: 每支队伍有独立备注文本框
系统 SHALL 在每行队伍的右侧提供一个多行文本输入框（textarea），用于填写该队伍的备注信息。

#### Scenario: 文本框随队伍出现
- **WHEN** 队伍行被渲染（初始加载或新增队伍）
- **THEN** 该行右侧显示一个空的备注文本框，占位提示为"队伍备注…"

#### Scenario: 用户输入备注
- **WHEN** 用户在某支队伍的备注框中输入文字
- **THEN** 文字实时显示在文本框中

### Requirement: 备注内容自动持久化
系统 SHALL 在用户输入备注时将备注内容保存到 localStorage，与队伍配置一起持久化。

#### Scenario: 刷新页面后恢复备注
- **WHEN** 用户填写备注后刷新页面
- **THEN** 对应队伍的备注文本框恢复显示之前填写的内容

#### Scenario: 删除队伍时清除备注
- **WHEN** 用户删除某支队伍
- **THEN** 该队伍的备注数据从 localStorage 中一并移除
