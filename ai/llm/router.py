import os

import litellm

from configs.settings import LLM_MODEL, LLM_TEMPERATURE

# LiteLLM model prefix -> env var name
_KEY_MAP = {
    "volcengine/": "VOLCENGINE_API_KEY",
    "openai/": "OPENAI_API_KEY",
    "anthropic/": "ANTHROPIC_API_KEY",
}


def _resolve_api_key(model: str) -> str | None:
    for prefix, env_var in _KEY_MAP.items():
        if model.startswith(prefix):
            return os.getenv(env_var)
    return None


def ask(prompt: str, system: str = "", model: str = "", temperature: float = -1) -> str:
    model = model or LLM_MODEL
    temperature = temperature if temperature >= 0 else LLM_TEMPERATURE

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    api_key = _resolve_api_key(model)
    kwargs = {"model": model, "messages": messages, "temperature": temperature}
    if api_key:
        kwargs["api_key"] = api_key

    resp = litellm.completion(**kwargs)
    return resp.choices[0].message.content
