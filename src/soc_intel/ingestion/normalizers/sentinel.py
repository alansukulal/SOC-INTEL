from typing import Any

from soc_intel.models.alert import Alert
from soc_intel.models.entity import Entity, EntityType
from soc_intel.models.enums import IncidentStatus, Severity
from soc_intel.models.incident import Incident


SENTINEL_ENTITY_TYPE_MAP = {
    "account": EntityType.USER,
    "host": EntityType.HOST,
    "ip": EntityType.IP,
    "dns": EntityType.DOMAIN,
    "url": EntityType.URL,
    "filehash": EntityType.FILE_HASH,
    "process": EntityType.PROCESS,
    "mailbox": EntityType.EMAIL,
    "azureresource": EntityType.CLOUD_RESOURCE,
}


def normalize_entity(raw_entity: dict[str, Any]) -> Entity | None:
    kind = raw_entity.get("kind", "").lower()

    entity_type = SENTINEL_ENTITY_TYPE_MAP.get(kind)

    if entity_type is None:
        return None

    properties = raw_entity.get("properties", {})

    value_fields = {
    EntityType.USER: [
        "userPrincipalName",
        "accountName",
        "name",
        "displayName",
        "friendlyName",
        "aadUserId",
        "sid",
        "puid",
        "objectGuid",
    ],

        EntityType.HOST: [
            "azureID",
            "omsAgentID",
            "hostName",
            "netBiosName",
            "friendlyName",
        ],

        EntityType.IP: [
            "address",
            "friendlyName",
        ],

        EntityType.DOMAIN: [
            "domainName",
            "friendlyName",
        ],

        EntityType.URL: [
            "url",
            "friendlyName",
        ],

        EntityType.FILE_HASH: [
            "hashValue",
            "value",
            "friendlyName",
        ],

        EntityType.PROCESS: [
            "processId",
            "commandLine",
            "friendlyName",
        ],

        EntityType.EMAIL: [
            "mailboxPrimaryAddress",
            "upn",
            "externalDirectoryObjectId",
            "displayName",
            "friendlyName",
        ],

        EntityType.CLOUD_RESOURCE: [
            "resourceId",
            "friendlyName",
        ],
    }

    value = ""

    for field in value_fields[entity_type]:
        if properties.get(field):
            value = str(properties[field])
            break

    if not value:
        return None

    attributes = {
        key: str(value)
        for key, value in properties.items()
        if value is not None
    }

    return Entity(
        entity_type=entity_type,
        value=value,
        attributes=attributes,
    )


from typing import Any

def normalize_entities(raw_entities: list[dict[str, Any]],) -> list[Entity]:

    normalized_entities = []

    for raw_entity in raw_entities:
        normalized_entity = normalize_entity(raw_entity)

        if normalized_entity is not None:
            normalized_entities.append(normalized_entity)

    return normalized_entities



def normalize_alert(raw_alert: dict) -> Alert:
    properties = raw_alert.get("properties", {})

    severity_map = {
        "Informational": Severity.INFORMATIONAL,
        "Low": Severity.LOW,
        "Medium": Severity.MEDIUM,
        "High": Severity.HIGH,
    }

    raw_severity = properties.get("severity", "Informational")

    return Alert(
        alert_id=properties.get(
            "systemAlertId",
            raw_alert.get("name", ""),
        ),
        title=properties.get(
            "alertDisplayName",
            properties.get("friendlyName", "Unknown alert"),
        ),
        description=properties.get(
            "description",
            "",
        ),
        severity=severity_map.get(
            raw_severity,
            Severity.INFORMATIONAL,
        ),
        source=properties.get(
            "vendorName",
            "Unknown",
        ),
        product=properties.get(
            "productName",
            "Unknown",
        ),
        rule_name=properties.get(
            "alertType",
            "Unknown",
        ),
        timestamp=properties["timeGenerated"],
        tactics=properties.get(
            "tactics",
            [],
        ),
        entities=[],
    )


def normalize_alerts(raw_alerts: list[dict],) -> list[Alert]:

    normalized_alerts = []

    for raw_alert in raw_alerts:
        normalized_alert = normalize_alert(raw_alert)
        normalized_alerts.append(normalized_alert)

    return normalized_alerts


def normalize_incident(
    raw_incident: dict,
    alerts: list[Alert],
    entities: list[Entity],
) -> Incident:
    properties = raw_incident.get("properties", {})

    severity_map = {
        "Informational": Severity.INFORMATIONAL,
        "Low": Severity.LOW,
        "Medium": Severity.MEDIUM,
        "High": Severity.HIGH,
    }

    status_map = {
        "New": IncidentStatus.NEW,
        "Active": IncidentStatus.INVESTIGATING,
        "Closed": IncidentStatus.CLOSED,
    }

    raw_severity = properties.get("severity", "Informational")
    raw_status = properties.get("status", "New")

    return Incident(
        incident_id=raw_incident.get(
            "name",
            "",
        ),
        title=properties.get(
            "title",
            "Unknown incident",
        ),
        severity=severity_map.get(
            raw_severity,
            Severity.INFORMATIONAL,
        ),
        status=status_map.get(
            raw_status,
            IncidentStatus.NEW,
        ),
        description=properties.get(
            "description",
            "",
        ),
        source=properties.get(
            "providerName",
            "Microsoft Sentinel",
        ),
        created_at=properties["createdTimeUtc"],
        entities=entities,
        alerts=alerts,
    )