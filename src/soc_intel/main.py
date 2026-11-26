import os

from soc_intel.auth.environment import EnvironmentCredentialResolver
from soc_intel.config.settings import load_sentinel_config
from soc_intel.ingestion.normalizers.identity import deduplicate_entities
from soc_intel.ingestion.normalizers.sentinel import (
    normalize_alerts,
    normalize_entities,
    normalize_incident,
)
from soc_intel.investigation.engine import run_investigation
from soc_intel.llm.providers.gpt import GPTClient
from soc_intel.tools.siem.providers.sentinel import SentinelProvider
from soc_intel.tools.siem.sentinel import SentinelQueryTool


def main() -> None:

    #1. Load Sentinel configuration and credentials
 
    config = load_sentinel_config()

    resolver = EnvironmentCredentialResolver()

    provider = SentinelProvider(
        config=config,
        credential_resolver=resolver,
    )

    print("SOC-INTEL started")
    print(f"Workspace: {config.workspace_name}")

    # 2. Retrieve incident

    incident_id = "925ec571-841d-4d90-af15-7b55ecba2621"

    raw_incident = provider.get_incident(
        incident_id
    )
    # 3. Retrieve and normalize alerts

    raw_alerts = provider.get_incident_alerts(
        incident_id
    )

    print(
        f"Alerts found: {len(raw_alerts)}"
    )

    normalized_alerts = normalize_alerts(
        raw_alerts
    )

    print(
        "Normalized alerts:",
        len(normalized_alerts),
    )

    # 4. Retrieve and normalize entities

    raw_entities = provider.get_incident_entities(
        incident_id
    )

    print(
        f"Raw entities found: {len(raw_entities)}"
    )

    normalized_entities = normalize_entities(
        raw_entities
    )

    deduplicated_entities = deduplicate_entities(
        normalized_entities
    )

    print(
        "Normalized entities:",
        len(normalized_entities),
    )

    print(
        "Deduplicated entities:",
        len(deduplicated_entities),
    )
  
    # 5. Build vendor-neutral SOC-INTEL Incident
   
    normalized_incident = normalize_incident(
        raw_incident=raw_incident,
        alerts=normalized_alerts,
        entities=deduplicated_entities,
    )

    print("\nNORMALIZED INCIDENT")

    print(
        "Incident ID:",
        normalized_incident.incident_id,
    )

    print(
        "Title:",
        normalized_incident.title,
    )

    print(
        "Severity:",
        normalized_incident.severity,
    )

    print(
        "Status:",
        normalized_incident.status,
    )

    print(
        "Source:",
        normalized_incident.source,
    )

    print(
        "Alerts:",
        len(normalized_incident.alerts),
    )

    print(
        "Entities:",
        len(normalized_incident.entities),
    )

    # 6. Create Sentinel query tool

    query_tool = SentinelQueryTool(
        config=config,
        credential_resolver=resolver,
    )

    # 7. Create OpenAI LLM client

    gpt = GPTClient(
        api_key=os.environ[
            "SOC_INTEL_OPENAI_API_KEY"
        ],
        model="gpt-6-luna",
    )

    # 8. Run SOC-INTEL investigation engine-

    print(
        "\nSTARTING SOC-INTEL INVESTIGATION"
    )

    evidence_items = run_investigation(
        incident=normalized_incident,
        llm=gpt,
        query_tool=query_tool,
    )

    # 9. Display safe investigation summary

    print(
        "\nINVESTIGATION COMPLETE"
    )

    print(
        "Evidence collected:",
        len(evidence_items),
    )

    for index, evidence in enumerate(
        evidence_items,
        start=1,
    ):
        print(
            f"\nEVIDENCE {index}"
        )

        print(
            "Source:",
            evidence.source,
        )

        print(
            "Type:",
            evidence.evidence_type,
        )

        print(
            "Summary:",
            evidence.summary,
        )


if __name__ == "__main__":
    main()