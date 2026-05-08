from ai.llm import router
from ai.prompts import impact as impact_prompt


def analyze_impact(article: dict, summary: dict) -> dict:
    system, prompt = impact_prompt.build(
        article["title"], article.get("content", ""), summary.get("人话解释", "")
    )
    resp = router.ask(prompt, system=system)
    return _parse_impact(resp)


def _parse_impact(text: str) -> dict:
    result = {"affected_roles": "", "trend": ""}
    parts = text.split("## ")
    for part in parts:
        part = part.strip()
        if part.startswith("受影响的角色"):
            result["affected_roles"] = part[len("受影响的角色"):].strip()
        elif part.startswith("未来趋势"):
            result["trend"] = part[len("未来趋势"):].strip()
    if not result["affected_roles"] and not result["trend"]:
        result["trend"] = text
    return result
