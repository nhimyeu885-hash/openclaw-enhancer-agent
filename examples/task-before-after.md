# 同一任务增强前后对比

## 用户原始请求
`帮我检查最近 7 天 coach 产物里有没有重复的修复建议，并给我一个简洁的风险总结。`

## 增强前
- `#homebase` 直接把原句完整转发给多个频道
- 下游结果可能包含重复背景、重复漏洞描述和大段样板总结
- 汇报可能刷屏，关键行动项埋在长文里

## 增强后
### 前置处理
```yaml
run_mode: optimize
optimization_actions:
  - "classify_task_value:P1"
  - "dedupe_repeated_background"
  - "compress_non_critical_instructions"
fallback_used: false
token_saving_estimate: "10%-18%"
ux_risk: low
```

### 优化后的路由指令
`检查最近 7 天 coach 产物，识别重复修复建议，按高/中/低风险归并，只保留唯一结论、阻塞项和下一步。`

### 后置整理后的汇报
- 关键结论：发现 3 类重复修复建议，其中 1 类属于高风险越狱防护缺口。
- 行动项：合并重复补丁模板；保留 1 个高风险补丁进入审批；低风险表述问题延后。
- 风险与状态：当前无需回滚，建议下一轮 coach 先验证越狱补丁。
