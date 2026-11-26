# This act as a guardrail for the generated KQL
from soc_intel.investigation.query_planner import InvestigationQuery


class QueryValidationError(ValueError):
    pass


def validate_investigation_query(
    query: InvestigationQuery,
) -> InvestigationQuery:
    kql = query.kql.strip()

    if not kql:
        raise QueryValidationError(
            "KQL query cannot be empty."
        )

    blocked_terms = [
        ".create",
        ".alter",
        ".drop",
        ".delete",
        ".set",
        ".append",
        ".ingest",
        ".execute",
    ]

    lowered_kql = kql.lower()

    for term in blocked_terms:
        if term in lowered_kql:
            raise QueryValidationError(
                f"Blocked KQL operation detected: {term}"
            )

    if len(kql) > 10000:
        raise QueryValidationError(
            "KQL query is too large."
        )

    return query