import anthropic
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ZAXELの現状コンテキスト（適宜更新してください）
ZAXEL_CONTEXT = """
あなたはZashiiのビジネスアシスタントです。
ZashiiはZAXEL LLC（東京/岡山）のオーナーで、以下を運営しています：

【事業領域】
- 経営コンサルティング（PM/BPR）
- アプリ開発（GitHubPages, React）
- コンテンツ販売（note.com）
- 株式投資

【現在の主要タスク・プロジェクト】
- ZAXELウェブサイト（GitHub Pages）: 運営中
- BPRプロセス改善診断ツール: 開発予定（最優先）
- プロジェクト健全性チェッカー: 開発予定
- KPIデザインウィザード: 開発予定
- note.com有料マガジン「PMゼロから実践塾」: 企画中
- コンサルティング単価アップ（リテイナー契約移行）: 進行中

【目標】
月次売上¥1,000,000、週1日稼働

【今日の日付】
{today}
"""

def generate_todo():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    today = datetime.now().strftime("%Y年%m月%d日（%A）")
    
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=ZAXEL_CONTEXT.format(today=today),
        messages=[
            {
                "role": "user",
                "content": f"""今日（{today}）のZashiiがすべきToDoを提案してください。

以下の形式でメール本文として作成してください：

## 🌅 おはようございます、Zashii！今日のToDoです

### 🔥 最優先（今日必ずやる）
- ...

### 📌 重要（できればやる）
- ...

### 💡 今日のワンポイントアドバイス
...

シンプルで実行しやすいToDoにしてください。多くても合計5〜7個。"""
            }
        ]
    )
    
    return message.content[0].text

def send_email(todo_content: str):
    gmail_user = os.environ["GMAIL_USER"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]
    to_email = os.environ["TO_EMAIL"]
    
    today = datetime.now().strftime("%Y/%m/%d")
    subject = f"☀️ 今日のToDo - {today}"
    
    # HTML形式に変換（簡易）
    html_content = todo_content.replace("\n", "<br>").replace("## ", "<h2>").replace("### ", "<h3>")
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = to_email
    
    # テキスト版とHTML版両方
    part1 = MIMEText(todo_content, "plain", "utf-8")
    part2 = MIMEText(f"<html><body style='font-family:sans-serif;max-width:600px;margin:auto;padding:20px'>{html_content}</body></html>", "html", "utf-8")
    
    msg.attach(part1)
    msg.attach(part2)
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, msg.as_string())
    
    print(f"✅ ToDoメール送信完了 → {to_email}")

if __name__ == "__main__":
    print("🤖 ToDo生成中...")
    todo = generate_todo()
    print(todo)
    print("\n📧 メール送信中...")
    send_email(todo)
