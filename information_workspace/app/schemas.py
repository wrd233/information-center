from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


SOURCE_TYPES = {"rss", "web", "wechat", "upload", "document", "agent", "api", "unknown"}
CONTENT_FACETS = {"news", "article", "opinion", "technical", "noise", "uncertain"}
RUN_STEPS = [
    "validate_input",
    "dedupe_compress",
    "persist_materials",
    "light_understanding",
    "similarity_marking",
    "candidate_events",
    "active_event_matching",
    "finalize_run",
]


class MaterialUpload(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: str
    content_text: str
    source_name: str
    source_type: str
    external_id: str | None = None
    source_url: str | None = None
    url: str | None = None
    author: str | None = None
    published_at: str | None = None
    fetched_at: str | None = None
    language: str | None = None
    content_html: str | None = None
    summary_from_source: str | None = None
    tags_from_source: list[str] = Field(default_factory=list)
    upstream_score: float | None = None
    upstream_reason: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    raw_payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("title", "content_text", "source_name")
    @classmethod
    def required_text(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("must be a non-empty string")
        return value.strip()

    @field_validator("source_type")
    @classmethod
    def valid_source_type(cls, value: str) -> str:
        if value not in SOURCE_TYPES:
            raise ValueError(f"source_type must be one of {sorted(SOURCE_TYPES)}")
        return value


class SingleUploadRequest(MaterialUpload):
    auto_process: bool = False


class BatchUploadRequest(BaseModel):
    items: list[dict[str, Any]]
    auto_process: bool = False
    source: str = "batch_upload"


class UploadResponse(BaseModel):
    run_id: str
    item_count: int
    accepted_count: int
    failed_count: int
    status: str


class RunProcessResponse(BaseModel):
    run_id: str
    status: str
    material_ids: list[str]
    candidate_event_ids: list[str]
    failed_steps: list[str]


class MaterialSearchResponse(BaseModel):
    items: list[dict[str, Any]]
    total: int


class EventFromMaterialsRequest(BaseModel):
    material_ids: list[str]
    title: str | None = None
    user_focus: str | None = None


class TopicCreateRequest(BaseModel):
    title: str
    goal: str
    organization: str = ""
    material_ids: list[str] = Field(default_factory=list)
    event_ids: list[str] = Field(default_factory=list)


class TopicAddMaterialsRequest(BaseModel):
    material_ids: list[str] = Field(default_factory=list)
    event_ids: list[str] = Field(default_factory=list)


class TopicRefreshRequest(BaseModel):
    include_new_materials: bool = True
    allow_mock_llm: bool = False


class TopicLocalRefreshRequest(BaseModel):
    node_id: str
    instruction: str
    include_new_materials: bool = True
    allow_mock_llm: bool = False


class ExportMaterialRequest(BaseModel):
    material_ids: list[str]


class PromptEvalRequest(BaseModel):
    task: Literal["light_understanding", "event_candidate", "topic_structure"]
    material_ids: list[str] = Field(default_factory=list)
    run_id: str | None = None
    fixture_file: str | None = None
    fixture_group: str | None = None
    test_purpose: str | None = None
    limit: int | None = None
    allow_mock_llm: bool = False
