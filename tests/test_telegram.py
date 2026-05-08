from publishing.telegram import format_digest, split_message


class TestFormatDigest:
    def test_empty_list(self):
        assert format_digest([]) == ""

    def test_formats_single_article(self):
        articles = [{
            "plain_title": "GPT大升级",
            "what_happened": "OpenAI发布新模型",
            "explanation": "更强大的AI",
            "affected_roles": "开发者",
            "future_trend": "AI更强",
            "url": "https://example.com",
        }]
        result = format_digest(articles)
        assert "AI 情报日报" in result
        assert "GPT大升级" in result
        assert "https://example.com" in result

    def test_multiple_articles_numbered(self):
        articles = [
            {"plain_title": "A", "what_happened": "", "explanation": "", "affected_roles": "", "future_trend": "", "url": "u1"},
            {"plain_title": "B", "what_happened": "", "explanation": "", "affected_roles": "", "future_trend": "", "url": "u2"},
        ]
        result = format_digest(articles)
        assert "1." in result
        assert "2." in result


class TestSplitMessage:
    def test_short_message(self):
        result = split_message("short text")
        assert len(result) == 1

    def test_empty_text(self):
        result = split_message("")
        assert result == []

    def test_splits_long_message(self):
        long_text = "---\n".join(["article " * 100] * 5)
        result = split_message(long_text, max_len=500)
        assert len(result) > 1
