#!/usr/bin/env python3
"""
交互式创建提醒向导
"""

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from reminder import ReminderManager, create_notifier_from_env


def main():
    print("=" * 50)
    print("  微信提醒 - 交互式创建向导")
    print("=" * 50)
    print()

    # 检查是否配置了推送服务
    notifier = create_notifier_from_env()

    if not notifier:
        print("还没有配置推送服务，让我们先来配置吧！")
        print()
        print("请选择一个推送服务:")
        print()
        print("  1. Server酱 (推荐)")
        print("     - 访问 https://sct.ftqq.com 注册")
        print("     - 简单易用，免费版每天5条")
        print()
        print("  2. WxPusher")
        print("     - 访问 https://wxpusher.zjiecode.com 注册")
        print("     - 支持推送给多人")
        print()
        print("  3. PushPlus")
        print("     - 访问 https://www.pushplus.plus 注册")
        print()

        choice = input("请选择 (1-3): ").strip()

        if choice == "1":
            print()
            print("请访问 https://sct.ftqq.com 获取你的 SENDKEY")
            sct_key = input("输入 SENDKEY: ").strip()
            if sct_key:
                # 创建 .env 文件
                with open(".env", "w", encoding="utf-8") as f:
                    f.write(f"SCT_KEY={sct_key}\n")
                print()
                print("✓ 已保存配置到 .env 文件")
                print("请重新运行此脚本")
                return 0

        elif choice == "2":
            print()
            print("请访问 https://wxpusher.zjiecode.com 获取:")
            token = input("输入 APP_TOKEN: ").strip()
            uids = input("输入 UIDs (多个用逗号分隔): ").strip()
            if token and uids:
                with open(".env", "w", encoding="utf-8") as f:
                    f.write(f"WXPUSHER_APP_TOKEN={token}\n")
                    f.write(f"WXPUSHER_UIDS={uids}\n")
                print()
                print("✓ 已保存配置到 .env 文件")
                print("请重新运行此脚本")
                return 0

        elif choice == "3":
            print()
            print("请访问 https://www.pushplus.plus 获取你的 token")
            token = input("输入 token: ").strip()
            if token:
                with open(".env", "w", encoding="utf-8") as f:
                    f.write(f"PUSHPLUS_TOKEN={token}\n")
                print()
                print("✓ 已保存配置到 .env 文件")
                print("请重新运行此脚本")
                return 0

        print()
        print("未完成配置，请稍后再试")
        return 1

    # 加载环境变量（如果有 .env 文件）
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=", 1)
                    import os
                    os.environ[key] = value

    # 重新创建通知器
    notifier = create_notifier_from_env()

    print()
    print("好的！现在让我们创建一个提醒")
    print()

    title = input("提醒标题 (例如: 喝水提醒): ").strip()
    if not title:
        title = "提醒"

    content = input("提醒内容: ").strip()
    if not content:
        content = "该做这件事了！"

    time_str = input("提醒时间 (HH:MM, 例如 09:00): ").strip()
    if not time_str:
        time_str = "09:00"

    print()
    print("哪些天提醒?")
    print("  1=周一, 2=周二, ..., 7=周日")
    print("  例如: 1,2,3,4,5 (工作日)")
    print("  例如: 1,3,5 (周一、三、五)")
    days_input = input("输入 (默认每天): ").strip()

    if not days_input:
        days = [1, 2, 3, 4, 5, 6, 7]
    else:
        days = [int(d.strip()) for d in days_input.split(",")]

    print()
    print("=" * 50)
    print("  提醒预览")
    print("=" * 50)
    print(f"标题: {title}")
    print(f"内容: {content}")
    print(f"时间: {time_str}")
    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    print(f"日期: {', '.join([weekday_names[d-1] for d in days])}")
    print("=" * 50)
    print()

    confirm = input("确认创建? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("已取消")
        return 0

    # 创建管理器
    manager = ReminderManager("reminders.yaml", notifier)

    # 添加提醒
    reminder = manager.add_reminder(
        title=title,
        content=content,
        time=time_str,
        days=days
    )

    print()
    print("✓ 提醒创建成功!")
    print()

    # 询问是否测试发送
    test = input("要测试发送一次吗? (yes/no): ").strip().lower()
    if test == "yes":
        print("发送测试消息...")
        if notifier.send(f"[测试] {title}", content):
            print("✓ 发送成功！请查看微信")
        else:
            print("✗ 发送失败，请检查配置")

    print()
    print("接下来，设置定时运行:")
    print()

    if sys.platform == "win32":
        print("Windows: 运行 python scripts\\install_windows_task.py")
    else:
        print("macOS/Linux: 运行 python scripts/install_cron.py")

    print()
    print("或者手动每分钟运行: python scripts/check_reminders.py")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
