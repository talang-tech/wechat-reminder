#!/usr/bin/env python3
"""
Linux/macOS crontab 安装脚本
"""

import sys
import subprocess
from pathlib import Path


def main():
    if sys.platform == "win32":
        print("此脚本不适用于 Windows")
        return 1

    print("=" * 50)
    print("  安装 crontab 定时任务")
    print("=" * 50)
    print()

    # 获取脚本路径
    script_dir = Path(__file__).parent.parent.absolute()
    check_script = script_dir / "scripts" / "check_reminders.py"
    python_exe = sys.executable

    print(f"技能目录: {script_dir}")
    print(f"Python: {python_exe}")
    print()

    # 获取当前 crontab
    try:
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True
        )
        current_crontab = result.stdout if result.returncode == 0 else ""
    except Exception:
        current_crontab = ""

    # 准备新的 cron 行
    cron_line = f"* * * * * cd {script_dir} && {python_exe} {check_script} --quiet"

    # 检查是否已存在
    if cron_line in current_crontab:
        print("任务已存在于 crontab 中")
        return 0

    # 添加到 crontab
    new_crontab = current_crontab
    if new_crontab and not new_crontab.endswith("\n"):
        new_crontab += "\n"
    new_crontab += f"{cron_line}\n"

    try:
        # 写入新的 crontab
        p = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
        p.communicate(new_crontab)

        if p.returncode == 0:
            print("✓ crontab 安装成功!")
            print()
            print("任务信息:")
            print("  频率: 每分钟")
            print()
            print("使用 `crontab -l` 查看当前任务")
            print("使用 `crontab -e` 编辑任务")
            return 0
        else:
            print("✗ crontab 安装失败")
            return 1
    except Exception as e:
        print(f"错误: {e}")
        print()
        print("你也可以手动添加这一行到 crontab:")
        print(f"  {cron_line}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
