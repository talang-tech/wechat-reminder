#!/usr/bin/env python3
"""
微信提醒核心模块
"""

import os
import yaml
import time
import datetime
import requests
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Reminder:
    """提醒配置"""
    id: str
    title: str
    content: str
    time: str  # HH:MM
    enabled: bool = True
    days: List[int] = None  # 1=周一, 7=周日
    last_sent: str = None  # 最后发送日期 YYYY-MM-DD

    def __post_init__(self):
        if self.days is None:
            self.days = [1, 2, 3, 4, 5, 6, 7]


class Notifier:
    """推送通知基类"""

    def send(self, title: str, content: str) -> bool:
        """发送通知，返回是否成功"""
        raise NotImplementedError


class ServerChanNotifier(Notifier):
    """Server酱推送"""

    def __init__(self, sendkey: str):
        self.sendkey = sendkey
        self.api_url = f"https://sctapi.ftqq.com/{sendkey}.send"

    def send(self, title: str, content: str) -> bool:
        try:
            response = requests.post(
                self.api_url,
                data={"title": title, "desp": content},
                timeout=10
            )
            result = response.json()
            return result.get("code") == 0
        except Exception as e:
            print(f"Server酱推送失败: {e}")
            return False


class WxPusherNotifier(Notifier):
    """WxPusher推送"""

    def __init__(self, app_token: str, uids: List[str]):
        self.app_token = app_token
        self.uids = uids
        self.api_url = "https://wxpusher.zjiecode.com/api/send/message"

    def send(self, title: str, content: str) -> bool:
        try:
            full_content = f"# {title}\n\n{content}"
            response = requests.post(
                self.api_url,
                json={
                    "appToken": self.app_token,
                    "content": full_content,
                    "contentType": 3,  # Markdown
                    "uids": self.uids
                },
                timeout=10
            )
            result = response.json()
            return result.get("success", False)
        except Exception as e:
            print(f"WxPusher推送失败: {e}")
            return False


class PushPlusNotifier(Notifier):
    """PushPlus推送"""

    def __init__(self, token: str):
        self.token = token
        self.api_url = "https://www.pushplus.plus/send"

    def send(self, title: str, content: str) -> bool:
        try:
            response = requests.post(
                self.api_url,
                json={
                    "token": self.token,
                    "title": title,
                    "content": content,
                    "template": "txt"
                },
                timeout=10
            )
            result = response.json()
            return result.get("code") == 200
        except Exception as e:
            print(f"PushPlus推送失败: {e}")
            return False


class WeComNotifier(Notifier):
    """企业微信推送"""

    def __init__(self, corpid: str, corpsecret: str, agentid: str, touser: str):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.touser = touser  # 接收人，多个用 | 分隔
        self.access_token = None
        self.token_expires = 0

    def _get_access_token(self) -> Optional[str]:
        """获取 access_token"""
        now = time.time()
        if self.access_token and now < self.token_expires - 60:
            return self.access_token

        try:
            url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
            response = requests.get(
                url,
                params={
                    "corpid": self.corpid,
                    "corpsecret": self.corpsecret
                },
                timeout=10
            )
            result = response.json()
            if result.get("errcode") == 0:
                self.access_token = result.get("access_token")
                self.token_expires = now + result.get("expires_in", 7200)
                return self.access_token
            else:
                print(f"获取access_token失败: {result}")
                return None
        except Exception as e:
            print(f"获取access_token异常: {e}")
            return None

    def send(self, title: str, content: str) -> bool:
        """发送企业微信消息（支持Markdown）"""
        access_token = self._get_access_token()
        if not access_token:
            return False

        try:
            url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"

            # 构建Markdown消息
            markdown_content = f"### {title}\n\n{content}"

            response = requests.post(
                url,
                json={
                    "touser": self.touser,
                    "msgtype": "markdown",
                    "agentid": int(self.agentid),
                    "markdown": {
                        "content": markdown_content
                    }
                },
                timeout=10
            )
            result = response.json()
            if result.get("errcode") == 0:
                return True
            else:
                print(f"企业微信发送失败: {result}")
                return False
        except Exception as e:
            print(f"企业微信推送异常: {e}")
            return False


class WorkerNotifier(Notifier):
    """Cloudflare Worker 代理推送（解决IP白名单问题）"""

    def __init__(self, worker_url: str, auth_token: str):
        self.worker_url = worker_url.rstrip('/')
        self.auth_token = auth_token

    def send(self, title: str, content: str) -> bool:
        try:
            send_url = f"{self.worker_url}/send"
            response = requests.post(
                send_url,
                headers={
                    "Authorization": f"Bearer {self.auth_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "title": title,
                    "content": content
                },
                timeout=10
            )
            result = response.json()
            if result.get("success"):
                return True
            else:
                print(f"Worker代理发送失败: {result.get('error', result)}")
                return False
        except Exception as e:
            print(f"Worker代理异常: {e}")
            return False


