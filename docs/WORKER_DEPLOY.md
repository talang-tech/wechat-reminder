# Cloudflare Worker 代理部署指南

使用 Cloudflare Worker 作为代理，解决 GitHub Actions IP 不固定的问题。完全免费，稳定可靠！

## 🌟 优势

- ✅ 完全免费（每天 10 万次请求足够用）
- ✅ 无需云服务器
- ✅ 解决企业微信 IP 白名单问题
- ✅ 配置简单

---

## 🚀 部署步骤

### 步骤 1：注册 Cloudflare 账号

1. 访问 https://dash.cloudflare.com/sign-up
2. 注册账号（免费）
3. 不需要购买域名也可以使用 Workers

### 步骤 2：创建 Worker

1. 登录 Cloudflare Dashboard
2. 左侧菜单点击 **Workers & Pages**
3. 点击 **Create application** → **Create Worker**
4. 给 Worker 起个名字，比如 `wechat-reminder-proxy`
5. 点击 **Deploy**

### 步骤 3：编辑 Worker 代码

1. 点击 **Edit code**
2. 删除默认代码，粘贴 `worker/worker.js` 中的内容
3. 点击 **Deploy**

### 步骤 4：配置环境变量

1. 在 Worker 页面，点击 **Settings** → **Variables**
2. 在 **Environment Variables** 部分，点击 **Add variable**
3. 添加以下变量：

| 变量名 | 值 |
|--------|-----|
| `WECOM_CORPID` | 你的企业 ID |
| `WECOM_CORPSECRET` | 你的应用 Secret |
| `WECOM_AGENTID` | 你的应用 AgentId（如 1000002） |
| `WECOM_TOUSER` | 接收人 UserId |
| `AUTH_TOKEN` | 自定义一个密钥（比如 `my-secret-token-123`） |

4. 点击 **Save and deploy**

### 步骤 5：获取 Worker URL

在 Worker 详情页，你会看到 URL，类似：
```
https://wechat-reminder-proxy.你的用户名.workers.dev
```

### 步骤 6：获取 Cloudflare IP 并添加到企业微信白名单

运行以下命令获取 Cloudflare Worker 的出口 IP（或者查看 Cloudflare 官方 IP 列表）：

Cloudflare 的官方 IP 段：
- IPv4: https://www.cloudflare.com/ips-v4
- IPv6: https://www.cloudflare.com/ips-v6

**更简单的方法**：先测试发送一次，企业微信错误信息会提示当前 IP，把那个 IP 添加到白名单即可。

---

## 📝 配置 GitHub Secrets

在 GitHub 仓库 Settings → Secrets → Actions 中，添加：

| Secret 名称 | 值 |
|-------------|-----|
| `WORKER_URL` | 你的 Worker URL（如 https://wechat-reminder-proxy.xxx.workers.dev） |
| `WORKER_TOKEN` | 你设置的 AUTH_TOKEN |

**删除/不需要的 Secrets**：
- 可以删除 `WECOM_CORPID`、`WECOM_CORPSECRET`、`WECOM_AGENTID`、`WECOM_TOUSER`（这些已经保存在 Worker 中了）

---

## ✅ 测试

在 GitHub Actions 中运行测试，应该可以收到消息了！

---

## 🔒 安全说明

- `AUTH_TOKEN` 用于验证请求，防止别人滥用你的 Worker
- 企业微信凭证只保存在 Cloudflare 环境变量中，不会暴露
- Worker URL 不要公开分享

---

## 📊 调用方式

Worker 接受 POST 请求：

```bash
curl -X POST https://你的-worker-url \
  -H "Authorization: Bearer 你的AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "喝水提醒 💧",
    "content": "该喝水了！"
  }'
```

响应：
```json
{ "success": true, "message": "Message sent" }
```
