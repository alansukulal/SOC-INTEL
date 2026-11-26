from pydantic import BaseModel, Field


class SecurityEnvironmentCapabilities(BaseModel):
    siem_provider: str
    available_tables: list[str] = Field(default_factory=list)