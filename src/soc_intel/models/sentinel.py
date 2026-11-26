from pydantic import BaseModel


class SentinelConfig(BaseModel):
    tenant_id: str
    subscription_id: str
    resource_group: str
    workspace_name: str
    workspace_id: str
    credential_ref: str