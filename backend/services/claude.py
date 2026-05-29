"""
Claude API wrapper.
Uses Haiku for fast product scoring, Sonnet for deep product discovery.
"""
import os
import json
import anthropic

_client: anthropic.Anthropic | None = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set")
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


HAIKU_MODEL = os.getenv("CLAUDE_HAIKU_MODEL", "claude-haiku-4-5-20251001")
SONNET_MODEL = os.getenv("CLAUDE_SONNET_MODEL", "claude-sonnet-4-5-20250514")


def call_claude(system_prompt: str, user_prompt: str, model: str, max_tokens: int = 1024) -> dict:
    """
    Call Claude and return parsed JSON from the response.
    Raises ValueError if the response cannot be parsed as JSON.
    """
    client = get_client()
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    raw = message.content[0].text.strip()

    # Strip markdown code fences if Claude wraps the JSON
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Claude returned non-JSON response: {raw[:200]}") from e


def call_haiku(system_prompt: str, user_prompt: str, max_tokens: int = 1024) -> dict:
    return call_claude(system_prompt, user_prompt, HAIKU_MODEL, max_tokens)


def call_sonnet(system_prompt: str, user_prompt: str, max_tokens: int = 2048) -> dict:
    return call_claude(system_prompt, user_prompt, SONNET_MODEL, max_tokens)
