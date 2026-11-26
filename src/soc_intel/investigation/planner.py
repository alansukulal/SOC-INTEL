from soc_intel.investigation.targets import get_investigation_targets
from soc_intel.models.incident import Incident
from soc_intel.models.investigation import InvestigationTask


def create_investigation_plan(incident: Incident) -> list[InvestigationTask]:
    targets = get_investigation_targets(incident)

    tasks: list[InvestigationTask] = []

    for entity in targets:
        entity_type = entity.entity_type.value

        if entity_type == "host":
            action = "investigate_host"

        elif entity_type == "user":
            action = "investigate_user"

        elif entity_type == "ip":
            action = "investigate_ip"

        else:
            action = "investigate_entity"

        task = InvestigationTask(
            target=entity,
            action=action,
        )

        tasks.append(task)

    return tasks