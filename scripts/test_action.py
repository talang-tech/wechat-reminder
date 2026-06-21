#!/usr/bin/env python3
"""
测试推送服务
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from reminder import create_notifier_from_env


def main():
    print("=== 微信提醒测试 ===")
    print()

    notifier = create_notifier_from_env()

    if not notifier:
        print("✗ 未检测到推送服务配置")
        print()
        print("请检查以下环境变量是否正确设置：")
        print("  - 企业微信: WECOM_CORPID, WECOM_CORPSECRET, WECOM_AGENTID, WECOM_TOUSER")
        print("  - Server酱: SCT_KEY")
        print("  - WxPusher: WXPUSHER_APP_TOKEN, WXPUSHER_UIDS")
        print("  - PushPlus: PUSHPLUS_TOKEN")
        return 1

    print(f"✓ 通知器创建成功: {type(notifier).__name__}")
    print()
    print("正在发送测试消息...")
    print()

    result = notifier.send(
        "测试消息 🎉",
        "这是一条来自 GitHub Actions 的测试消息！\n\n如果你收到了，说明配置成功！"
    )

    if result:
        print("✓ 测试消息发送成功！请查看微信/企业微信")
        return 0
    else:
        print("✗ 消息发送失败，请检查配置")
        return 1


if __name__ == "__main__":
    sys.exit(main())
