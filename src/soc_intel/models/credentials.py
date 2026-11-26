from pydantic import BaseModel


class ClientSecretCredentials(BaseModel):
    client_id: str
    client_secret: str