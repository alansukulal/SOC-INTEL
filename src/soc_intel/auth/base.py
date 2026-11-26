from abc import ABC, abstractmethod

from soc_intel.models.credentials import ClientSecretCredentials


class CredentialResolver(ABC):
    @abstractmethod
    def resolve(
        self,
        credential_ref: str,
    ) -> ClientSecretCredentials:
        pass