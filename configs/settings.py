import os
from datetime import timezone, timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
TZ_CN = timezone(timedelta(hours=8))

# Storage
RAW_DIR = BASE_DIR / "storage" / "raw"
CLEANED_DIR = BASE_DIR / "storage" / "cleaned"
SUMMARIZED_DIR = BASE_DIR / "storage" / "summarized"
PUBLISHED_DIR = BASE_DIR / "storage" / "published"

# LLM — 支持 openai/*, anthropic/*, volcengine/* 等前缀
# 火山引擎示例: volcengine/ep-20241209123456-xxxxx
LLM_MODEL = os.getenv("LLM_MODEL", "volcengine/ep-placeholder")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
VOLCENGINE_API_KEY = os.getenv("VOLCENGINE_API_KEY")

# Email
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.qq.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
