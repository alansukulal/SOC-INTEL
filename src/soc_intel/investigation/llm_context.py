import re

from pydantic import BaseModel

from soc_intel.models.incident import Incident
from soc_intel.models.investigation import InvestigationTask


class LLMInvestigationContext(BaseModel):
    incident_title: str
    incident_description: str
    severity: str
    action: str
    target_type: str
    target_placeholder: str


def _sanitize_text(
    text: str,
    target_value: str,
    target_placeholder: str,
) -> str:
    sanitized = text

    # Replace the known investigation target.
    if target_value:
        sanitized = sanitized.replace(
            target_value,
            target_placeholder,
        )

    # Redact email addresses.
    sanitized = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "EMAIL_REDACTED",
        sanitized,
    )

    # Redact IPv4 addresses.
    sanitized = re.sub(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "IP_REDACTED",
        sanitized,
    )

    # Remove URLs.
    sanitized = re.sub(
        r"https?://\S+",
        "URL_REDACTED",
        sanitized,
    )

    return sanitized


def build_llm_context(
    incident: Incident,
    task: InvestigationTask,
) -> LLMInvestigationContext:
    target_type = task.target.entity_type.value

    target_placeholder = (
        f"{target_type.upper()}_TARGET"
    )

    target_value = task.target.value

    sanitized_title = _sanitize_text(
        text=incident.title,
        target_value=target_value,
        target_placeholder=target_placeholder,
    )

    sanitized_description = _sanitize_text(
        text=incident.description,
        target_value=target_value,
        target_placeholder=target_placeholder,
    )

    return LLMInvestigationContext(
        incident_title=sanitized_title,
        incident_description=sanitized_description,
        severity=incident.severity.value,
        action=task.action,
        target_type=target_type,
        target_placeholder=target_placeholder,
    )