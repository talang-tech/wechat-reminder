# wechat-reminder-skill — 微信定时提醒技能

一个简单易用的微信定时提醒工具，支持日常任务提醒、喝水提醒、吃药提醒等。

## 功能特点

- ✅ 支持多种微信推送服务（企业微信、Server酱、WxPusher、PushPlus）
- ✅ 灵活的提醒配置（时间、日期、内容）
- ✅ 自动定时检查发送
- ✅ Windows/macOS/Linux 全平台支持
- ✅ 支持 GitHub Actions 云端部署
- ✅ 支持云服务器部署
- ✅ 简单的命令行工具和交互式向导

## 推送服务对比

| 服务 | 推荐度 | 特点 | 部署方式 |
|------|--------|------|---------|
| **企业微信** | ⭐⭐⭐⭐⭐ | 功能强大，完全免费，支持 Markdown，可指定用户 | 云服务器（有固定IP） |
| Server酱 | ⭐⭐⭐⭐ | 简单易用，注册即用，无需服务器 | GitHub Actions、本地 |
| WxPusher | ⭐⭐⭐⭐ | 支持多人推送 | GitHub Actions、本地、服务器 |
| PushPlus | ⭐⭐⭐ | 模板丰富 | GitHub Actions、本地、服务器 |

## 三种部署方式

| 方式 | 优点 | 缺点 | 适合人群 |
|------|------|------|---------|
| ☁️ **GitHub Actions** | 免费，无需服务器，设置简单 | 企业微信需要IP白名单（不适合） | 使用Server酱/WxPusher |
| 🖥️ **云服务器** | 稳定可靠，固定IP，适合企业微信 | 需要购买服务器 | 长期使用，用企业微信 |
| 💻 **本地运行** | 快速测试 | 电脑需要一直开机 | 临时测试 |

---

## 快速开始

### 方式一：GitHub Actions（推荐用 Server酱）

快速部署，无需服务器。详见：[docs/GITHUB_DEPLOY.md](docs/GITHUB_DEPLOY.md)

### 方式二：云服务器（推荐用企业微信）

最稳定的方案，有固定IP。详见：[docs/SERVER_DEPLOY.md](docs/SERVER_DEPLOY.md)

**一键部署命令（在服务器上运行）：**
```bash
wget -O deploy-server.sh https://raw.githubusercontent.com/talang-tech/wechat-reminder/main/deploy-server.sh
chmod +x deploy-server.sh
sudo bash deploy-server.sh
```

### 方式三：本地运行（测试用）

```bash
# 1. 克隆代码
git clone https://github.com/talang-tech/wechat-reminder.git
cd wechat-reminder

# 2. 安装依赖
pip install requests PyYAML

# 3. 创建 .env 配置文件（见下方配置说明）

# 4. 创建提醒
python scripts/wizard.py

# 5. 测试推送
python scripts/test_push.py
```

---

## 配置说明

### 企业微信配置

```env
WECOM_CORPID=你的企业ID
WECOM_CORPSECRET=你的应用Secret
WECOM_AGENTID=你的应用AgentId
WECOM_TOUSER=接收人UserId
```

获取方法见：[docs/GITHUB_DEPLOY.md](docs/GITHUB_DEPLOY.md)

### Server酱配置

```env
SCT_KEY=你的SENDKEY
```

访问 https://sct.ftqq.com 获取。

---

## 提醒配置

编辑 `reminders.yaml`：

```yaml
reminders:
  - id: drink-water
    title: "喝水提醒 💧"
    content: "该喝水了！保持健康的饮水习惯。"
    time: "09:00"
    enabled: true
    days: [1, 2, 3, 4, 5, 6, 7]  # 1=周一, 7=周日
```

---

## 命令行工具

| 命令 | 功能 |
|------|------|
| `python scripts/wizard.py` | 交互式创建提醒 |
| `python scripts/create_reminder.py` | 创建提醒 |
| `python scripts/list_reminders.py` | 列出所有提醒 |
| `python scripts/delete_reminder.py` | 删除提醒 |
| `python scripts/test_push.py` | 测试推送服务 |
| `python scripts/test_action.py` | GitHub Actions 测试脚本 |
| `python scripts/check_reminders.py` | 检查并发送提醒 |

---

## 目录结构

```
wechat-reminder-skill/
├── SKILL.md
├── README.md
├── .github/workflows/
│   └── reminder.yml              # GitHub Actions 配置
├── docs/
│   ├── GITHUB_DEPLOY.md          # GitHub 部署文档
│   └── SERVER_DEPLOY.md          # 服务器部署文档
├── scripts/
│   ├── reminder.py               # 核心模块
│   ├── wizard.py                 # 交互式向导
│   ├── test_push.py              # 测试推送
│   ├── test_action.py            # Actions 测试
│   ├── check_reminders.py        # 检查并发送
│   └── ...
├── deploy-server.sh              # 服务器一键部署脚本
├── wechat-reminder.service       # Systemd 服务文件
└── assets/
    └── reminders.example.yaml    # 配置示例
```

---

## 许可证

MIT License
