# 部署到 GitHub Actions

使用 GitHub Actions 免费运行定时提醒，无需你的电脑一直开机！

## 🌟 优势

- ✅ 免费使用 GitHub Actions
- ✅ 24/7 云端运行，无需开机
- ✅ 配置简单，几分钟搞定
- ✅ 支持多个提醒

## 🚀 部署步骤

### 1. 创建 GitHub 仓库

1. 登录 GitHub，点击右上角 "+" → "New repository"
2. 仓库名: `wechat-reminder` (或你喜欢的名字)
3. 选择 Public 或 Private (推荐 Private)
4. 点击 "Create repository"

### 2. 推送代码到 GitHub

```bash
cd ~/.claude/skills/wechat-reminder-skill

# 初始化 git
git init
git add .
git commit -m "Initial commit: WeChat reminder skill"

# 添加远程仓库
git remote add origin https://github.com/你的用户名/wechat-reminder.git
git branch -M main
git push -u origin main
```

### 3. 配置 Secrets

在 GitHub 仓库中：

1. 点击 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. 添加以下 Secret (根据你选择的推送服务)：

**使用 Server酱 (推荐)**：
- Name: `SCT_KEY`
- Value: 你的 Server酱 SENDKEY

**使用 WxPusher**：
- Name: `WXPUSHER_APP_TOKEN`
- Value: 你的 APP_TOKEN
- Name: `WXPUSHER_UIDS`
- Value: 你的 UID

**使用 PushPlus**：
- Name: `PUSHPLUS_TOKEN`
- Value: 你的 Token

**可选：自定义提醒配置**：
- Name: `REMINDERS_CONFIG`
- Value: (完整的 YAML 配置内容)

### 4. 配置提醒

#### 方式 A: 使用仓库中的 reminders.yaml (推荐)

编辑仓库中的 `reminders.yaml` 文件，提交后会自动使用。

#### 方式 B: 使用 Secrets 配置

在 Secrets 中添加 `REMINDERS_CONFIG`，值为完整的 YAML：

```yaml
reminders:
  - id: drink-water
    title: "喝水提醒 💧"
    content: "该喝水了！"
    time: "09:00"
    enabled: true
    days: [1, 2, 3, 4, 5, 6, 7]
```

### 5. 启用 Workflow

1. 在 GitHub 仓库点击 **Actions**
2. 你会看到 "微信定时提醒" workflow
3. 点击它，然后点击 "Enable workflow"
4. 可以点击 "Run workflow" 手动测试一次

## ⏰ 时区说明

GitHub Actions 使用 UTC 时间。

**中国时区 (UTC+8) 转换：**

| 本地时间 | UTC 时间 (cron) |
|---------|----------------|
| 09:00 | 01:00 |
| 12:00 | 04:00 |
| 18:00 | 10:00 |
| 22:00 | 14:00 |

Workflow 配置为每分钟运行一次，脚本会根据 `reminders.yaml` 中的时间判断是否发送。

## 📋 提醒配置示例

```yaml
reminders:
  - id: drink-water-9
    title: "喝水提醒 💧"
    content: "早上9点了，该喝一杯水了！"
    time: "09:00"
    enabled: true
    days: [1, 2, 3, 4, 5, 6, 7]

  - id: drink-water-11
    title: "喝水提醒 💧"
    content: "上午11点了，记得喝水！"
    time: "11:00"
    enabled: true
    days: [1, 2, 3, 4, 5, 6, 7]

  - id: drink-water-15
    title: "喝水提醒 💧"
    content: "下午3点了，补充水分！"
    time: "15:00"
    enabled: true
    days: [1, 2, 3, 4, 5, 6, 7]

  - id: take-medicine
    title: "吃药提醒 💊"
    content: "记得吃药！"
    time: "08:30"
    enabled: true
    days: [1, 2, 3, 4, 5]
```

## 🧪 测试

在 GitHub Actions 页面：
1. 点击 "微信定时提醒" workflow
2. 点击 "Run workflow" → "Run workflow"
3. 等待几秒，查看运行结果

## 💡 GitHub Actions 免费额度

- **Public 仓库**: 无限分钟
- **Private 仓库**: 每月 2000 分钟 (完全够用)

这个 workflow 每分钟运行一次，但每次只执行几秒钟，完全不会超出免费额度！

## 🔧 故障排查

### 收不到提醒？

1. 检查 GitHub Actions 运行日志，看是否有错误
2. 确认 Secrets 配置正确
3. 确认时间设置正确 (注意时区)
4. 测试推送服务是否正常

### 查看日志

1. 进入仓库 → Actions
2. 点击某次 workflow 运行
3. 点击 "check-reminders" job
4. 查看步骤输出

## 📝 修改提醒

要修改提醒，只需：
1. 编辑 `reminders.yaml`
2. 提交并 push 到 GitHub
3. GitHub Actions 会自动使用新配置

## 🎉 完成！

设置好后，GitHub 会自动在云端运行，每天准时给你发送微信提醒！
