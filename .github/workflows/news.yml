import os
import requests
import anthropic
from datetime import datetime

# 初始化 Claude 客户端
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
webhook_url = os.environ["WEIXIN_WEBHOOK"]

def fetch_oman_news():
    """调用 Claude 搜索阿曼本地新闻"""
    print("正在搜索阿曼新闻...")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[
            {
                "role": "user",
                "content": (
                    "请搜索今天阿曼（Oman）的本地最新新闻，"
                    "包括政治、经济、社会、天气等方面。"
                    "用中文总结5条最重要的新闻，每条新闻包括标题和2-3句简介。"
                    "格式要清晰易读。"
                )
            }
        ]
    )

    # 提取文本内容
    result = ""
    for block in response.content:
        if block.type == "text":
            result += block.text

    return result

def send_to_weixin(content):
    """发送消息到企业微信机器人"""
    today = datetime.now().strftime("%Y年%m月%d日")
    message = f"📰 【阿曼每日新闻】{today}\n\n{content}"

    payload = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }

    response = requests.post(webhook_url, json=payload)
    result = response.json()

    if result.get("errcode") == 0:
        print("✅ 新闻已成功推送到企业微信！")
    else:
        print(f"❌ 推送失败：{result}")

if __name__ == "__main__":
    news = fetch_oman_news()
    print("获取到的新闻内容：")
    print(news)
    send_to_weixin(news)
