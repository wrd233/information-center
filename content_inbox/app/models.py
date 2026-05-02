from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator


SuggestedAction = Literal["ignore", "skim", "read", "save", "transcribe", "review"]
FollowupType = Literal["none", "fetch_fulltext", "archive", "transcribe", "manual_review"]
ClusterRelation = Literal[
    "new_event",
    "incremental_update",
    "duplicate",
    "uncertain",
    "embedding_failed",
    "skipped_low_value",
    "disabled",
]
NotificationDecision = Literal["full_push", "incremental_push", "silent", "manual_review"]


class RSSAnalyzeRequest(BaseModel):
    feed_url: str
    source_name: str | None = None
    source_category: str | None = None
    limit: int | None = Field(default=20, ge=1, le=200)
    screen: bool = True


class ContentAnalyzeRequest(BaseModel):
    url: str | None = None
    title: str | None = None
    source_name: str | None = None
    source_category: str | None = None
    content_type: str | None = "unknown"
    summary: str | None = None
    content_text: str | None = None
    published_at: str | None = None
    author: str | None = None
    guid: str | None = None
    screen: bool = True

    @model_validator(mode="after")
    def require_basic_information(self) -> "ContentAnalyzeRequest":
        fields = [self.url, self.title, self.summary, self.content_text]
        if not any(value and value.strip() for value in fields):
            raise ValueError("at least one of url, title, summary, or content_text is required")
        return self


class NormalizedContent(BaseModel):
    title: str
    url: str | None = None
    source_name: str
    source_category: str | None = None
    content_type: str
    published_at: str | None = None
    author: str | None = None
    summary: str | None = None
    content_text: str | None = None
    guid: str | None = None


class ScreeningResult(BaseModel):
    summary: str
    category: str
    value_score: int = Field(ge=1, le=5)
    personal_relevance: int = Field(ge=1, le=5)
    novelty_score: int = Field(default=3, ge=1, le=5)
    source_quality: int = Field(default=3, ge=1, le=5)
    actionability: int = Field(default=3, ge=1, le=5)
    hidden_signals: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    event_hint: str = ""
    suggested_action: SuggestedAction
    followup_type: FollowupType = "none"
    reason: str
    tags: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    screening_method: Literal["ai", "none"] = "none"
    screening_status: Literal["ok", "failed", "skipped"] = "ok"
    prompt_version: str | None = None
    model: str | None = None
    raw_model_response: dict[str, Any] | None = None
    error: str | None = None

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(cls, value: object) -> str:
        if isinstance(value, list):
            return str(value[0]) if value else "其他"
        return str(value or "其他")


class ClusteringResult(BaseModel):
    cluster_id: str | None = None
    cluster_title: str | None = None
    cluster_relation: ClusterRelation = "disabled"
    max_similarity: float | None = None
    entity_overlap_ratio: float | None = None
    notification_decision: NotificationDecision = "manual_review"
    incremental_summary: str = ""
    embedding_text: str | None = None
    embedding_model: str | None = None
    clustering_status: Literal["ok", "failed", "skipped", "disabled"] = "disabled"
    error: str | None = None


class ProcessResult(BaseModel):
    item_id: str
    is_duplicate: bool
    normalized: NormalizedContent
    screening: ScreeningResult
    clustering: ClusteringResult = Field(default_factory=ClusteringResult)
    notification_decision: NotificationDecision = "manual_review"
    cluster_relation: ClusterRelation = "disabled"
    incremental_summary: str = ""
