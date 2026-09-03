from datetime import datetime

from pydantic import BaseModel, Field

from soc_intel.models.entity import Entity
from soc_intel.models.enums import Severity

class Alert(BaseModel):
    alert_id: str
    title: str
    description: str
    severity: Severity
    source: str
    product: str
    rule_name: str
    timestamp: datetime
    tactics: list[str] = Field(default_factory=list)
    entities: list[Entity] = Field(default_factory=list)