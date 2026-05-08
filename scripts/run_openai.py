"""Fetch OpenAI News and save raw articles to storage."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipelines.collect_pipeline import save_raw
from sources.official.openai.crawler import OpenAICrawler


def main():
    crawler = OpenAICrawler()
    print("Fetching OpenAI News RSS...")
    raw_items = crawler.fetch()
    print(f"Fetched {len(raw_items)} articles")

    articles = [crawler.parse(item).to_dict() for item in raw_items]
    path = save_raw(articles, "openai")
    print(f"Saved to {path}")

    for a in articles[:5]:
        print(f"  [{a['category']}] {a['title']}")


if __name__ == "__main__":
    main()
