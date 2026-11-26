from pydantic import BaseModel

from soc_intel.llm.base import LLMClient
from soc_intel.models.evidence import Evidence


class EvidenceEvaluation(BaseModel):
    sufficient: bool
    reasoning: str
    next_action: str | None = None


def evaluate_evidence(
    evidence: Evidence,
    llm: LLMClient,
) -> EvidenceEvaluation:
    records = evidence.data.get(
        "records",
        []
    )

    record_count = len(records)

    objective = evidence.data.get(
        "objective",
        "Unknown investigation objective",
    )

    expected_evidence = evidence.data.get(
        "expected_evidence",
        [],
    )

    prompt = f"""
You are the evidence-evaluation component of SOC-INTEL,
a cybersecurity investigation platform.

Evaluate whether the CURRENT investigation step produced
enough useful evidence to stop this investigation step.

INVESTIGATION OBJECTIVE

{objective}


EXPECTED EVIDENCE

{expected_evidence}


QUERY RESULT SUMMARY

Records returned:
{record_count}


RULES

1. Do not assume that zero records means the activity is safe.

2. If zero records were returned, normally consider the
   current evidence insufficient.

3. If evidence is insufficient, recommend one concise
   next investigative action.

4. The next action should describe WHAT additional evidence
   should be investigated.

5. Do not generate KQL.

6. Do not invent usernames, IP addresses, hostnames,
   domains, hashes, or other identifiers.

7. Do not make a final incident verdict.

8. Return only the structured response required by the
   EvidenceEvaluation schema.
"""

    return llm.generate_structured(
        prompt=prompt,
        response_model=EvidenceEvaluation,
    )