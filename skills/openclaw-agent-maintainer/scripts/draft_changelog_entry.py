#!/usr/bin/env python3
from datetime import datetime


def main() -> int:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"- 时间：{now}")
    print("- 变更等级：L0")
    print("- 目标：")
    print("- 变更内容：")
    print("- 原因：")
    print("- 审查结论：PASS")
    print("- 验收结果：")
    print("- 是否触发回退：否")
    print("- 备注：")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
