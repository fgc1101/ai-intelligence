import litellm

from configs.settings import LLM_MODEL, LLM_TEMPERATURE


def ask(prompt: str, system: str = "", model: str = "", temperature: float = -1) -> str:
    model = model or LLM_MODEL
    temperature = temperature if temperature >= 0 else LLM_TEMPERATURE

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    resp = litellm.completion(model=model, messages=messages, temperature=temperature)
    return resp.choices[0].message.content
