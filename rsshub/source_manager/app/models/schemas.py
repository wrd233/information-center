from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator


SourceType = Literal["rsshub", "wechat", "native"]
SourceStatus = Literal["active", "paused", "broken", "disabled"]
CheckStatus = Literal["ok", "failed"]
RatingReason = Literal[
    "manual_adjustment",
    "useful_discovery",
    "duplicate_noise",
    "low_value_content",
    "fetch_unstable",
    "recovered_quality",
]
ImportStrategy = Literal["skip", "fill_empty", "overwrite_metadata", "overwrite_all"]


class SourceBase(BaseModel):
    source_type: SourceType
    display_name: str = Field(min_length=1)
    status: SourceStatus | None = None
    category: str | None = None
    tags: list[str] = Field(default_factory=list)
    rating: int = Field(default=50, ge=0, le=100)
    notes: str | None = None
    adapter_id: str | None = None
    route_path: str | None = None
    feed_url: str | None = None
    original_feed_url: str | None = None
    wechat_identity: dict[str, Any] = Field(default_factory=dict)

    @field_validator("category", mode="before")
    @classmethod
    def default_category(cls, value: object) -> str:
        text = str(value).strip() if value is not None else ""
        return text or "未分类"

    @field_validator("rating", mode="before")
    @classmethod
    def clamp_rating(cls, value: object) -> int:
        try:
            number = int(value)
        except (TypeError, ValueError):
            number = 50
        return max(0, min(100, number))


class SourceCreate(SourceBase):
    source_id: str | None = None
    allow_duplicate: bool = False
    check_before_save: bool = False

    @model_validator(mode="after")
    def require_identity(self) -> "SourceCreate":
        if self.source_type == "rsshub" and not self.route_path:
            raise ValueError("rsshub source requires route_path")
        if self.source_type == "native" and not self.feed_url:
            raise ValueError("native source requires feed_url")
        if self.source_type == "wechat" and not (self.feed_url or self.wechat_identity):
            raise ValueError("wechat source requires feed_url or wechat_identity")
        return self


class SourceUpdate(BaseModel):
    display_name: str | None = None
    status: SourceStatus | None = None
    category: str | None = None
    tags: list[str] | None = None
    rating: int | None = Field(default=None, ge=0, le=100)
    notes: str | None = None
    adapter_id: str | None = None
    route_path: str | None = None
    feed_url: str | None = None
    original_feed_url: str | None = None
    wechat_identity: dict[str, Any] | None = None
    allow_duplicate: bool = False


class SourceResponse(BaseModel):
    source_id: str
    source_type: SourceType
    display_name: str
    status: SourceStatus
    category: str
    tags: list[str] = Field(default_factory=list)
    rating: int
    notes: str | None = None
    adapter_id: str | None = None
    route_path: str | None = None
    feed_url: str | None = None
    original_feed_url: str | None = None
    resolved_feed_url: str | None = None
    wechat_identity: dict[str, Any] = Field(default_factory=dict)
    last_checked_at: str | None = None
    last_check_status: str | None = None
    last_check_error: str | None = None
    last_success_at: str | None = None
    last_failure_at: str | None = None
    consecutive_failures: int = 0
    last_error: str | None = None
    total_entries_seen: int = 0
    last_fetch_new_count: int = 0
    last_fetch_existing_count: int = 0
    last_fetch_scanned_count: int = 0
    created_at: str | None = None
    updated_at: str | None = None
    disabled_at: str | None = None


class SourceListResponse(BaseModel):
    ok: bool = True
    sources: list[SourceResponse]
    total: int
    stats: dict[str, Any]


class BatchUpdateRequest(BaseModel):
    source_ids: list[str]
    category: str | None = None
    tags: list[str] | None = None
    rating: int | None = Field(default=None, ge=0, le=100)
    status: SourceStatus | None = None


class RatingAdjustmentRequest(BaseModel):
    delta: int
    reason: RatingReason
    actor: str = "local"


class CheckResult(BaseModel):
    ok: bool
    feed_url: str
    status: CheckStatus
    entry_count: int = 0
    error: str | None = None
    checked_at: str


class FetchRequest(BaseModel):
    include_raw: bool = False


class BatchRunRequest(BaseModel):
    source_ids: list[str] | None = None
    statuses: list[SourceStatus] | None = None
    include_paused: bool = False
    include_broken: bool = False
    max_concurrent_sources: int | None = None
    include_raw: bool = False


class EntryResponse(BaseModel):
    entry_id: str
    source_id: str
    guid: str | None = None
    url: str | None = None
    normalized_url: str | None = None
    identity_key: str
    title: str | None = None
    published_at: str | None = None
    first_seen_at: str | None = None
    last_seen_at: str | None = None
    seen_count: int = 1
    summary_excerpt: str | None = None


class FetchRunResponse(BaseModel):
    fetch_run_id: str
    source_id: str
    status: str
    started_at: str | None = None
    finished_at: str | None = None
    fetched_count: int = 0
    scanned_count: int = 0
    new_count: int = 0
    existing_count: int = 0
    stopped_reason: str | None = None
    error_message: str | None = None
    include_raw: bool = False


class SourceDetailResponse(BaseModel):
    ok: bool = True
    source: SourceResponse
    recent_entries: list[EntryResponse]
    recent_fetch_runs: list[FetchRunResponse]


class ImportPreviewRequest(BaseModel):
    content: str
    filename: str | None = None


class ImportCommitRequest(BaseModel):
    content: str
    filename: str | None = None
    strategy: ImportStrategy = "skip"


class ImportPreviewResponse(BaseModel):
    ok: bool = True
    import_type: Literal["csv", "opml"]
    filename: str | None = None
    summary: dict[str, int]
    items: list[dict[str, Any]]


class ImportCommitResponse(BaseModel):
    ok: bool = True
    import_run_id: str
    summary: dict[str, int]
    created_source_ids: list[str] = Field(default_factory=list)
