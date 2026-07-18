# Wang-Yeah623 Skills

可复用、可验证的 Agent 技能集合。

## Skills

### `agent-project-quality-audit`

以风险地图、证据复现、测试先行和持久化质量台账，对软件项目执行有边界、可验证的质量审计与最小修复。

主要能力：

- 建立项目地图、验收标准、风险登记与覆盖矩阵；
- 按风险选择一次有边界的审计范围；
- 区分已确认缺陷、静态假设、环境问题和误报；
- 在获得修改授权后，用失败测试约束最小修复；
- 通过分层回归验证，并把证据持续记录在 `.quality/` 中；
- 使用内置脚本检查审计制品的结构和问题台账一致性。

详见 [`agent-project-quality-audit/SKILL.md`](agent-project-quality-audit/SKILL.md)。

## 安装

将目标 Skill 文件夹复制到 Codex 的 Skills 目录：

```text
$CODEX_HOME/skills/agent-project-quality-audit/
```

安装后重新启动或刷新 Codex，使其重新发现 Skill。

## 状态

- 已通过 Skill 结构校验；
- 已在真实软件仓库快照上完成只读审计实测；
- 实测不等于对所有语言、框架和运行环境均已验证。
