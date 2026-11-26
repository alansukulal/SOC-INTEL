from abc import ABC, abstractmethod
from typing import Any

#This is the rule for all siems to follow:All onboarding siems should give the following details.

class SIEMProvider(ABC):

    @abstractmethod
    def get_incident(
        self,
        incident_id: str,
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_incident_alerts(
        self,
        incident_id: str,
    ) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def get_incident_entities(
        self,
        incident_id: str,
    ) -> list[dict[str, Any]]:
        pass