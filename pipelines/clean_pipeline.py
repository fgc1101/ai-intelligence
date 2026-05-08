import json
from datetime import datetime, timezone
from pathlib import Path

from ai.tasks.score import score_article
from configs.settings import CLEANED_DIR, RAW_DIR


def load_raw(source: str, storage_dir: Path = RAW_DIR) -> list[dict]:
    source_dir = storage_dir / source
    if not source_dir.exists():
        return []
    files = sorted(source_dir.glob("*.json"))
    if not files:
        return []
    return json.loads(files[-1].read_text())


def deduplicate(articles: list[dict], seen_urls: set | None = None) -> list[dict]:
    seen = set(seen_urls or [])
    result = []
    for a in articles:
        url = a.get("url", "")
        if url and url not in seen:
            seen.add(url)
            result.append(a)
    return result


def score_and_filter(articles: list[dict], min_score: int = 7) -> list[dict]:
    scored = []
    for a in articles:
        s = score_article(a)
        a["score"] = s
        if s >= min_score:
            scored.append(a)
    return scored


def save_cleaned(articles: list[dict], source: str, storage_dir: Path = CLEANED_DIR) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_dir = storage_dir / source
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{ts}.json"
    path.write_text(json.dumps(articles, ensure_ascii=False, indent=2, default=str))
    return path


def clean_pipeline(source: str, min_score: int = 7) -> list[dict]:
    articles = load_raw(source)
    articles = deduplicate(articles)
    articles = score_and_filter(articles, min_score=min_score)
    if articles:
        save_cleaned(articles, source)
    return articles
