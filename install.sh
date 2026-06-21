#!/usr/bin/env bash
# 微信提醒技能安装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "  微信提醒技能 - 安装脚本"
echo "=========================================="
echo

# 检测平台
case "$(uname -s)" in
    Darwin*)
        PLATFORM="macOS"
        ;;
    Linux*)
        PLATFORM="Linux"
        ;;
    MINGW*|MSYS*|CYGWIN*)
        PLATFORM="Windows"
        ;;
    *)
        PLATFORM="Unknown"
        ;;
esac

echo "检测到平台: $PLATFORM"
echo

# 检查 Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "错误: 未找到 Python，请先安装 Python 3"
    exit 1
fi

PYTHON_CMD="python"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
fi

echo "使用 Python: $($PYTHON_CMD --version)"
echo

# 检查依赖
echo "检查依赖..."
$PYTHON_CMD -c "import requests" 2>/dev/null || {
    echo "安装 requests 库..."
    $PYTHON_CMD -m pip install requests
}
echo

# 询问是否现在配置
read -p "要现在配置推送服务并创建提醒吗? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd "$SCRIPT_DIR"
    $PYTHON_CMD scripts/wizard.py
else
    echo
    echo "好的！稍后你可以手动配置："
    echo "  1. 创建 .env 文件配置推送服务"
    echo "  2. 运行 python scripts/wizard.py 创建提醒"
    echo "  3. 设置定时任务"
fi

echo
echo "=========================================="
echo "  安装完成！"
echo "=========================================="
echo
echo "技能已安装到: $SCRIPT_DIR"
echo
echo "快速开始："
echo "  cd $SCRIPT_DIR"
echo "  python scripts/wizard.py"
echo
echo "更多命令："
echo "  python scripts/list_reminders.py    # 列出提醒"
echo "  python scripts/test_push.py         # 测试推送"
echo "  python scripts/check_reminders.py   # 检查并发送"
echo
