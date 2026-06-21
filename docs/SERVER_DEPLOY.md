# 云服务器部署指南

部署到云服务器是最稳定的方案，24 小时运行，有固定 IP 可以配置企业微信白名单。

## 📋 准备工作

### 1. 购买云服务器
推荐：
- **阿里云**、**腾讯云**、**华为云**的轻量应用服务器
- 配置：1核1G 即可，约 30-50 元/年
- 系统：**Ubuntu 22.04 LTS**

### 2. 登录服务器
使用 SSH 登录：
```bash
ssh root@你的服务器IP
```

---

## 🚀 一键部署（推荐）

### 方法一：使用部署脚本（最简单）

在服务器上运行：

```bash
# 1. 下载并运行部署脚本
wget -O deploy-server.sh https://raw.githubusercontent.com/talang-tech/wechat-reminder/main/deploy-server.sh
chmod +x deploy-server.sh
sudo bash deploy-server.sh
```

按提示输入企业微信配置即可。

---

## 🔧 手动部署

### 步骤 1：安装依赖

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip git cron

# CentOS/RHEL
sudo yum install -y python3 python3-pip git cronie
```

### 步骤 2：克隆代码

```bash
cd /opt
git clone https://github.com/talang-tech/wechat-reminder.git
cd wechat-reminder
```

### 步骤 3：安装 Python 依赖

```bash
pip3 install requests PyYAML
```

### 步骤 4：配置推送服务

```bash
# 创建环境变量配置
cat > .env << EOF
WECOM_CORPID=你的企业ID
WECOM_CORPSECRET=你的应用Secret
WECOM_AGENTID=你的应用AgentId
WECOM_TOUSER=接收人UserId
EOF
```

或者使用 Server酱：
```bash
cat > .env << EOF
SCT_KEY=你的Server酱SENDKEY
EOF
```

### 步骤 5：配置提醒

```bash
# 复制示例配置
cp assets/reminders.example.yaml reminders.yaml

# 编辑配置
nano reminders.yaml
```

### 步骤 6：测试推送

```bash
cd scripts
python3 test_action.py
```

### 步骤 7：配置定时运行（二选一）

#### 方式 A：使用 Cron（简单）

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每分钟运行一次）
* * * * * cd /opt/wechat-reminder/scripts && /usr/bin/python3 check_reminders.py >> /opt/wechat-reminder/cron.log 2>&1
```

#### 方式 B：使用 Systemd（推荐，更可靠）

```bash
# 复制服务文件
cp /opt/wechat-reminder/wechat-reminder.service /etc/systemd/system/

# 重新加载 systemd
systemctl daemon-reload

# 启动服务
systemctl start wechat-reminder

# 设置开机自启
systemctl enable wechat-reminder

# 查看状态
systemctl status wechat-reminder
```

---

## 📱 配置企业微信 IP 白名单

1. 获取服务器 IP：
```bash
curl ifconfig.me
```

2. 登录企业微信管理后台：
   - 应用管理 → 点击你的应用
   - 找到"企业可信IP"
   - 点击"配置"
   - 添加上面获取的服务器 IP
   - 保存

3. 再次测试：
```bash
cd /opt/wechat-reminder/scripts
python3 test_action.py
```

---

## 📊 管理命令

### Cron 方式

```bash
# 查看定时任务
crontab -l

# 查看日志
tail -f /opt/wechat-reminder/cron.log

# 手动测试
cd /opt/wechat-reminder/scripts
python3 check_reminders.py
```

### Systemd 方式

```bash
# 查看状态
systemctl status wechat-reminder

# 查看日志
journalctl -u wechat-reminder -f

# 重启服务
systemctl restart wechat-reminder

# 停止服务
systemctl stop wechat-reminder
```

---

## 🔄 更新代码

```bash
cd /opt/wechat-reminder
git pull

# 如果使用 systemd，重启服务
systemctl restart wechat-reminder
```

---

## ✏️ 修改提醒

编辑配置文件：
```bash
nano /opt/wechat-reminder/reminders.yaml
```

不需要重启服务（cron 方式会自动加载，systemd 方式会自动检测文件变化）。

---

## ❓ 故障排查

### 查看日志
```bash
# Cron 方式
tail -50 /opt/wechat-reminder/cron.log

# Systemd 方式
journalctl -u wechat-reminder -n 50
```

### 手动测试
```bash
cd /opt/wechat-reminder/scripts
python3 test_action.py
```

### 检查时区
```bash
date
# 应该显示中国时间 (CST)
```

如果时区不对：
```bash
sudo timedatectl set-timezone Asia/Shanghai
```

---

## 🎉 完成！

设置完成后，你的云服务器会每天准时发送微信提醒！
