from ai.llm import router
from ai.prompts import summarize as summarize_prompt

SECTIONS = ["人话标题", "发生了什么", "人话解释", "影响人群", "未来趋势"]


def summarize_article(article: dict) -> dict:
    system, prompt = summarize_prompt.build(article["title"], article.get("content", ""))
    resp = router.ask(prompt, system=system)
    return _parse_sections(resp)


def _parse_sections(text: str) -> dict:
    result = {key: "" for key in SECTIONS}
    parts = text.split("## ")
    for part in parts:
        part = part.strip()
        for key in SECTIONS:
            if part.startswith(key):
                result[key] = part[len(key):].strip()
                break
    if not any(result.values()):
        result["人话解释"] = text
    return result
