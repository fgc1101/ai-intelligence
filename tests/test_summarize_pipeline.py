from unittest.mock import patch

from pipelines.summarize_pipeline import process_article


class TestProcessArticle:
    @patch("pipelines.summarize_pipeline.analyze_impact")
    @patch("pipelines.summarize_pipeline.summarize_article")
    def test_enriches_article(self, mock_summarize, mock_impact):
        mock_summarize.return_value = {
            "人话标题": "GPT大升级",
            "发生了什么": "OpenAI发布了新模型",
            "人话解释": "这次升级意味着...",
            "影响人群": "开发者、创业者",
            "未来趋势": "AI能力会更强",
        }
        mock_impact.return_value = {
            "affected_roles": "开发者、产品经理",
            "trend": "AI开发门槛降低",
        }
        article = {"title": "Introducing GPT-5.5", "url": "https://example.com", "content": "blah", "category": "Product", "score": 8, "source": "openai"}
        result = process_article(article)
        assert result["plain_title"] == "GPT大升级"
        assert result["explanation"] == "这次升级意味着..."
        assert result["future_trend"] == "AI开发门槛降低"
        assert result["original_title"] == "Introducing GPT-5.5"

    @patch("pipelines.summarize_pipeline.analyze_impact", side_effect=Exception("LLM error"))
    @patch("pipelines.summarize_pipeline.summarize_article")
    def test_error_skips_article(self, mock_summarize, mock_impact):
        mock_summarize.return_value = {"人话标题": "t", "发生了什么": "", "人话解释": "", "影响人群": "", "未来趋势": ""}
        from pipelines.summarize_pipeline import summarize_pipeline
        import json
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cleaned_dir = td / "openai"
            cleaned_dir.mkdir()
            (cleaned_dir / "test.json").write_text(json.dumps([{"title": "t", "url": "u", "content": "c"}]))
            with patch("pipelines.summarize_pipeline.CLEANED_DIR", td), \
                 patch("pipelines.summarize_pipeline.SUMMARIZED_DIR", td / "out"):
                result = summarize_pipeline("openai")
            assert result == []
