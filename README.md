# wechat-reminder-skill — 微信定时提醒技能

一个简单易用的微信定时提醒工具，支持日常任务提醒、喝水提醒、吃药提醒等。

## 功能特点

- ✅ 支持多种微信推送服务（企业微信、Server酱、WxPusher、PushPlus）
- ✅ 支持 Cloudflare Worker 代理（解决企业微信 IP 白名单问题）
- ✅ 灵活的提醒配置（时间、日期、内容）
- ✅ GitHub Actions / 云服务器 / 本地 多种部署方式
- ✅ 简单的命令行工具

## 推荐方案对比

| 方案 | 难度 | 成本 | 适合企业微信 | 推荐度 |
|------|------|------|-------------|--------|
| ☁️ **GitHub Actions + Server酱** | ⭐ 简单 | 免费 | ❌ | ⭐⭐⭐⭐⭐ 最快上手 |
| 🔶 **GitHub Actions + Cloudflare Worker** | ⭐⭐ 中等 | 免费 | ✅ | ⭐⭐⭐⭐⭐ 推荐方案 |
| 🖥️ **云服务器** | ⭐⭐⭐ 较难 | ~50元/年 | ✅ | ⭐⭐⭐⭐ 最稳定 |
| 💻 **本地运行** | ⭐ 简单 | 免费 | ✅ | ⭐⭐ 测试用 |

---

## 🚀 方案一：GitHub Actions + Server酱（最快，5分钟）

1. 访问 https://sct.ftqq.com 扫码获取 SENDKEY
2. 部署到 GitHub（参考 docs/GITHUB_DEPLOY.md）
3. 添加 GitHub Secret: `SCT_KEY`

---

## 🔶 方案二：GitHub Actions + Cloudflare Worker（推荐）

完美解决企业微信 IP 白名单问题，全部免费！

### 步骤：

1. **部署 Cloudflare Worker**（详见 docs/WORKER_DEPLOY.md）
2. **添加 GitHub Secrets**：
   - `WORKER_URL`: 你的 Worker URL
   - `WORKER_TOKEN`: 你设置的 AUTH_TOKEN

详细文档：[docs/WORKER_DEPLOY.md](docs/WORKER_DEPLOY.md)

---

## 🖥️ 方案三：云服务器

最稳定的方案。详见：[docs/SERVER_DEPLOY.md](docs/SERVER_DEPLOY.md)

一键部署：
```bash
wget -O deploy-server.sh https://raw.githubusercontent.com/talang-tech/wechat-reminder/main/deploy-server.sh
chmod +x deploy-server.sh
sudo bash deploy-server.sh
```

---

## 配置说明

### 提醒配置 (reminders.yaml)

```yaml
reminders:
  - id: drink-water
    title: "喝水提醒 💧"
    content: "该喝水了！保持健康的饮水习惯。"
    time: "09:00"
    enabled: true
    days: [1, 2, 3, 4, 5, 6, 7]  # 1=周一, 7=周日
```

### 环境变量

| 变量 | 用途 |
|------|------|
| `WORKER_URL` + `WORKER_TOKEN` | Cloudflare Worker 代理 |
| `SCT_KEY` | Server酱 |
| `WECOM_*` | 企业微信直连（需固定IP） |
| `WXPUSHER_*` | WxPusher |
| `PUSHPLUS_TOKEN` | PushPlus |

---

## 文档

- [GitHub Actions 部署](docs/GITHUB_DEPLOY.md)
- [Cloudflare Worker 部署](docs/WORKER_DEPLOY.md) ⭐
- [云服务器部署](docs/SERVER_DEPLOY.md)

---

## 许可证

MIT License
