# This will bind the LLM generated data with real customer data.from soc_intel.investigation.llm_context import build_llm_context
from soc_intel.investigation.llm_context import build_llm_context
from soc_intel.investigation.query_planner import InvestigationQuery
from soc_intel.models.incident import Incident
from soc_intel.models.investigation import InvestigationTask


class QueryBindingError(ValueError):
    pass


def _escape_kql_string(
    value: str,
) -> str:
    return value.replace("'", "''")


def bind_query_target(
    query: InvestigationQuery,
    incident: Incident,
    task: InvestigationTask,
) -> InvestigationQuery:
    context = build_llm_context(
        incident=incident,
        task=task,
    )

    placeholder = context.target_placeholder
    target_value = task.target.value

    if not placeholder:
        raise QueryBindingError(
            "Target placeholder cannot be empty."
        )

    if not target_value:
        raise QueryBindingError(
            "Target value cannot be empty."
        )

    if placeholder not in query.kql:
        raise QueryBindingError(
            f"Target placeholder '{placeholder}' "
            "was not found in the generated KQL."
        )

    safe_target_value = _escape_kql_string(
        target_value
    )

    bound_kql = query.kql.replace(
        placeholder,
        safe_target_value,
    )

    if placeholder in bound_kql:
        raise QueryBindingError(
            f"Target placeholder '{placeholder}' "
            "still exists after query binding."
        )

    bound_query = query.model_copy(
        update={
            "kql": bound_kql,
        }
    )

    return bound_query