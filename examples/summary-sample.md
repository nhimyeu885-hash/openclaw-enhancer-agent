# 精简结果汇报样例

```yaml
run_mode: optimize
optimization_actions:
  - "merge_duplicate_findings"
  - "summarize_long_results"
  - "remove_repeated_boilerplate"
fallback_used: false
token_saving_estimate: "22%"
ux_risk: low
```

## 任务目标
检查本周 token 消耗异常的主要原因。

## 路由与增强策略
保留原始统计口径，压缩重复背景，只汇总异常峰值、归因和动作建议。

## 关键信息/结论
- 周三和周五出现两次高峰，主要由重复检索和长摘要造成。
- 结果完整性未受影响，原始明细仍保留在下游文件中。

## 行动项
- 对重复检索启用更严格的语义去重。
- 将长摘要任务改为“先提纲后展开”的模式。

## 风险与状态
- 当前风险：低
- 建议状态：可继续优化，不需要回滚
