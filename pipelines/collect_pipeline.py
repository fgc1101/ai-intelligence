import json
from datetime import datetime, timezone
from pathlib import Path

from configs.settings import RAW_DIR


def save_raw(articles: list[dict], source: str, storage_dir: Path = RAW_DIR) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_dir = storage_dir / source
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{ts}.json"
    path.write_text(json.dumps(articles, ensure_ascii=False, indent=2, default=str))
    return path
