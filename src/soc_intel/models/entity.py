from enum import Enum

from pydantic import BaseModel, Field


class EntityType(str, Enum):
    HOST = "host"
    USER = "user"
    IP = "ip"
    DOMAIN = "domain"
    URL = "url"
    FILE_HASH = "file_hash"
    PROCESS = "process"
    EMAIL = "email"
    CLOUD_RESOURCE = "cloud_resource"


class Entity(BaseModel):
    entity_type: EntityType
    value: str
    attributes: dict[str, str] = Field(default_factory=dict)