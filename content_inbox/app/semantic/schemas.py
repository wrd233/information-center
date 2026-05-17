from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

from app.semantic.cluster_policy import cluster_relation_action as policy_cluster_relation_action
from app.semantic.relation_policy import should_fold as policy_should_fold


SCHEMA_VERSION = "semantic_v1"
ITEM_CARD_PROMPT_VERSION = "item_card_v1"
ITEM_RELATION_PROMPT_VERSION = "item_relation_v3"
ITEM_CLUSTER_PROMPT_VERSION = "item_cluster_relation_v3"
CLUSTER_CARD_PROMPT_VERSION = "cluster_card_patch_v1"
SOURCE_REVIEW_PROMPT_VERSION = "source_review_v1"

ItemRelationPrimary = Literal[
    "duplicate",
    "near_duplicate",
    "related_with_new_info",
    "same_product_different_event",
    "same_thread",
    "different",
    "uncertain",
]
ItemRelationRole = Literal[
    "same_url",
    "same_guid",
    "same_canonical_url",
    "same_content_hash",
    "same_title_hash",
    "translation",
    "rewrite",
    "summary_of",
    "syndicated_copy",
    "cross_language",
    "same_product",
    "same_actor",
    "same_event_signature",
    "same_announcement",
    "same_event_hint",
    "new_fact_hint",
    "new_analysis_hint",
    "firsthand_hint",
    "source_material",
    "source_material_hint",
    "availability_detail",
    "pricing_detail",
    "benchmark_detail",
    "case_study",
    "same_product_different_event",
    "same_thread",
    "same_conference",
    "same_template",
    "generic_topic_overlap",
    "weak_context",
]
ItemClusterPrimary = Literal[
    "source_material",
    "repeat",
    "new_info",
    "analysis",
    "experience",
    "context",
    "follow_up",
    "same_topic",
    "unrelated",
    "uncertain",
]
ItemClusterRole = Literal[
    "official",
    "paper",
    "github_release",
    "changelog",
    "data_source",
    "media_report",
    "commentary",
    "background",
    "benchmark",
    "hands_on",
    "user_feedback",
    "contrarian_view",
    "risk_signal",
    "market_impact",
    "technical_detail",
    "business_impact",
    "source_discovery",
    "citation_hub",
    "same_product_different_event",
    "same_thread",
    "same_conference",
    "same_template",
    "generic_topic_overlap",
    "weak_context",
]
ContentRole = Literal[
    "source_material",
    "report",
    "analysis",
    "firsthand",
    "commentary",
    "aggregator",
    "low_signal",
    "unknown",
]
ClusterStatus = Literal["active", "cooling", "archived", "reopened", "merged"]
SourcePriority = Literal["new_source_under_evaluation", "high", "normal", "low", "disabled_for_llm"]


class ItemCardData(BaseModel):
    item_id: str
    canonical_title: str
    language: str = "unknown"
    short_summary: str
    embedding_text: str
    entities: list[str] = Field(default_factory=list)
    event_hint: str | None = None
    content_role: ContentRole = "unknown"
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    warnings: list[str] = Field(default_factory=list)
    key_facts: list[str] = Field(default_factory=list)
    key_opinions: list[str] = Field(default_factory=list)
    cited_sources: list[str] = Field(default_factory=list)
    source_material_candidates: list[str] = Field(default_factory=list)
    quality_hints: dict[str, Any] = Field(default_factory=dict)

    @field_validator("canonical_title", "short_summary", "embedding_text", mode="before")
    @classmethod
    def require_non_empty(cls, value: object) -> str:
        text = str(value or "").strip()
        if not text:
            raise ValueError("field must be non-empty")
        return text


class ItemCardBatchOutput(BaseModel):
    item_cards: list[ItemCardData]


class ItemRelationDecision(BaseModel):
    candidate_item_id: str
    primary_relation: ItemRelationPrimary
    secondary_roles: list[ItemRelationRole] = Field(default_factory=list)
    canonical_item_id: str | None = None
    new_information: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    reason: str = ""
    reason_code: str = ""
    evidence: list[str] = Field(default_factory=list)
    event_relation_type: str = "different"
    cluster_eligible: bool = False
    same_event: bool = False
    same_product: bool = False
    same_thread: bool = False
    should_fold: bool = False
    same_event_evidence: list[str] = Field(default_factory=list)
    new_info_evidence: list[str] = Field(default_factory=list)
    disqualifiers: list[str] = Field(default_factory=list)
    shared_entities: list[str] = Field(default_factory=list)
    boilerplate_detected: bool = False
    generic_entity_overlap: bool = False


class ItemRelationOutput(BaseModel):
    new_item_id: str
    relations: list[ItemRelationDecision]


class ItemClusterDecision(BaseModel):
    cluster_id: str | None = None
    primary_relation: ItemClusterPrimary
    secondary_roles: list[ItemClusterRole] = Field(default_factory=list)
    same_event: bool = False
    same_topic: bool = False
    follow_up_event: bool = False
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    incremental_value: int = Field(default=0, ge=0, le=5)
    report_value: int = Field(default=0, ge=0, le=5)
    should_update_cluster_card: bool = False
    should_notify: bool = False
    new_facts: list[str] = Field(default_factory=list)
    new_angles: list[str] = Field(default_factory=list)
    reason: str = ""
    reason_code: str = ""
    evidence: list[str] = Field(default_factory=list)
    cluster_relation_type: str = "uncertain"
    attach_eligible: bool = False
    attach_disqualifiers: list[str] = Field(default_factory=list)


class ItemClusterOutput(BaseModel):
    item_id: str
    best_relation: ItemClusterDecision


class ClusterCardData(BaseModel):
    cluster_id: str
    cluster_title: str
    event_type: str | None = None
    main_entities: list[str] = Field(default_factory=list)
    core_facts: list[str] = Field(default_factory=list)
    known_angles: list[str] = Field(default_factory=list)
    representative_items: list[str] = Field(default_factory=list)
    source_items: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    first_seen_at: str | None = None
    last_major_update_at: str | None = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class SourceReviewOutput(BaseModel):
    source_id: str
    priority_suggestion: SourcePriority
    reason: str
    evidence: list[str] = Field(default_factory=list)


def item_relation_should_fold(primary_relation: str) -> bool:
    return policy_should_fold(primary_relation)


def cluster_relation_action(primary_relation: str) -> str:
    return policy_cluster_relation_action(primary_relation)
