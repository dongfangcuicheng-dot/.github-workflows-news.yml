import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

news_api_key = os.environ["NEWS_API_KEY"]
qq_email = os.environ["QQ_EMAIL"]
qq_auth_code = os.environ["QQ_AUTH_CODE"]

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
        description = article.get("description") or "无简介"
        source = article.get("source", {}).get("name", "未知来源")
        url_link = article.get("url", "")
        result += f"{i}. 【{source}】{title}\n{description}\n{url_link}\n\n"

    return result

def send_email(content):
    today = datetime.now().strftime("%Y年%m月%d日")
    subject = f"📰 阿曼每日新闻 {today}"
    body = f"阿曼每日新闻 {today}\n\n{content}"

    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = qq_email
    msg["To"] = qq_email
    msg["Subject"] = subject

    with smtplib.SMTP_SSL("smtp.qq.com", 465) as smtp:
        smtp.login(qq_email, qq_auth_code)
        smtp.sendmail(qq_email, qq_email, msg.as_string())
    print("✅ 邮件发送成功！")

if __name__ == "__main__":
    news = fetch_oman_news()
    print(news)
    send_email(news)
