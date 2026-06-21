#!/usr/bin/env python3
"""
列出所有提醒
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from reminder import ReminderManager, create_notifier_from_env


def main():
    parser = argparse.ArgumentParser(description="列出所有提醒")
    parser.add_argument("--config", default="reminders.yaml", help="配置文件路径")

    args = parser.parse_args()

    # 创建通知器（不需要真的发送）
    notifier = create_notifier_from_env()
    if not notifier:
        # 创建一个空的通知器
        class DummyNotifier:
            def send(self, title, content): return True
        notifier = DummyNotifier()

    manager = ReminderManager(args.config, notifier)
    reminders = manager.get_reminders()

    if not reminders:
        print("暂无提醒")
        return 0

    print(f"共有 {len(reminders)} 个提醒:\n")

    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    for i, reminder in enumerate(reminders, 1):
        status = "✓" if reminder.enabled else "✗"
        days_str = ", ".join([weekday_names[d-1] for d in reminder.days])
        print(f"{status} [{i}] {reminder.title}")
        print(f"    时间: {reminder.time}")
        print(f"    日期: {days_str}")
        print(f"    内容: {reminder.content[:50]}{'...' if len(reminder.content) > 50 else ''}")
        if reminder.last_sent:
            print(f"    上次发送: {reminder.last_sent}")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
