from pydantic import BaseModel,Field
from soc_intel.models.customer import CustomerSecurityProfile
from soc_intel.models.evidence import Evidence
from soc_intel.models.incident import Incident
from soc_intel.models.entity import Entity

class InvestigationContext(BaseModel):
    incident: Incident
    findings: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)


class InvestigationTask(BaseModel):
    target:Entity
    action:str


class InvestigationSession(BaseModel):
    customer: CustomerSecurityProfile
    context: InvestigationContext
    tasks: list[InvestigationTask] = Field(default_factory=list)