from typing import Literal

from pydantic import BaseModel, Field

from soc_intel.investigation.llm_context import build_llm_context
from soc_intel.llm.base import LLMClient
from soc_intel.models.incident import Incident
from soc_intel.models.investigation import InvestigationTask


class InvestigationQuery(BaseModel):
    objective: str

    kql: str

    timespan: Literal[
        "PT1H",
        "PT6H",
        "PT12H",
        "PT24H",
        "P2D",
        "P7D",
    ] = "PT24H"

    expected_evidence: list[str] = Field(
        default_factory=list
    )


def create_investigation_query(
    incident: Incident,
    task: InvestigationTask,
    llm: LLMClient,
    next_action: str | None = None,
    history_summary: str |None=None,
) -> InvestigationQuery:
    context = build_llm_context(
        incident=incident,
        task=task,
    )

    # Extra guidance is added only when the engine
    # is retrying an investigation.
    follow_up_guidance = ""

    if next_action:
        follow_up_guidance = f"""
FOLLOW-UP INVESTIGATION

The previous investigation attempt did not produce
sufficient usable evidence.

Recommended next investigative action:

{next_action}

Generate a DIFFERENT investigation approach that follows
this recommendation.

Do not simply repeat the previous investigation strategy.
Use a simpler or alternative evidence source where appropriate.
"""
    history_guidance = ""

    if history_summary:
        history_guidance = f"""
    PREVIOUS INVESTIGATION HISTORY

    {history_summary}

    Use this history to avoid repeating investigation
    strategies that were already attempted.

    Prefer a materially different evidence source,
    filtering technique, or investigation approach.
    """

    prompt = f"""
You are the query-planning component of SOC-INTEL,
a cybersecurity investigation platform.

Your job is to create ONE focused, read-only KQL query
for the current investigation task.


INCIDENT CONTEXT

Title:
{context.incident_title}

Description:
{context.incident_description}

Severity:
{context.severity}


INVESTIGATION TASK

Action:
{context.action}

Target entity type:
{context.target_type}

Target placeholder:
{context.target_placeholder}


{follow_up_guidance}
{history_guidance}


TARGET RULES

The real target value is intentionally hidden from you.

Whenever the investigation query needs to reference the
target entity, use this exact placeholder:

{context.target_placeholder}

Do not invent or guess a real username, email address,
hostname, IP address, domain, hash, or other identifier.


QUERY RULES

1. Generate exactly one focused KQL investigation query.

2. The KQL must only retrieve or analyze data.

3. Do not create, modify, delete, update, ingest,
   or execute external actions.

4. Base the investigation strategy on the sanitized
   incident context and investigation task.

5. Use the exact target placeholder whenever the target
   entity needs to appear in the query.

6. Choose a security data source appropriate for the
   incident behavior and entity type.

7. Keep the query reasonably scoped.

8. Limit returned records where appropriate.

9. Choose exactly one timespan supported by the
   InvestigationQuery schema.

10. Describe the specific investigation objective.

11. Describe what evidence the query should collect.

12. Return only the structured response required by
    the InvestigationQuery schema.

13. When using summarize, distinct, join, or grouping
    operations, do not directly group by dynamic-type
    columns. Extract or cast dynamic values to an
    appropriate scalar type first.

14. Do not assume that optional, derived, renamed,
    or custom columns exist. Prefer standard fields
    required for the investigation when possible.

15. Prefer simple, reliable KQL over unnecessarily
    complex queries.

16. If this is a follow-up investigation, change the
    evidence source, investigation technique, filtering
    approach, or query strategy rather than repeating
    the previous approach.
"""

    return llm.generate_structured(
        prompt=prompt,
        response_model=InvestigationQuery,
    )