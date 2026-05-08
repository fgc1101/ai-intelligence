from abc import ABC, abstractmethod

from database.models import Article


class BaseCrawler(ABC):
    @abstractmethod
    def fetch(self) -> list[dict]:
        """Fetch raw items from the source. Returns list of raw dicts."""

    @abstractmethod
    def parse(self, raw: dict) -> Article:
        """Parse a raw item into an Article."""
