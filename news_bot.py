import os
import requests
from datetime import datetime

news_api_key = os.environ["NEWS_API_KEY"]
webhook_url = os.environ["WEIXIN_WEBHOOK"]

def fetch_oman_news():
    print("正在搜索阿曼新闻...")
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "Oman",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": news_api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "ok":
        return f"获取新闻失败：{data.get('message', '未知错误')}"

    articles = data.get("articles", [])
    if not articles:
        return "今日暂无阿曼相关新闻。"

    result = ""
    for i, article in enumerate(articles, 1):
        title = article.get("title", "无标题")
        description = article.get("description", "无简介")
        source = article.get("source", {}).get("name", "未知来源")
        url_link = article.get("url", "")
        result += f"{i}. 【{source}】{title}\n{description}\n{url_link}\n\n"

    return result

def send_to_weixin(content):
    today = datetime.now().strftime("%Y年%m月%d日")
    message = f"📰 【阿曼每日新闻】{today}\n\n{content}"
    payload = {
        "msgtype": "text",
        "text": {"content": message}
    }
    response = requests.post(webhook_url, json=payload)
    result = response.json()
    if result.get("errcode") == 0:
        print("✅ 新闻已成功推送到企业微信！")
    else:
        print(f"❌ 推送失败：{result}")

if __name__ == "__main__":
    news = fetch_oman_news()
    print(news)
    send_to_weixin(news)
