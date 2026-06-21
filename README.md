# wechat-reminder-skill — 微信定时提醒技能

一个简单易用的微信定时提醒工具，支持日常任务提醒、喝水提醒、吃药提醒等。

## 功能特点

- ✅ 支持多种微信推送服务（企业微信、Server酱、WxPusher、PushPlus）
- ✅ 灵活的提醒配置（时间、日期、内容）
- ✅ 自动定时检查发送
- ✅ Windows/macOS/Linux 全平台支持
- ✅ 简单的命令行工具和交互式向导
- ☁️ **支持 GitHub Actions 云端部署（免费！）**

## 推送服务对比

| 服务 | 推荐度 | 特点 | 免费额度 |
|------|--------|------|---------|
| **企业微信** | ⭐⭐⭐⭐⭐ | 功能强大，完全免费，支持 Markdown，可指定用户 | 无限 |
| Server酱 | ⭐⭐⭐⭐ | 简单易用，注册即用 | 每天 5 条 |
| WxPusher | ⭐⭐⭐⭐ | 支持多人推送 | 有免费额度 |
| PushPlus | ⭐⭐⭐ | 模板丰富 | 免费可用 |

## 部署方式选择

### 🖥️ 方式一：本地运行（需要电脑开机）
适合临时使用或测试。

### ☁️ 方式二：GitHub Actions（推荐！无需开机）
使用 GitHub Actions 免费云端运行，24/7 全天候服务。

---

## 快速开始（本地运行）

### 1. 配置推送服务

选择一个推送服务并配置：

**企业微信（推荐）**：
1. 访问 https://work.weixin.qq.com/ 注册企业微信
2. 进入应用管理创建应用，获取：
   - `AgentId`
   - `Secret`
3. 进入"我的企业"获取 `企业ID`
4. 进入"通讯录"获取用户 `UserId`
5. 创建 `.env` 文件：
   ```
   WECOM_CORPID=你的企业ID
   WECOM_CORPSECRET=你的应用Secret
   WECOM_AGENTID=你的应用AgentId
   WECOM_TOUSER=接收人UserId
   ```

**Server酱**：
1. 访问 https://sct.ftqq.com 注册
2. 获取你的 SENDKEY
3. 创建 `.env` 文件：
   ```
   SCT_KEY=你的SENDKEY
   ```

**WxPusher**：
1. 访问 https://wxpusher.zjiecode.com 注册
2. 创建应用获取 APP_TOKEN
3. 关注公众号获取你的 UID
4. 创建 `.env` 文件：
   ```
   WXPUSHER_APP_TOKEN=你的APP_TOKEN
   WXPUSHER_UIDS=你的UID
   ```

**PushPlus**：
1. 访问 https://www.pushplus.plus 注册
2. 获取你的 token
3. 创建 `.env` 文件：
   ```
   PUSHPLUS_TOKEN=你的TOKEN
   ```

### 2. 创建提醒

使用交互式向导：

```bash
python scripts/wizard.py
```

或者手动创建 `reminders.yaml`：

```yaml
reminders:
  - id: drink-water
    title: "喝水提醒 💧"
    content: "该喝水了！保持健康的饮水习惯。"
    time: "09:00"
    enabled: true
    days: [1, 2, 3, 4, 5, 6, 7]
```

### 3. 测试推送

```bash
python scripts/test_push.py
```

### 4. 设置定时运行

**Windows**：
```bash
python scripts/install_windows_task.py
```

**macOS/Linux**：
```bash
python scripts/install_cron.py
```

或者使用后台守护进程：
```bash
python scripts/daemon.py start
```

---

## 快速开始（GitHub Actions 云端部署）⭐推荐！

### 1. 准备 GitHub 仓库

```bash
cd ~/.claude/skills/wechat-reminder-skill

# Windows:
deploy-github.bat

# macOS/Linux:
chmod +x deploy-github.sh
./deploy-github.sh
```

