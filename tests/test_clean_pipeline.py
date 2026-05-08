import json
from pathlib import Path
from unittest.mock import patch

import pytest

from pipelines.clean_pipeline import clean_pipeline, deduplicate, load_raw


@pytest.fixture
def raw_articles(tmp_path):
    articles = [
        {"title": "Article A", "url": "https://example.com/a", "content": "content a"},
        {"title": "Article B", "url": "https://example.com/b", "content": "content b"},
        {"title": "Article A dup", "url": "https://example.com/a", "content": "dup"},
    ]
    source_dir = tmp_path / "openai"
    source_dir.mkdir()
    (source_dir / "20260509_000000.json").write_text(json.dumps(articles))
    return tmp_path


class TestLoadRaw:
    def test_loads_most_recent(self, raw_articles):
        result = load_raw("openai", storage_dir=raw_articles)
        assert len(result) == 3

    def test_returns_empty_if_no_dir(self, tmp_path):
        result = load_raw("nonexistent", storage_dir=tmp_path)
        assert result == []


class TestDeduplicate:
    def test_removes_dup_urls(self):
        articles = [
            {"url": "a"}, {"url": "b"}, {"url": "a"},
        ]
        result = deduplicate(articles)
        assert len(result) == 2

    def test_filters_seen_urls(self):
        articles = [{"url": "a"}, {"url": "b"}]
        result = deduplicate(articles, seen_urls={"a"})
        assert len(result) == 1
        assert result[0]["url"] == "b"


class TestCleanPipeline:
    @patch("pipelines.clean_pipeline.score_article", return_value=8)
    def test_filters_by_score(self, mock_score, raw_articles, tmp_path):
        cleaned = clean_pipeline("openai", min_score=7)
        assert len(cleaned) == 2  # deduplicated 3 -> 2, all score 8

    @patch("pipelines.clean_pipeline.score_article", return_value=3)
    def test_all_below_threshold(self, mock_score, raw_articles, tmp_path):
        cleaned = clean_pipeline("openai", min_score=7)
        assert len(cleaned) == 0
