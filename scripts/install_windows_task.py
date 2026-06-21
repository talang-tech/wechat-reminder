#!/usr/bin/env python3
"""
Windows 任务计划程序安装脚本
"""

import sys
import subprocess
from pathlib import Path


def main():
    if sys.platform != "win32":
        print("此脚本仅适用于 Windows")
        return 1

    print("=" * 50)
    print("  安装 Windows 定时任务")
    print("=" * 50)
    print()

    # 获取脚本路径
    script_dir = Path(__file__).parent.parent.absolute()
    check_script = script_dir / "scripts" / "check_reminders.py"
    python_exe = sys.executable

    # 任务名称
    task_name = "WeChatReminder"

    print(f"技能目录: {script_dir}")
    print(f"Python: {python_exe}")
    print()

    # 检查是否已存在
    try:
        result = subprocess.run(
            ["schtasks", "/query", "/tn", task_name],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("任务已存在，将先删除...")
            subprocess.run(
                ["schtasks", "/delete", "/tn", task_name, "/f"],
                capture_output=True
            )
    except Exception:
        pass

    # 创建任务 - 每分钟运行一次
    cmd = [
        "schtasks", "/create",
        "/tn", task_name,
        "/tr", f'"{python_exe}" "{check_script}" --quiet',
        "/sc", "minute",
        "/f"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ 任务创建成功!")
            print()
            print("任务信息:")
            print(f"  名称: {task_name}")
            print(f"  频率: 每分钟")
            print()
            print("你可以在「任务计划程序」中查看和修改此任务")
            return 0
        else:
            print("✗ 任务创建失败")
            print(result.stderr)
            return 1
    except Exception as e:
        print(f"错误: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
