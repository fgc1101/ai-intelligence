import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from configs.settings import EMAIL_TO, SMTP_HOST, SMTP_PASS, SMTP_PORT, SMTP_USER, TZ_CN


def format_html(articles: list[dict]) -> str:
    date_str = datetime.now(TZ_CN).strftime("%Y-%m-%d")
    rows = ""
    for i, a in enumerate(articles, 1):
        rows += f"""
        <div style="margin-bottom:24px;padding:16px;border-left:4px solid #4A90D9;background:#f8f9fa;">
            <h3 style="margin:0 0 8px;">{i}. {a.get('plain_title', a.get('original_title', ''))}</h3>
            <p><b>发生了什么：</b>{a.get('what_happened', '')}</p>
            <p><b>人话解释：</b>{a.get('explanation', '')}</p>
            <p><b>影响人群：</b>{a.get('affected_roles', '')}</p>
            <p><b>未来趋势：</b>{a.get('future_trend', '')}</p>
            <p><a href="{a.get('url', '')}">查看原文</a></p>
        </div>"""
    return f"""
    <html><body style="font-family:sans-serif;max-width:680px;margin:0 auto;color:#333;">
        <h2 style="color:#1a1a1a;">AI 情报日报 — {date_str}</h2>
        {rows}
        <p style="color:#999;font-size:12px;">共 {len(articles)} 条情报 | AI Intelligence</p>
    </body></html>"""


def send_email(articles: list[dict]) -> bool:
    if not SMTP_USER or not SMTP_PASS or not EMAIL_TO:
        print("  Email not configured, skipping")
        return False
    date_str = datetime.now(TZ_CN).strftime("%Y-%m-%d")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"AI 情报日报 — {date_str}"
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_TO
    msg.attach(MIMEText(format_html(articles), "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, EMAIL_TO.split(","), msg.as_string())
        print(f"  Email sent to {EMAIL_TO}")
        return True
    except Exception as e:
        print(f"  Email send failed: {e}")
        return False
