from __future__ import annotations

from app.models.schemas import RatingAdjustmentRequest
from app.services.source_service import SourceService
from app.storage.repositories import RatingRepository


class RatingService:
    def __init__(self, source_service: SourceService):
        self.source_service = source_service
        self.ratings = RatingRepository(source_service.db)

    def adjust(self, source_id: str, payload: RatingAdjustmentRequest):
        source = self.source_service.sources.get(source_id)
        if not source:
            return None
        old_rating = int(source.get("rating") or 50)
        new_rating = max(0, min(100, old_rating + payload.delta))
        self.ratings.add_adjustment(source_id, old_rating, payload.delta, new_rating, payload.reason, payload.actor)
        updated = self.source_service.sources.update(source_id, {"rating": new_rating})
        return self.source_service.as_response(updated) if updated else None