class ReminderManager:
    """提醒管理器"""

    def __init__(self, config_path: str, notifier: Notifier):
        self.config_path = Path(config_path)
        self.notifier = notifier
        self.reminders: Dict[str, Reminder] = {}
        self._load()

    def _load(self):
        """加载配置"""
        if not self.config_path.exists():
            self.reminders = {}
            return

        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}

        for r_data in data.get('reminders', []):
            reminder = Reminder(**r_data)
            self.reminders[reminder.id] = reminder

    def _save(self):
        """保存配置"""
        data = {
            'reminders': [asdict(r) for r in self.reminders.values()]
        }
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    def add_reminder(self, title: str, content: str, time: str,
                     days: List[int] = None) -> Reminder:
        """添加提醒"""
        # 生成ID
        reminder_id = title.lower().replace(' ', '-')[:50]
        if reminder_id in self.reminders:
            reminder_id = f"{reminder_id}-{int(time.time())}"

        reminder = Reminder(
            id=reminder_id,
            title=title,
            content=content,
            time=time,
            days=days
        )
        self.reminders[reminder.id] = reminder
        self._save()
        return reminder

    def delete_reminder(self, reminder_id: str) -> bool:
        """删除提醒"""
        if reminder_id in self.reminders:
            del self.reminders[reminder_id]
            self._save()
            return True
        return False

    def get_reminders(self) -> List[Reminder]:
        """获取所有提醒"""
        return list(self.reminders.values())

    def should_send(self, reminder: Reminder, now: datetime.datetime = None) -> bool:
        """检查是否应该发送提醒"""
        if now is None:
            now = datetime.datetime.now()

        if not reminder.enabled:
            return False

        # 检查星期几 (1=周一, 7=周日)
        weekday = now.isoweekday()
        if weekday not in reminder.days:
            return False

        # 检查时间
        target_time = datetime.datetime.strptime(reminder.time, "%H:%M").time()
        current_time = now.time()

        # 检查是否在同一分钟
        if (current_time.hour == target_time.hour and
                current_time.minute == target_time.minute):
            # 检查今天是否已经发送过
            today_str = now.strftime("%Y-%m-%d")
            if reminder.last_sent == today_str:
                return False
            return True

        return False

    def check_and_send(self, now: datetime.datetime = None) -> List[Reminder]:
        """检查并发送到期提醒，返回已发送的提醒列表"""
        if now is None:
            now = datetime.datetime.now()

        sent = []
        for reminder in self.reminders.values():
            if self.should_send(reminder, now):
                if self.notifier.send(reminder.title, reminder.content):
                    reminder.last_sent = now.strftime("%Y-%m-%d")
                    sent.append(reminder)
                    print(f"✓ 已发送提醒: {reminder.title}")

        if sent:
            self._save()

        return sent


def create_notifier_from_env() -> Optional[Notifier]:
    """从环境变量创建通知器"""
    # 优先尝试 Cloudflare Worker 代理
    worker_url = os.getenv("WORKER_URL")
    worker_token = os.getenv("WORKER_TOKEN")
    if worker_url and worker_token:
        return WorkerNotifier(worker_url, worker_token)

    # 尝试企业微信（需要固定IP）
    wecom_corpid = os.getenv("WECOM_CORPID")
    wecom_corpsecret = os.getenv("WECOM_CORPSECRET")
    wecom_agentid = os.getenv("WECOM_AGENTID")
    wecom_touser = os.getenv("WECOM_TOUSER")
    if wecom_corpid and wecom_corpsecret and wecom_agentid and wecom_touser:
        return WeComNotifier(wecom_corpid, wecom_corpsecret, wecom_agentid, wecom_touser)

    # 尝试 Server酱
    sct_key = os.getenv("SCT_KEY")
    if sct_key:
        return ServerChanNotifier(sct_key)

    # 尝试 WxPusher
    wx_token = os.getenv("WXPUSHER_APP_TOKEN")
    wx_uids = os.getenv("WXPUSHER_UIDS")
    if wx_token and wx_uids:
        uids = [u.strip() for u in wx_uids.split(",")]
        return WxPusherNotifier(wx_token, uids)

    # 尝试 PushPlus
    pp_token = os.getenv("PUSHPLUS_TOKEN")
    if pp_token:
        return PushPlusNotifier(pp_token)

    return None
