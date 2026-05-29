import os
import json
from openai import OpenAI

_client = None


def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is not set")
        _client = OpenAI(api_key=api_key)
    return _client


def call_claude(system_prompt, user_prompt, model, max_tokens=1024):
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    raw = response.choices[0].message.content.strip()

    # Strip markdown code fences if the model wraps the JSON
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"OpenAI returned non-JSON response: {raw[:200]}") from e


def call_haiku(system_prompt, user_prompt, max_tokens=1024):
    return call_claude(system_prompt, user_prompt, "gpt-4o-mini", max_tokens)


def call_sonnet(system_prompt, user_prompt, max_tokens=2048):
    return call_claude(system_prompt, user_prompt, "gpt-4o", max_tokens)
