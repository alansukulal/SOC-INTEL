from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    evidence_id: str
    source: str
    evidence_type: str
    summary: str
    data: dict = Field(default_factory=dict)
    collected_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )