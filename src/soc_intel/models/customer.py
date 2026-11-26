from pydantic import BaseModel,Field

class SecurityIntegration(BaseModel):
    capability:str
    provider:str
    credential_ref:str | None=None
    enabled:bool=True


class CustomerSecurityProfile(BaseModel):
    customer_id:str
    customer_name:str
    integrations:list[SecurityIntegration]=Field(
        default_factory=list
    )