或者手动操作：
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M main
git push -u origin main
```

### 2. 配置 GitHub Secrets

在 GitHub 仓库中：
1. **Settings** → **Secrets and variables** → **Actions**
2. 添加 Secret（根据你选择的服务）：

**企业微信（推荐）**：
- Name: `WECOM_CORPID`
- Value: 你的企业 ID
- Name: `WECOM_CORPSECRET`
- Value: 你的应用 Secret
- Name: `WECOM_AGENTID`
- Value: 你的应用 AgentId
- Name: `WECOM_TOUSER`
- Value: 接收人 UserId

**Server酱**：
- Name: `SCT_KEY`
- Value: 你的 Server酱 SENDKEY

### 3. 启用并测试

1. 点击 **Actions** → "微信定时提醒" → **Enable workflow**
2. 点击 **Run workflow** 手动测试一次

详细文档：[docs/GITHUB_DEPLOY.md](docs/GITHUB_DEPLOY.md)

---

## 命令行工具

| 命令 | 功能 |
|------|------|
| `python scripts/wizard.py` | 交互式创建提醒 |
| `python scripts/create_reminder.py` | 创建提醒（命令行参数） |
| `python scripts/list_reminders.py` | 列出所有提醒 |
| `python scripts/delete_reminder.py` | 删除提醒 |
| `python scripts/test_push.py` | 测试推送服务 |
| `python scripts/check_reminders.py` | 检查并发送提醒 |
| `python scripts/daemon.py start` | 启动后台守护进程 |
| `python scripts/daemon.py stop` | 停止后台守护进程 |

### 创建提醒示例

```bash
# 创建喝水提醒
python scripts/create_reminder.py \
  --title "喝水提醒 💧" \
  --content "该喝水了！" \
  --time 09:00 \
  --days 1,2,3,4,5,6,7

# 创建工作日吃药提醒
python scripts/create_reminder.py \
  --title "吃药提醒 💊" \
  --content "记得吃药" \
  --time 08:30 \
  --days 1,2,3,4,5
```

## 提醒配置说明

```yaml
reminders:
  - id: drink-water           # 唯一标识
    title: "喝水提醒 💧"      # 提醒标题
    content: "该喝水了！"     # 提醒内容
    time: "09:00"            # 时间 (HH:MM)
    enabled: true            # 是否启用
    days: [1, 2, 3, 4, 5]   # 1=周一, 7=周日
    last_sent: "2026-06-21"  # 最后发送日期（自动维护）
```

## 目录结构

```
wechat-reminder-skill/
├── SKILL.md                    # 技能说明
├── AGENTS.md                   # 跨平台兼容说明
├── README.md                   # 本文件
├── .env                        # 环境变量（自行创建）
├── reminders.yaml              # 提醒配置（自行创建）
├── deploy-github.bat           # Windows 快速部署脚本
├── deploy-github.sh            # Unix 快速部署脚本
├── .github/
│   └── workflows/
│       └── reminder.yml        # GitHub Actions 配置
├── docs/
│   └── GITHUB_DEPLOY.md        # GitHub 部署详细文档
├── scripts/
│   ├── reminder.py             # 核心模块
│   ├── wizard.py               # 交互式向导
│   ├── create_reminder.py      # 创建提醒
│   ├── list_reminders.py       # 列出提醒
│   ├── delete_reminder.py      # 删除提醒
│   ├── test_push.py            # 测试推送
│   ├── check_reminders.py      # 检查并发送
│   ├── daemon.py               # 后台守护进程
│   ├── install_windows_task.py # Windows任务安装
│   └── install_cron.py         # Cron安装
├── assets/
│   └── reminders.example.yaml  # 配置示例
└── references/
    └── guide.md                # 参考文档
```

## 故障排查

### 收不到提醒？

1. 先测试推送服务：`python scripts/test_push.py`
2. 检查提醒是否启用
3. 检查日期配置是否正确
4. 检查定时任务是否运行

### 查看日志

手动运行检查：
```bash
python scripts/check_reminders.py
```

## 许可证

MIT License
