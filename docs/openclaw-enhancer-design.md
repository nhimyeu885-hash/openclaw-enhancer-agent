# OpenClaw Enhancer Agent V1 设计稿

## 1. 目标
`openclaw-enhancer` 是现有虾的后台增强层，不是新的使用入口。

V1 只做三件事：
- 发任务前减少无效 token 和重复上下文
- 收结果后减少刷屏和重复结论
- 发现安全 `L0` 热修机会时给出可执行修补和回滚记录

## 2. 不变的部分
- `#homebase` 仍是 Andy 的主入口
- 原频道路由规则继续有效
- `DNA -> coach -> result/` 的基础链路不改
- 查询任务结果的语义不变

## 3. 新增的增强层
增强层在两个时点介入：

### 前置优化
- 任务价值分级
- 重复请求识别
- token 预算控制
- 指令压缩，但保留硬约束、目标和交付格式

### 后置整理
- 重复结论归并
- 冗余样板删除
- 长结果摘要
- 汇报重组为“结论 / 行动项 / 风险 / 状态”

## 4. 风险门槛
以下情况必须降级为 `passthrough` 或 `fallback`：
- 增强会改变任务意图
- 增强可能掩盖关键结论
- 路由信心不足
- 用户明确要求完整原文

## 5. 安全热修范围
只允许自动热修：
- prompt 微调
- 配置修补
- cron 修补

不得自动改动：
- 业务逻辑
- 频道结构
- 数据结构
- `DNA` / `coach` 的核心角色

## 6. 标准输出
每次运行 enhancer 都应输出固定字段：
- `run_mode`
- `optimization_actions`
- `fallback_used`
- `token_saving_estimate`
- `ux_risk`

并附带结构化说明：
- 任务目标
- 路由与增强策略
- 关键信息/结论
- 行动项
- 风险与状态

## 7. 运行文件
- 策略配置：`control/enhancer-policy.yaml`
- 治理规则：`control/change-governance.yaml`
- 验收清单：`control/acceptance-checklist.yaml`
- 输出字段：`control/enhancer-output-schema.yaml`
- 变更日志：`result/system/changelog.md`
