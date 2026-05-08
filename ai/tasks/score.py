import re

from ai.llm import router
from ai.prompts import score as score_prompt


def score_article(article: dict) -> int:
    system, prompt = score_prompt.build(article["title"], article.get("content", ""))
    resp = router.ask(prompt, system=system)
    m = re.search(r"\d+", resp)
    if not m:
        return 0
    score = int(m.group())
    return min(max(score, 1), 10)
