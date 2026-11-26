from soc_intel.ingestion.loader import load_incident


def test_load_valid_incident():
    incident = load_incident("data/samples/incident_001.json")

    assert incident.incident_id == "INC-001"
    assert incident.severity.value == "high"
    assert incident.status.value == "new"

    assert len(incident.alerts) == 1
    assert incident.alerts[0].alert_id == "ALT-001"

    assert len(incident.entities) == 3
    assert incident.entities[0].entity_type.value == "host"
    assert incident.entities[0].value == "WIN-WS01"


