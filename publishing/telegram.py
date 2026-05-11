import json
from datetime import datetime

import requests

from configs.settings import PUBLISHED_DIR, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TZ_CN

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"
MAX_MSG_LEN = 4000


def format_digest(articles: list[dict]) -> str:
    if not articles:
        return ""
    lines = ["*AI 情报日报*\n"]
    for i, a in enumerate(articles, 1):
        lines.append(f"{i}. *{a.get('plain_title', a.get('original_title', ''))}*")
        lines.append(f"发生了什么：{a.get('what_happened', '')}")
        lines.append(f"人话解释：{a.get('explanation', '')}")
        lines.append(f"影响人群：{a.get('affected_roles', '')}")
        lines.append(f"未来趋势：{a.get('future_trend', '')}")
        lines.append(f"[原文链接]({a.get('url', '')})")
        lines.append("---")
    date_str = datetime.now(TZ_CN).strftime("%Y-%m-%d")
    lines.append(f"共 {len(articles)} 条情报 | {date_str}")
    return "\n".join(lines)


def split_message(text: str, max_len: int = MAX_MSG_LEN) -> list[str]:
    if len(text) <= max_len:
        return [text] if text else []
    parts = text.split("---")
    messages = []
    current = ""
    for part in parts:
        chunk = part.strip()
        if not chunk:
            continue
        section = part if not current else "---" + part
        if len(current) + len(section) > max_len:
            if current:
                messages.append(current)
            current = chunk
        else:
            current += section
    if current:
        messages.append(current)
    return messages


def send_telegram(text: str, token: str = "", chat_id: str = "") -> bool:
    token = token or TELEGRAM_BOT_TOKEN
    chat_id = chat_id or TELEGRAM_CHAT_ID
    if not token or not chat_id:
        print("  Telegram not configured, skipping publish")
        return False
    url = TELEGRAM_API.format(token=token)
    try:
        resp = requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}, timeout=30)
        if resp.status_code != 200:
            print(f"  Telegram error: {resp.text}")
            return False
        return True
    except Exception as e:
        print(f"  Telegram send failed: {e}")
        return False


def publish_digest(articles: list[dict], source: str) -> bool:
    if not articles:
        print("  No articles to publish")
        return True
    digest = format_digest(articles)
    messages = split_message(digest)
    success = True
    for msg in messages:
        if not send_telegram(msg):
            success = False
    # Save published record
    ts = datetime.now(TZ_CN).strftime("%Y%m%d_%H%M%S")
    out_dir = PUBLISHED_DIR / source
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{ts}.json"
    path.write_text(json.dumps(articles, ensure_ascii=False, indent=2, default=str))
    return success
