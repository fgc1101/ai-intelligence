from datetime import datetime, timezone
from pathlib import Path

import feedparser
import requests

from configs.settings import RAW_DIR
from database.models import Article
from sources.base import BaseCrawler

RSS_URL = "https://openai.com/blog/rss.xml"
SOURCE_NAME = "openai"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}


class OpenAICrawler(BaseCrawler):
    def __init__(self, rss_url: str = RSS_URL):
        self.rss_url = rss_url

    def fetch(self) -> list[dict]:
        path = Path(self.rss_url)
        if path.exists():
            content = path.read_bytes()
        else:
            resp = requests.get(self.rss_url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            content = resp.content
        feed = feedparser.parse(content)
        if feed.bozo and not feed.entries:
            raise RuntimeError(f"Failed to parse RSS feed: {feed.bozo_exception}")
        return [self._entry_to_raw(e) for e in feed.entries]

    def parse(self, raw: dict) -> Article:
        return Article(
            source=SOURCE_NAME,
            url=raw["url"],
            title=raw["title"],
            content=raw["description"],
            category=raw.get("category", ""),
            published_at=raw.get("published_at"),
        )

    @staticmethod
    def _entry_to_raw(entry) -> dict:
        published_at = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published_at = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

        return {
            "title": entry.get("title", ""),
            "url": entry.get("link", ""),
            "description": entry.get("summary", ""),
            "category": entry.get("category", ""),
            "published_at": published_at,
        }
