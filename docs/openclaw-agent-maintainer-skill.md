# OpenClaw Agent Maintainer Skill 设计稿

## 目标
`openclaw-agent-maintainer` 不是给 Andy 日常直接使用的入口，而是给 Codex 在后续维护 enhancer 时调用的内部 skill。

它负责三件事：
- 审查 enhancer 工作区是否漂移
- 判断拟议改动是不是安全 `L0`
- 在安全前提下帮助生成热修记录，而不是随手改一通

## 为什么单独做成 skill
- 把维护 enhancer 的流程沉淀下来，避免每次靠临时 prompt 回忆规则
- 让“不要把虾改得更难用”成为硬约束，而不是口头提醒
- 让校验、分级、日志模板这些重复动作标准化

## 能力边界
- 可以校验工作区结构和关键配置项
- 可以基于文件路径给出 `L0/L1/L2` 的保守分类建议
- 可以生成 changelog 记录模板
- 不应绕过人工审批去做 `L1/L2` 变更

## 关键资源
- Skill 主体：`C:/Users/Andyw/.codex/skills/openclaw-agent-maintainer/SKILL.md`
- 工作区校验脚本：`scripts/validate_workspace.py`
- 变更级别分类脚本：`scripts/classify_change_scope.py`
- 日志模板脚本：`scripts/draft_changelog_entry.py`

## 触发示例
- `Use $openclaw-agent-maintainer to audit this enhancer workspace for drift.`
- `Use $openclaw-agent-maintainer to classify whether these prompt changes are safe L0 hotfixes.`
- `Use $openclaw-agent-maintainer to prepare a changelog entry for a config hotfix.`
