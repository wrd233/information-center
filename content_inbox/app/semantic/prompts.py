from __future__ import annotations

from pathlib import Path

from app.config import BASE_DIR


PROMPT_DIR = BASE_DIR / "prompts"


def load_prompt(prompt_version: str) -> str:
    path = PROMPT_DIR / f"{prompt_version}.md"
    if not path.exists():
        raise RuntimeError(f"missing semantic prompt: {path}")
    return path.read_text(encoding="utf-8")


def build_messages(prompt_version: str, input_json: str, repair_error: str | None = None) -> list[dict[str, str]]:
    prompt = load_prompt(prompt_version)
    suffix = ""
    if repair_error:
        suffix = (
            "\n\nPrevious output failed JSON validation. Return only corrected JSON. "
            f"Validation error: {repair_error}"
        )
    return [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Input JSON:\n{input_json}{suffix}"},
    ]
