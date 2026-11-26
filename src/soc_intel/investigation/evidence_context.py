import re
from typing import Any

from pydantic import BaseModel, Field

from soc_intel.models.evidence import Evidence


MAX_EVIDENCE_RECORDS = 20


class EvidenceContext(BaseModel):
    record_count: int
    fields_observed: list[str] = Field(
        default_factory=list
    )
    records: list[dict[str, Any]] = Field(
        default_factory=list
    )


def _sanitize_string(value: str) -> str:
    sanitized = value

    # Email addresses
    sanitized = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "EMAIL_REDACTED",
        sanitized,
    )

    # IPv4 addresses
    sanitized = re.sub(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "IP_REDACTED",
        sanitized,
    )

    # URLs
    sanitized = re.sub(
        r"https?://\S+",
        "URL_REDACTED",
        sanitized,
    )

    return sanitized


def _sanitize_value(
    value: Any,
) -> Any:
    if isinstance(value, str):
        return _sanitize_string(value)

    if isinstance(value, dict):
        return {
            key: _sanitize_value(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            _sanitize_value(item)
            for item in value
        ]

    return value


def build_evidence_context(
    evidence: Evidence,
) -> EvidenceContext:
    raw_records = evidence.data.get(
        "records",
        [],
    )

    if not isinstance(raw_records, list):
        raw_records = []

    record_count = len(raw_records)

    limited_records = raw_records[
        :MAX_EVIDENCE_RECORDS
    ]

    sanitized_records: list[
        dict[str, Any]
    ] = []

    fields_observed: set[str] = set()

    for record in limited_records:
        if not isinstance(record, dict):
            continue

        fields_observed.update(
            record.keys()
        )

        sanitized_record = {
            key: _sanitize_value(value)
            for key, value in record.items()
        }

        sanitized_records.append(
            sanitized_record
        )

    return EvidenceContext(
        record_count=record_count,
        fields_observed=sorted(
            fields_observed
        ),
        records=sanitized_records,
    )