from __future__ import annotations

import secrets
import string


ALPHABET = string.ascii_lowercase + string.digits


def short_id(prefix: str, length: int = 12) -> str:
    return prefix + "".join(secrets.choice(ALPHABET) for _ in range(length))


def new_source_id() -> str:
    return short_id("src_")


def new_entry_id() -> str:
    return short_id("ent_")


def new_fetch_run_id() -> str:
    return short_id("fr_")


def new_import_run_id() -> str:
    return short_id("imp_")

