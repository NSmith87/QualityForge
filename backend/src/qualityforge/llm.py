from __future__ import annotations

import httpx

from qualityforge.settings import Settings

SYSTEM_PROMPT = (
    "You are QualityForge, an AI QA engineer. Analyze requirements, propose test "
    "strategy, and prefer user-facing Playwright locators (getByRole, getByLabel)."
)


class LLMError(RuntimeError):
    pass


def configured_model(settings: Settings) -> str:
    if settings.llm_provider == "openai":
        return settings.openai_model
    if settings.llm_provider == "anthropic":
        return settings.anthropic_model
    if settings.llm_provider == "azure_openai":
        return settings.azure_openai_deployment or settings.llm_model
    return settings.llm_model


def complete(settings: Settings, prompt: str) -> str:
    """Call the configured provider. Local default is Ollama (Mistral/Llama)."""
    provider = settings.llm_provider
    if provider == "ollama":
        return _ollama(settings, prompt)
    if provider == "openai":
        return _openai(settings, prompt)
    if provider == "anthropic":
        return _anthropic(settings, prompt)
    if provider == "azure_openai":
        return _azure_openai(settings, prompt)
    raise LLMError(f"Unsupported LLM provider: {provider}")


def try_complete(settings: Settings, prompt: str) -> str | None:
    try:
        return complete(settings, prompt)
    except (LLMError, httpx.HTTPError, OSError):
        return None


def _ollama(settings: Settings, prompt: str) -> str:
    url = f"{settings.ollama_base_url.rstrip('/')}/api/chat"
    payload = {
        "model": settings.llm_model,
        "stream": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    }
    with httpx.Client(timeout=60) as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        message = response.json().get("message") or {}
        content = message.get("content")
        if not content:
            raise LLMError("Ollama returned an empty response")
        return str(content)


def _openai(settings: Settings, prompt: str) -> str:
    if not settings.openai_api_key:
        raise LLMError("OPENAI_API_KEY is not set")
    headers = {"Authorization": f"Bearer {settings.openai_api_key}"}
    payload = {
        "model": settings.openai_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    }
    with httpx.Client(timeout=60) as client:
        response = client.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        return str(response.json()["choices"][0]["message"]["content"])


def _anthropic(settings: Settings, prompt: str) -> str:
    if not settings.anthropic_api_key:
        raise LLMError("ANTHROPIC_API_KEY is not set")
    headers = {
        "x-api-key": settings.anthropic_api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": settings.anthropic_model,
        "max_tokens": 1024,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": prompt}],
    }
    with httpx.Client(timeout=60) as client:
        response = client.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        blocks = response.json().get("content") or []
        text = "".join(block.get("text", "") for block in blocks if block.get("type") == "text")
        if not text:
            raise LLMError("Anthropic returned an empty response")
        return text


def _azure_openai(settings: Settings, prompt: str) -> str:
    if not settings.azure_openai_api_key or not settings.azure_openai_endpoint:
        raise LLMError("AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT are required")
    if not settings.azure_openai_deployment:
        raise LLMError("AZURE_OPENAI_DEPLOYMENT is not set")
    endpoint = settings.azure_openai_endpoint.rstrip("/")
    url = (
        f"{endpoint}/openai/deployments/{settings.azure_openai_deployment}"
        f"/chat/completions?api-version={settings.azure_openai_api_version}"
    )
    headers = {"api-key": settings.azure_openai_api_key}
    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
    }
    with httpx.Client(timeout=60) as client:
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return str(response.json()["choices"][0]["message"]["content"])
