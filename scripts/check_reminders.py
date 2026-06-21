#!/usr/bin/env python3
"""
检查并发送到期提醒
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from reminder import ReminderManager, create_notifier_from_env


def main():
    parser = argparse.ArgumentParser(description="检查并发送到期提醒")
    parser.add_argument("--config", default="reminders.yaml", help="配置文件路径")
    parser.add_argument("--quiet", "-q", action="store_true", help="静默模式，不输出")
    parser.add_argument("--force", "-f", action="store_true", help="强制发送所有提醒")

    args = parser.parse_args()

    notifier = create_notifier_from_env()
    if not notifier:
        if not args.quiet:
            print("错误: 请先配置推送服务")
        return 1

    manager = ReminderManager(args.config, notifier)

    if args.force:
        # 强制发送所有启用的提醒
        if not args.quiet:
            print("强制发送所有提醒...")
        sent = []
        for reminder in manager.get_reminders():
            if reminder.enabled:
                if notifier.send(reminder.title, reminder.content):
                    sent.append(reminder)
                    if not args.quiet:
                        print(f"✓ 已发送: {reminder.title}")
    else:
        # 正常检查
        now = datetime.now()
        if not args.quiet:
            print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
            print("检查提醒...")
        sent = manager.check_and_send(now)

    if not sent and not args.quiet:
        print("没有需要发送的提醒")

    return 0


if __name__ == "__main__":
    sys.exit(main())
