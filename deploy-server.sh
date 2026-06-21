#!/bin/bash
# 微信提醒服务 - 云服务器一键部署脚本
# 适用于 Ubuntu/Debian 系统

set -e

echo "========================================"
echo "  微信提醒服务 - 云服务器部署"
echo "========================================"
echo

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then
    echo "请使用 root 用户运行: sudo bash deploy-server.sh"
    exit 1
fi

# 安装目录
INSTALL_DIR="/opt/wechat-reminder"
SERVICE_NAME="wechat-reminder"

echo "[1/7] 安装系统依赖..."
apt update -qq
apt install -y -qq python3 python3-pip git cron

echo "[2/7] 克隆或更新代码..."
if [ -d "$INSTALL_DIR" ]; then
    cd $INSTALL_DIR
    git pull
else
    git clone https://github.com/talang-tech/wechat-reminder.git $INSTALL_DIR
    cd $INSTALL_DIR
fi

echo "[3/7] 安装 Python 依赖..."
pip3 install requests PyYAML -q

echo "[4/7] 创建配置文件..."
if [ ! -f "$INSTALL_DIR/reminders.yaml" ]; then
    cp $INSTALL_DIR/assets/reminders.example.yaml $INSTALL_DIR/reminders.yaml
    echo "✓ 已创建 reminders.yaml，请编辑配置提醒"
fi

echo
echo "========================================"
echo "  配置推送服务"
echo "========================================"
echo

read -p "请输入企业微信 CorpID (留空跳过): " WECOM_CORPID
read -p "请输入企业微信 CorpSecret (留空跳过): " WECOM_CORPSECRET
read -p "请输入企业微信 AgentId (留空跳过): " WECOM_AGENTID
read -p "请输入企业微信接收人 UserId (留空跳过): " WECOM_TOUSER

# 创建环境变量文件
cat > $INSTALL_DIR/.env << EOF
# 企业微信配置
WECOM_CORPID=$WECOM_CORPID
WECOM_CORPSECRET=$WECOM_CORPSECRET
WECOM_AGENTID=$WECOM_AGENTID
WECOM_TOUSER=$WECOM_TOUSER
EOF

echo
echo "✓ 配置文件已创建: $INSTALL_DIR/.env"

echo "[5/7] 设置定时任务..."
# 先删除旧的 cron 任务
crontab -l 2>/dev/null | grep -v "wechat-reminder" | crontab - 2>/dev/null || true
# 添加新的 cron 任务（每分钟运行一次）
(crontab -l 2>/dev/null; echo "* * * * * cd $INSTALL_DIR/scripts && /usr/bin/python3 check_reminders.py >> $INSTALL_DIR/cron.log 2>&1") | crontab -
echo "✓ 定时任务已设置（每分钟检查一次）"

echo "[6/7] 设置时区为 Asia/Shanghai..."
timedatectl set-timezone Asia/Shanghai 2>/dev/null || echo "时区设置失败，请手动设置"

echo "[7/7] 获取服务器IP..."
SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || echo "无法获取")
echo "✓ 服务器IP: $SERVER_IP"

echo
echo "========================================"
echo "  部署完成！"
echo "========================================"
echo
echo "📋 下一步操作："
echo
echo "1. 将服务器 IP 添加到企业微信可信IP:"
echo "   - 登录企业微信管理后台"
echo "   - 应用管理 → 你的应用 → 企业可信IP"
echo "   - 添加IP: $SERVER_IP"
echo
echo "2. 编辑提醒配置:"
echo "   nano $INSTALL_DIR/reminders.yaml"
echo
echo "3. 测试推送:"
echo "   cd $INSTALL_DIR/scripts && python3 test_action.py"
echo
echo "4. 查看日志:"
echo "   tail -f $INSTALL_DIR/cron.log"
echo
echo "📂 安装目录: $INSTALL_DIR"
echo "📝 配置文件: $INSTALL_DIR/.env"
echo "⏰ 定时任务: crontab -l"
echo
