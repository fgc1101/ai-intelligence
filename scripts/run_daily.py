"""Run the full daily pipeline: collect -> clean -> summarize -> publish."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipelines.clean_pipeline import clean_pipeline
from pipelines.collect_pipeline import save_raw
from pipelines.summarize_pipeline import summarize_pipeline
from publishing.telegram import publish_digest
from sources.official.openai.crawler import OpenAICrawler


def main():
    source = "openai"

    # Step 1: Collect
    print("[1/4] Collecting...")
    crawler = OpenAICrawler()
    raw_items = crawler.fetch()
    articles = [crawler.parse(item).to_dict() for item in raw_items]
    path = save_raw(articles, source)
    print(f"  Collected {len(articles)} articles -> {path.name}")

    # Step 2: Clean & Filter
    print("[2/4] Cleaning & filtering...")
    cleaned = clean_pipeline(source)
    print(f"  Kept {len(cleaned)} articles after scoring")
    for a in cleaned:
        print(f"    [{a['score']}] {a['title']}")

    if not cleaned:
        print("  No articles passed filter, done.")
        return

    # Step 3: Summarize
    print("[3/4] Summarizing...")
    summarized = summarize_pipeline(source)
    print(f"  Processed {len(summarized)} articles")

    # Step 4: Publish
    print("[4/4] Publishing...")
    success = publish_digest(summarized, source)
    print("  Done!" if success else "  Publish failed!")


if __name__ == "__main__":
    main()
