# L0 Enhancer Worker MVP

## 目标
把当前仓库从“治理资产”推进到“可本地运行的最小执行器”。

这个 MVP 只处理低风险增强：
- 去重
- 结构化
- 短报
- token 预算估算

它不会直接改业务逻辑，也不会直接接管真实 Discord/OpenClaw 运行时。

## 组成

### 1. 执行器
- `scripts/l0_enhancer_worker.py`

输入一个 JSON 任务包，输出一个增强后的 JSON 结果包，并写入指标日志。

### 2. 灰度配置
- `control/gray-rollout.yaml`

默认只放开：
- `#homebase`
- `#多agent协作`

### 3. 指标闭环
- `control/metrics-policy.yaml`
- `scripts/summarize_enhancer_metrics.py`
- `scripts/record_manual_review.py`

重点追踪 3 个指标：
- 压缩前后 token 变化
- fallback 触发率
- 结论完整性人工抽检通过率

## 输入格式

最小输入示例：

```json
{
  "task_id": "demo-post-003",
  "stage": "post_result",
  "channel": "#homebase",
  "user_goal": "给我一个简洁风险总结",
  "raw_text": "结论：...\\n下一步：...\\n风险：...",
  "must_keep": ["高风险补丁"],
  "require_verbatim": false
}
```

## 输出格式

输出仍然遵守 enhancer 的稳定字段：
- `run_mode`
- `optimization_actions`
- `fallback_used`
- `token_saving_estimate`
- `ux_risk`

同时增加：
- `optimized_text`
- `structured_sections`
- `report`

## 运行方式

### 单次运行

```bash
python .\scripts\l0_enhancer_worker.py --input .\examples\runtime-post-input.json --output .\result\system\runtime\demo-post-output.json
```

### 汇总指标

```bash
python .\scripts\summarize_enhancer_metrics.py
```

### 记录人工抽检

```bash
python .\scripts\record_manual_review.py --task-id demo-post-003 --pass true --reviewer Andy
```

## 当前边界

这个 MVP 已经能证明三件事：
- 低风险增强可以独立执行
- 指标可以落盘并形成最小闭环
- 可以先灰度到 1-2 个频道验证

它仍然没有做的部分：
- 实时接入 Discord 事件流
- 真实 token 计费回读
- 自动改写下游 OpenClaw runtime
