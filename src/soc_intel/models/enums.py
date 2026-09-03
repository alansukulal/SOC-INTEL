from enum import Enum

#enum is for defining fixed values and this is for both alert and incidents
class Severity(str, Enum):
    INFORMATIONAL = "informational"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(str, Enum):
    NEW = "new"
    INVESTIGATING = "investigating"
    ESCALATED = "escalated"
    CLOSED = "closed"