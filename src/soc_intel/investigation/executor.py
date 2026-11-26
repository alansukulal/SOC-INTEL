from uuid import uuid4

from soc_intel.investigation.query_planner import InvestigationQuery
from soc_intel.models.evidence import Evidence
from soc_intel.tools.siem.sentinel import SentinelQueryTool


def _table_to_rows(
    query_result: dict,
) -> list[dict]:
    tables = query_result.get("tables", [])

    if not tables:
        return []

    table = tables[0]

    columns = [
        column["name"]
        for column in table.get("columns", [])
    ]

    rows = table.get("rows", [])

    return [
        dict(zip(columns, row))
        for row in rows
    ]


def execute_investigation_query(
    query: InvestigationQuery,
    query_tool: SentinelQueryTool,
) -> Evidence:
    query_result = query_tool.run_query(
        kql=query.kql,
        timespan=query.timespan,
    )

    rows = _table_to_rows(query_result)

    return Evidence(
        evidence_id=str(uuid4()),
        source="sentinel",
        evidence_type="kql_result",
        summary=(
            f"Investigation query returned "
            f"{len(rows)} records."
        ),
        data={
            "objective": query.objective,
            "expected_evidence": query.expected_evidence,
            "records": rows,
        },
    )