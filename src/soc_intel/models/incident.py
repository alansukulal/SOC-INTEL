from pydantic import BaseModel,Field
from datetime import datetime,timezone
from soc_intel.models.entity import Entity
from soc_intel.models.enums import IncidentStatus, Severity
from soc_intel.models.alert import Alert


#Incidents structure that we will use 

class Incident(BaseModel):
    incident_id: str
    title: str
    severity:Severity
    status:IncidentStatus=IncidentStatus.NEW
    description:str
    source:str
    created_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))
    entities:list[Entity]=Field(default_factory=list)
    alerts:list[Alert]=Field(default_factory=list)
