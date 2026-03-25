# 现有虾与 Enhancer 对照图

```mermaid
flowchart LR
    A["Andy 在原入口下指令"] --> B["#homebase"]
    B --> C["openclaw-enhancer 前置优化"]
    C --> D["原频道路由与执行链路"]
    D --> E["result/ 异步产物"]
    E --> F["openclaw-enhancer 后置整理"]
    F --> G["#homebase 结构化汇报"]
```

## 保留不变
- 主入口仍然是 `#homebase`
- 原频道分工仍然存在
- `DNA -> coach -> result/` 原链路继续工作
- 用户日常说法和提问方式不变

## 新增增强
- 任务价值分级
- 重复查询去重
- token 预算控制
- 输出长度控制
- 结果归并整理
- 安全 `L0` 热修建议与日志

## 明确不碰
- 不新增默认入口
- 不要求用户手动切换模式
- 不自动做 `L1/L2` 变更
- 不改变 `DNA` 和 `coach` 的核心职责
- 不用“为了省 token”牺牲结果完整性
