# 微信提醒技能 - 参考文档

## 推送服务配置详解

### Server酱

**官网**: https://sct.ftqq.com

**特点**:
- 简单易用，配置方便
- 免费版每天5条消息
- 支持Markdown格式

**配置步骤**:
1. 访问官网，使用微信扫码登录
2. 复制你的 SENDKEY
3. 设置环境变量或创建 .env 文件

**限额**:
- 免费版：每天5条
- 付费版：每天更多，支持更多功能

### WxPusher

**官网**: https://wxpusher.zjiecode.com

**特点**:
- 支持推送给多个人
- 有API接口，可以更灵活使用
- 免费版有额度限制

**配置步骤**:
1. 访问官网注册
2. 创建应用，获取 APP_TOKEN
3. 让需要接收提醒的人关注公众号，获取他们的 UID
4. 配置环境变量

### PushPlus

**官网**: https://www.pushplus.plus

**特点**:
- 模板丰富
- 支持多种推送方式
- 免费可用

## Cron 表达式参考

| 表达式 | 说明 |
|--------|------|
| `* * * * *` | 每分钟 |
| `0 * * * *` | 每小时 |
| `0 9 * * *` | 每天9点 |
| `0 9 * * 1-5` | 工作日9点 |
| `0 9,12,18 * * *` | 每天9点、12点、18点 |

## Windows 任务计划程序

可以通过"任务计划程序" GUI管理任务：
1. 按 Win+R，输入 `taskschd.msc`
2. 找到 "WeChatReminder" 任务
3. 可以修改、禁用或删除

## 常见问题

### Q: 提醒没有发送？

A: 按此顺序排查：
1. `python scripts/test_push.py` 测试推送是否正常
2. `python scripts/list_reminders.py` 确认提醒已启用
3. `python scripts/check_reminders.py` 手动运行检查
4. 确认定时任务在运行

### Q: 如何修改提醒时间？

A: 编辑 `reminders.yaml` 文件，修改 `time` 字段，或者使用交互式向导重新创建。

### Q: 可以同时使用多个推送服务吗？

A: 目前一次只能配置一个服务，但你可以修改代码支持同时发送到多个服务。

### Q: 提醒内容支持Markdown吗？

A: Server酱和WxPusher支持Markdown格式的内容。
