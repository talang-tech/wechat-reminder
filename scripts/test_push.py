#!/usr/bin/env python3
"""
测试推送服务
"""

import argparse
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from reminder import (
    ServerChanNotifier,
    WxPusherNotifier,
    PushPlusNotifier,
    create_notifier_from_env
)


def main():
    parser = argparse.ArgumentParser(description="测试推送服务")
    parser.add_argument("--message", "-m", default="这是一条测试消息 🎉",
                       help="测试消息内容")
    parser.add_argument("--title", "-t", default="测试提醒", help="消息标题")

    # Server酱
    parser.add_argument("--sct-key", help="Server酱 SENDKEY")
    # WxPusher
    parser.add_argument("--wxpusher-token", help="WxPusher APP_TOKEN")
    parser.add_argument("--wxpusher-uids", help="WxPusher UIDs (逗号分隔)")
    # PushPlus
    parser.add_argument("--pushplus-token", help="PushPlus TOKEN")

    args = parser.parse_args()

    # 选择通知器
    notifier = None

    if args.sct_key:
        notifier = ServerChanNotifier(args.sct_key)
        print("使用 Server酱")
    elif args.wxpusher_token and args.wxpusher_uids:
        uids = [u.strip() for u in args.wxpusher_uids.split(",")]
        notifier = WxPusherNotifier(args.wxpusher_token, uids)
        print("使用 WxPusher")
    elif args.pushplus_token:
        notifier = PushPlusNotifier(args.pushplus_token)
        print("使用 PushPlus")
    else:
        notifier = create_notifier_from_env()
        if notifier:
            print("使用环境变量配置的服务")

    if not notifier:
        print("错误: 请提供推送服务配置")
        print()
        print("Server酱: --sct-key SCT123456...")
        print("WxPusher: --wxpusher-token AT_xxx --wxpusher-uids UID_xxx")
        print("PushPlus: --pushplus-token xxx")
        print()
        print("或者设置环境变量: SCT_KEY、WXPUSHER_APP_TOKEN+WXPUSHER_UIDS、PUSHPLUS_TOKEN")
        return 1

    # 发送测试消息
    print(f"发送测试消息: {args.title}")
    success = notifier.send(args.title, args.message)

    if success:
        print("✓ 发送成功! 请查看微信")
        return 0
    else:
        print("✗ 发送失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
