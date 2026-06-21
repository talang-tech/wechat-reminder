#!/usr/bin/env python3
"""
后台守护进程
"""

import argparse
import sys
import time
import subprocess
import os
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from reminder import ReminderManager, create_notifier_from_env


def get_pid_file():
    """获取PID文件路径"""
    return Path(__file__).parent.parent / ".daemon.pid"


def is_running():
    """检查是否已在运行"""
    pid_file = get_pid_file()
    if not pid_file.exists():
        return False

    try:
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())

        # 检查进程是否存在
        if sys.platform == "win32":
            try:
                os.kill(pid, 0)
                return True
            except OSError:
                return False
        else:
            try:
                os.kill(pid, 0)
                return True
            except OSError:
                return False
    except Exception:
        return False


def start_daemon():
    """启动守护进程"""
    if is_running():
        print("守护进程已在运行")
        return 1

    print("启动守护进程...")

    if sys.platform == "win32":
        # Windows: 使用 pythonw
        script = Path(__file__).parent / "daemon.py"
        pythonw = Path(sys.executable).parent / "pythonw.exe"
        if not pythonw.exists():
            pythonw = sys.executable

        subprocess.Popen(
            [str(pythonw), str(script), "run"],
            cwd=Path(__file__).parent.parent,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.DETACHED_PROCESS if hasattr(subprocess, 'DETACHED_PROCESS') else 0
        )
    else:
        # Unix: fork
        pid = os.fork()
        if pid > 0:
            # 父进程
            with open(get_pid_file(), 'w') as f:
                f.write(str(pid))
            print("✓ 守护进程已启动")
            return 0

        # 子进程
        os.setsid()
        pid = os.fork()
        if pid > 0:
            sys.exit(0)

        # 重定向标准输入输出
        devnull = open(os.devnull, 'r+')
        os.dup2(devnull.fileno(), sys.stdin.fileno())
        os.dup2(devnull.fileno(), sys.stdout.fileno())
        os.dup2(devnull.fileno(), sys.stderr.fileno())

        # 写入PID
        with open(get_pid_file(), 'w') as f:
            f.write(str(os.getpid()))

        run_loop()


def stop_daemon():
    """停止守护进程"""
    pid_file = get_pid_file()
    if not pid_file.exists():
        print("守护进程未在运行")
        return 0

    try:
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())

        os.kill(pid, 15)  # SIGTERM
        pid_file.unlink()
        print("✓ 守护进程已停止")
        return 0
    except Exception as e:
        print(f"停止失败: {e}")
        return 1


def run_loop():
    """运行主循环"""
    print("守护进程已启动，按 Ctrl+C 停止")

    # 确保有配置文件
    config_path = Path(__file__).parent.parent / "reminders.yaml"

    # 加载环境变量
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value

    notifier = create_notifier_from_env()
    if not notifier:
        print("错误: 未配置推送服务")
        return

    manager = ReminderManager(str(config_path), notifier)

    last_minute = -1

    try:
        while True:
            now = time.localtime()

            # 每分钟检查一次
            if now.tm_min != last_minute:
                last_minute = now.tm_min
                try:
                    manager.check_and_send()
                except Exception as e:
                    print(f"检查提醒时出错: {e}")

            # 每秒检查一次
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在停止...")
    finally:
        pid_file = get_pid_file()
        if pid_file.exists():
            try:
                pid_file.unlink()
            except Exception:
                pass


def main():
    parser = argparse.ArgumentParser(description="后台守护进程")
    parser.add_argument("command", choices=["start", "stop", "status", "run"],
                       help="命令: start(启动), stop(停止), status(状态), run(前台运行)")

    args = parser.parse_args()

    if args.command == "start":
        return start_daemon()
    elif args.command == "stop":
        return stop_daemon()
    elif args.command == "status":
        if is_running():
            print("守护进程正在运行")
            return 0
        else:
            print("守护进程未在运行")
            return 1
    elif args.command == "run":
        # 前台运行（用于调试）
        # 写入PID
        with open(get_pid_file(), 'w') as f:
            f.write(str(os.getpid()))
        try:
            run_loop()
        finally:
            pid_file = get_pid_file()
            if pid_file.exists():
                try:
                    pid_file.unlink()
                except Exception:
                    pass
        return 0


if __name__ == "__main__":
    sys.exit(main())
