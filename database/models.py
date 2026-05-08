from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    source: str
    url: str
    title: str
    content: str
    category: str = ""
    tags: list[str] = field(default_factory=list)
    published_at: Optional[datetime] = None
    summary: str = ""
    impact: str = ""
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "url": self.url,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "tags": self.tags,
            "published_at": self.published_at.isoformat() if self.published_at else None,
        }
