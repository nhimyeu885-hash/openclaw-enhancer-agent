# OpenClaw Enhancer Agent V1

`openclaw-enhancer` 是现有虾的后台增强层，不是新的使用入口。

它的目标很克制：在不改变原来使用方式、不削弱原有能力的前提下，让现有虾更省 token、更少重复、更容易阅读，也更容易后续维护。

## 它能做什么

### 1. 发任务前做轻量优化
- 判断任务价值等级，决定是否值得压缩
- 识别重复查询、重复背景和重复检索
- 做 token 预算控制
- 压缩废话和非关键上下文，但保留目标、约束、交付格式

### 2. 结果回来后做结构化整理
- 合并重复结论
- 删除重复样板
- 对长结果做摘要和长度控制
- 将汇报收敛为“结论 / 行动项 / 风险 / 状态”

### 3. 管理安全热修
- 只允许 `L0` 级别的 prompt / config / cron 热修
- 所有自动热修都要经过验收清单
- 所有系统级改动都要写入 `result/system/changelog.md`

### 4. 必要时主动回退
- `passthrough`：不压缩，只观察
- `optimize`：正常启用增强
- `fallback`：检测到风险或完整性问题时，直接退回原流程

### 5. 支持后续维护
- 提供一个内部 skill `openclaw-agent-maintainer`
- 用它校验工作区、判断变更级别、生成 changelog 模板
- 这个 skill 不是给 Andy 日常直接操作的入口

## 它明确不做什么
- 不新增默认入口
- 不要求 Andy 学新命令
- 不改掉现有 `#homebase` 的角色
- 不重做 `DNA -> coach -> result/` 基础链路
- 不自动执行 `L1/L2` 级改动
- 不为了省 token 牺牲关键结论、关键行动项和关键状态

## 核心工作流

```mermaid
flowchart LR
    A["Andy 在原入口下指令"] --> B["#homebase"]
    B --> C["openclaw-enhancer 前置优化"]
    C --> D["原频道路由与执行链路"]
    D --> E["result/ 异步产物"]
    E --> F["openclaw-enhancer 后置整理"]
    F --> G["#homebase 结构化汇报"]
```

## 目录说明

### `control/`
系统级事实源。

- `enhancer-policy.yaml`：增强策略主配置
- `change-governance.yaml`：`L0/L1/L2`、`PASS/BLOCK/REJECT` 等治理规则
- `acceptance-checklist.yaml`：热修验收项
- `channel-routing.yaml`：保留的频道分工与路由
- `enhancer-output-schema.yaml`：增强层标准输出字段

### `prompts/agents/`
版本化 agent prompt。

- `homebase.md`：原主入口，已接入 enhancer 协同
- `openclaw-enhancer.md`：增强层主 prompt
- `openclaw-core-config.md`：系统配置与热修控制面
- `dna-caster.md`：数字人 DNA 铸造
- `coach.md`：红队审查与补丁建议

### `docs/`
设计和展示文档。

- `openclaw-enhancer-design.md`：设计稿
- `openclaw-enhancer-compare.md`：现有虾与增强层对照图
- `openclaw-agent-maintainer-skill.md`：内部维护 skill 设计稿

### `examples/`
固定展示样例。

- `task-before-after.md`：同一任务增强前后对比
- `summary-sample.md`：精简汇报样例
- `l0-hotfix-log.md`：安全热修记录样例
- `fallback-sample.md`：增强失败后自动回退样例

### `result/`
运行期产物目录。

- `result/system/changelog.md`：系统级改动日志
- `result/project/dna/`：DNA 产物
- `result/project/coach/`：红队报告与补丁

### `scripts/`
本仓库脚本。

- `validate_enhancer_setup.py`：检查当前工作区是否完整

### `skills/`
仓库内镜像的内部维护 skill，方便公开仓库直接携带完整资产。

- `skills/openclaw-agent-maintainer/`：维护 enhancer 的 skill 镜像

## 快速使用

### 1. 先看策略和 prompt
- `control/enhancer-policy.yaml`
- `prompts/agents/homebase.md`
- `prompts/agents/openclaw-enhancer.md`

### 2. 跑一遍工作区校验

```bash
python .\scripts\validate_enhancer_setup.py
```

### 3. 需要维护 enhancer 时，使用内部 skill

Skill 路径：

`C:\Users\Andyw\.codex\skills\openclaw-agent-maintainer`

仓库镜像路径：

`.\skills\openclaw-agent-maintainer`

它提供：
- `validate_workspace.py`：校验工作区
- `classify_change_scope.py`：保守判断改动是 `L0/L1/L2`
- `draft_changelog_entry.py`：生成热修日志模板

示例：

```bash
python "C:\Users\Andyw\.codex\skills\openclaw-agent-maintainer\scripts\validate_workspace.py" "D:\工作内容\工作内容\新兴项目经理\AI学习\AI学习心得\养虾专供"
python "C:\Users\Andyw\.codex\skills\openclaw-agent-maintainer\scripts\classify_change_scope.py" "control/enhancer-policy.yaml" "prompts/agents/homebase.md"
python "C:\Users\Andyw\.codex\skills\openclaw-agent-maintainer\scripts\draft_changelog_entry.py"
```

## 什么时候应该回退

出现以下任一情况时，enhancer 应优先 `passthrough` 或 `fallback`：
- 用户明确要求完整原文
- 压缩会影响关键结论
- 路由信心不足
- 增强后的结果可能让现有虾更难用

## 当前实现边界

这套仓库目前实现的是：
- 版本化 prompt
- 策略配置
- 治理与验收规则
- 展示样例
- 校验脚本
- 内部维护 skill

还没有直接接入真实的 Discord/DingTalk 运行时，也没有真实的 OpenClaw 执行器代码。换句话说，这里已经把“怎么增强、怎么治理、怎么维护”落好了，但还没有把它接成在线服务。
