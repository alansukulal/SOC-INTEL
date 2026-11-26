from soc_intel.investigation.evaluator import evaluate_evidence
from soc_intel.investigation.executor import (
    execute_investigation_query,
)
from soc_intel.investigation.planner import (
    create_investigation_plan,
)
from soc_intel.investigation.query_binding import (
    bind_query_target,
)
from soc_intel.investigation.query_planner import (
    create_investigation_query,
)
from soc_intel.investigation.query_validator import (
    validate_investigation_query,
)
from soc_intel.investigation.investigation_state import (
    InvestigationAttempt,
    InvestigationState,
)
from soc_intel.llm.base import LLMClient
from soc_intel.models.evidence import Evidence
from soc_intel.models.incident import Incident
from soc_intel.tools.siem.sentinel import SentinelQueryTool


MAX_INVESTIGATION_ATTEMPTS = 3


def run_investigation(
    incident: Incident,
    llm: LLMClient,
    query_tool: SentinelQueryTool,
) -> list[Evidence]:
    tasks = create_investigation_plan(
        incident
    )

    all_evidence: list[Evidence] = []

    for task in tasks:
        state = InvestigationState()

        next_action: str | None = None

        for attempt_number in range(
            1,
            MAX_INVESTIGATION_ATTEMPTS + 1,
        ):
            print(
                f"\nInvestigation attempt "
                f"{attempt_number}/"
                f"{MAX_INVESTIGATION_ATTEMPTS}"
            )

            # ---------------------------------------------
            # Build safe memory of previous attempts
            # ---------------------------------------------

            history_summary = (
                state.get_history_summary()
            )

            query = None

            try:
                # -----------------------------------------
                # GPT creates investigation query
                # using previous investigation history
                # -----------------------------------------

                query = create_investigation_query(
                    incident=incident,
                    task=task,
                    llm=llm,
                    next_action=next_action,
                    history_summary=history_summary,
                )

                # -----------------------------------------
                # Validate GPT-generated placeholder KQL
                # -----------------------------------------

                validated_query = (
                    validate_investigation_query(
                        query
                    )
                )

                # -----------------------------------------
                # Bind real target locally
                # -----------------------------------------

                bound_query = bind_query_target(
                    query=validated_query,
                    incident=incident,
                    task=task,
                )

                # -----------------------------------------
                # Validate final executable KQL
                # -----------------------------------------

                final_query = (
                    validate_investigation_query(
                        bound_query
                    )
                )

                # -----------------------------------------
                # Execute against Sentinel
                # -----------------------------------------

                collected_evidence = (
                    execute_investigation_query(
                        query=final_query,
                        query_tool=query_tool,
                    )
                )

            except RuntimeError:
                print(
                    "Query execution failed. "
                    "SOC-INTEL will try another "
                    "investigation approach."
                )

                next_action = (
                    "The previous query could not be "
                    "executed. Use a simpler or alternative "
                    "investigation strategy. Avoid relying "
                    "on optional, derived, renamed, custom, "
                    "or unsupported schema fields."
                )

                # -----------------------------------------
                # Remember failed attempt
                # -----------------------------------------

                if query is not None:
                    failed_attempt = InvestigationAttempt(
                        attempt_number=attempt_number,
                        objective=query.objective,
                        kql_strategy=query.kql,
                        record_count=0,
                        successful=False,
                        failure_reason=(
                            "Query execution failed."
                        ),
                        evaluation=(
                            "No evidence was collected "
                            "because the query failed."
                        ),
                        next_action=next_action,
                    )

                    state.add_attempt(
                        failed_attempt
                    )

                continue

            # ---------------------------------------------
            # Store successful evidence
            # ---------------------------------------------

            all_evidence.append(
                collected_evidence
            )

            records = collected_evidence.data.get(
                "records",
                [],
            )

            record_count = len(records)

            # ---------------------------------------------
            # Evaluate evidence
            # ---------------------------------------------

            evaluation = evaluate_evidence(
                evidence=collected_evidence,
                llm=llm,
            )

            # ---------------------------------------------
            # Remember this successful attempt
            #
            # IMPORTANT:
            # query.kql contains USER_TARGET etc.
            # It does NOT contain the real bound entity.
            # ---------------------------------------------

            investigation_attempt = InvestigationAttempt(
                attempt_number=attempt_number,
                objective=query.objective,
                kql_strategy=query.kql,
                record_count=record_count,
                successful=True,
                failure_reason=None,
                evaluation=evaluation.reasoning,
                next_action=evaluation.next_action,
            )

            state.add_attempt(
                investigation_attempt
            )

            print(
                "Evidence sufficient:",
                evaluation.sufficient,
            )

            print(
                "Evaluation:",
                evaluation.reasoning,
            )

            # ---------------------------------------------
            # Stop if enough evidence was collected
            # ---------------------------------------------

            if evaluation.sufficient:
                state.completed = True

                print(
                    "Investigation task has "
                    "sufficient evidence."
                )

                break

            # ---------------------------------------------
            # Otherwise prepare next investigation attempt
            # ---------------------------------------------

            next_action = evaluation.next_action

            state.next_action = next_action

            if not next_action:
                print(
                    "No additional investigation "
                    "action recommended."
                )

                break

            print(
                "Next investigation action:",
                next_action,
            )

        else:
            print(
                "\nMaximum investigation "
                "attempts reached."
            )

        # ---------------------------------------------
        # Show investigation state summary
        # ---------------------------------------------

        print(
            "\nINVESTIGATION STATE"
        )

        print(
            "Attempts recorded:",
            len(state.attempts),
        )

        print(
            "Completed:",
            state.completed,
        )

    return all_evidence