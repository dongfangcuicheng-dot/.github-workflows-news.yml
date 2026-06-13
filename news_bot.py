import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from urllib.parse import quote

news_api_key = os.environ["NEWS_API_KEY"]
qq_email = os.environ["QQ_EMAIL"]
qq_auth_code = os.environ["QQ_AUTH_CODE"]

def translate(text):
    """使用 Google 翻译免费接口"""
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": "zh-CN",
            "dt": "t",
            "q": text
        }
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        translated = ""
        for item in result[0]:
            if item[0]:
                translated += item[0]
        return translated
    except:
        return text

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
        title_en = article.get("title", "无标题")
        desc_en = article.get("description") or ""
        source = article.get("source", {}).get("name", "未知来源")
        url_link = article.get("url", "")

        title_zh = translate(title_en)
        desc_zh = translate(desc_en) if desc_en else "暂无详情"

        result += f"{i}. 【{source}】{title_zh}\n{desc_zh}\n🔗 {url_link}\n\n"

    return result

def send_email(content):
    today = datetime.now().strftime("%Y年%m月%d日")
    subject = f"📰 阿曼每日新闻 {today}"
    body = f"阿曼每日新闻 · {today}\n{'='*30}\n\n{content}\n\n{'='*30}\n本邮件由自动程序发送"

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
