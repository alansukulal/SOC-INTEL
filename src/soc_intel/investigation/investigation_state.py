from pydantic import BaseModel, Field


class InvestigationAttempt(BaseModel):
    attempt_number: int

    objective: str

    kql_strategy: str

    record_count: int = 0

    successful: bool = True

    failure_reason: str | None = None

    evaluation: str | None = None

    next_action: str | None = None


class InvestigationState(BaseModel):
    attempts: list[InvestigationAttempt] = Field(
        default_factory=list
    )

    next_action: str | None = None

    completed: bool = False

    def add_attempt(
        self,
        attempt: InvestigationAttempt,
    ) -> None:
        self.attempts.append(attempt)

    def get_history_summary(self) -> str:
        if not self.attempts:
            return "No previous investigation attempts."

        history: list[str] = []

        for attempt in self.attempts:
            history.append(
                (
                    f"Attempt {attempt.attempt_number}: "
                    f"Objective={attempt.objective}; "
                    f"Strategy={attempt.kql_strategy}; "
                    f"Records={attempt.record_count}; "
                    f"Successful={attempt.successful}; "
                    f"Evaluation={attempt.evaluation}; "
                    f"Next action={attempt.next_action}"
                )
            )

        return "\n".join(history)