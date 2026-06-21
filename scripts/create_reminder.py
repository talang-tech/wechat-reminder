#!/usr/bin/env python3
"""
创建提醒
"""

import argparse
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from reminder import ReminderManager, create_notifier_from_env


def main():
    parser = argparse.ArgumentParser(description="创建微信提醒")
    parser.add_argument("--title", "-t", required=True, help="提醒标题")
    parser.add_argument("--content", "-c", required=True, help="提醒内容")
    parser.add_argument("--time", required=True, help="提醒时间 (HH:MM)")
    parser.add_argument("--days", default="1,2,3,4,5,6,7",
                       help="提醒日期 (1=周一, 7=周日, 逗号分隔)")
    parser.add_argument("--config", default="reminders.yaml", help="配置文件路径")

    args = parser.parse_args()

    # 解析日期
    try:
        days = [int(d.strip()) for d in args.days.split(",")]
    except ValueError:
        print("错误: 日期格式不正确，请使用数字 1-7")
        return 1

    # 创建通知器
    notifier = create_notifier_from_env()
    if not notifier:
        print("错误: 请先配置推送服务")
        print("请设置环境变量 SCT_KEY、WXPUSHER_APP_TOKEN+WXPUSHER_UIDS 或 PUSHPLUS_TOKEN")
        return 1

    # 创建管理器
    manager = ReminderManager(args.config, notifier)

    # 添加提醒
    reminder = manager.add_reminder(
        title=args.title,
        content=args.content,
        time=args.time,
        days=days
    )

    print(f"✓ 提醒创建成功!")
    print(f"  ID: {reminder.id}")
    print(f"  标题: {reminder.title}")
    print(f"  时间: {reminder.time}")
    print(f"  日期: {reminder.days}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
