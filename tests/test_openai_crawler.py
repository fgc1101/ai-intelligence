from pathlib import Path

from sources.official.openai.crawler import OpenAICrawler

FIXTURE = str(Path(__file__).resolve().parent / "fixtures" / "openai_rss_sample.xml")


class TestOpenAICrawler:
    def setup_method(self):
        self.crawler = OpenAICrawler(rss_url=FIXTURE)

    def test_fetch_returns_entries(self):
        raw_items = self.crawler.fetch()
        assert len(raw_items) == 6

    def test_parse_first_article(self):
        raw_items = self.crawler.fetch()
        article = self.crawler.parse(raw_items[0])
        assert article.source == "openai"
        assert "GPT-5.5" in article.title
        assert article.url.startswith("https://openai.com/")
        assert article.category == "Security"
        assert article.published_at is not None
        assert article.published_at.year == 2026
        assert article.published_at.month == 5

    def test_parse_category_product(self):
        raw_items = self.crawler.fetch()
        article = self.crawler.parse(raw_items[1])
        assert article.title == "Introducing GPT-5.5"
        assert article.category == "Product"

    def test_to_dict_roundtrip(self):
        raw_items = self.crawler.fetch()
        article = self.crawler.parse(raw_items[0])
        d = article.to_dict()
        assert d["source"] == "openai"
        assert d["published_at"] is not None
