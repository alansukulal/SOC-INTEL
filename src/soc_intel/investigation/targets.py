from soc_intel.models.entity import Entity
from soc_intel.models.incident import Incident


def get_investigation_targets(incident: Incident) -> list[Entity]:
    targets = list(incident.entities)

    for alert in incident.alerts:
        targets.extend(alert.entities)

    unique_targets: dict[tuple[str, str], Entity] = {}

    for entity in targets:
        key = (entity.entity_type.value, entity.value)
        unique_targets.setdefault(key, entity)

    return list(unique_targets.values())