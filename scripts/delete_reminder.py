#!/usr/bin/env python3
"""
删除提醒
"""

import argparse
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from reminder import ReminderManager, create_notifier_from_env


def main():
    parser = argparse.ArgumentParser(description="删除提醒")
    parser.add_argument("id", nargs="?", help="提醒ID")
    parser.add_argument("--config", default="reminders.yaml", help="配置文件路径")
    parser.add_argument("--all", action="store_true", help="删除所有提醒")

    args = parser.parse_args()

    # 创建一个空的通知器
    class DummyNotifier:
        def send(self, title, content): return True

    manager = ReminderManager(args.config, DummyNotifier())

    if args.all:
        confirm = input("确定要删除所有提醒吗? (yes/no): ")
        if confirm.lower() == "yes":
            reminders = manager.get_reminders()
            for r in reminders:
                manager.delete_reminder(r.id)
            print(f"✓ 已删除 {len(reminders)} 个提醒")
        return 0

    if not args.id:
        # 列出提醒让用户选择
        reminders = manager.get_reminders()
        if not reminders:
            print("暂无提醒")
            return 0

        print("选择要删除的提醒:\n")
        for i, reminder in enumerate(reminders, 1):
            print(f"{i}. {reminder.title} ({reminder.time})")

        print()
        choice = input("输入编号 (或 'all' 删除所有): ")

        if choice.lower() == "all":
            confirm = input("确定要删除所有提醒吗? (yes/no): ")
            if confirm.lower() == "yes":
                for r in reminders:
                    manager.delete_reminder(r.id)
                print(f"✓ 已删除 {len(reminders)} 个提醒")
            return 0

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(reminders):
                reminder = reminders[idx]
                manager.delete_reminder(reminder.id)
                print(f"✓ 已删除: {reminder.title}")
            else:
                print("无效的编号")
        except ValueError:
            print("请输入有效的编号")
        return 0

    # 通过ID删除
    if manager.delete_reminder(args.id):
        print(f"✓ 已删除: {args.id}")
    else:
        print(f"未找到提醒: {args.id}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
