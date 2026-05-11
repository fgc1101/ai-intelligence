import json
from datetime import datetime
from pathlib import Path

from ai.tasks.analyze import analyze_impact
from ai.tasks.summarize import summarize_article
from configs.settings import CLEANED_DIR, SUMMARIZED_DIR, TZ_CN


def load_cleaned(source: str, storage_dir: Path = CLEANED_DIR) -> list[dict]:
    source_dir = storage_dir / source
    if not source_dir.exists():
        return []
    files = sorted(source_dir.glob("*.json"))
    if not files:
        return []
    return json.loads(files[-1].read_text())


def process_article(article: dict) -> dict:
    summary = summarize_article(article)
    impact = analyze_impact(article, summary)
    return {
        "source": article.get("source", ""),
        "url": article.get("url", ""),
        "original_title": article.get("title", ""),
        "category": article.get("category", ""),
        "published_at": article.get("published_at", ""),
        "score": article.get("score", 0),
        "plain_title": summary.get("人话标题", ""),
        "what_happened": summary.get("发生了什么", ""),
        "explanation": summary.get("人话解释", ""),
        "affected_roles": summary.get("影响人群", ""),
        "trend": summary.get("未来趋势", ""),
        "impact_detail": impact.get("affected_roles", ""),
        "future_trend": impact.get("trend", ""),
    }


def save_summarized(articles: list[dict], source: str, storage_dir: Path = SUMMARIZED_DIR) -> Path:
    ts = datetime.now(TZ_CN).strftime("%Y%m%d_%H%M%S")
    out_dir = storage_dir / source
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{ts}.json"
    path.write_text(json.dumps(articles, ensure_ascii=False, indent=2, default=str))
    return path


def summarize_pipeline(source: str) -> list[dict]:
    articles = load_cleaned(source)
    if not articles:
        return []
    results = []
    for a in articles:
        try:
            enriched = process_article(a)
            results.append(enriched)
        except Exception as e:
            print(f"  Error processing '{a.get('title', '?')}': {e}")
    if results:
        save_summarized(results, source)
    return results
