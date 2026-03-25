# 增强失败后自动切回原流程样例

## 场景
用户要求：`把 coach 最近一次完整红队日志原样给我，不要摘要。`

## enhancer 判定
```yaml
run_mode: fallback
optimization_actions:
  - "none"
fallback_used: true
token_saving_estimate: "0%"
ux_risk: high
```

## 原因
- 用户明确要求完整原文
- 摘要会损失对抗日志中的关键细节
- 为保持原体验和完整性，必须直接回退到原始流程

## 系统动作
- `#homebase` 直接读取原始结果文件
- 不做压缩、不做重写、不做归并
- 回复中注明：本次因完整性要求已禁用增强摘要
