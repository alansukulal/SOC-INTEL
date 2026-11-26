from typing import Any

import requests
from azure.identity import ClientSecretCredential

from soc_intel.auth.base import CredentialResolver
from soc_intel.models.sentinel import SentinelConfig
from soc_intel.tools.siem.base import SIEMProvider


class SentinelProvider(SIEMProvider):
    def __init__(
        self,
        config: SentinelConfig,
        credential_resolver: CredentialResolver,
    ) -> None:
        self.config = config
        self.credential_resolver = credential_resolver

    def _build_azure_credential(self) -> ClientSecretCredential:
        credentials = self.credential_resolver.resolve(
            self.config.credential_ref
        )

        return ClientSecretCredential(
            tenant_id=self.config.tenant_id,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
        )

    def get_incident(
        self,
        incident_id: str,
    ) -> dict[str, Any]:
        credential = self._build_azure_credential()

        token = credential.get_token(
            "https://management.azure.com/.default"
        )

        url = (
            "https://management.azure.com/"
            f"subscriptions/{self.config.subscription_id}/"
            f"resourceGroups/{self.config.resource_group}/"
            "providers/Microsoft.OperationalInsights/"
            f"workspaces/{self.config.workspace_name}/"
            "providers/Microsoft.SecurityInsights/"
            f"incidents/{incident_id}"
        )

        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {token.token}",
            },
            params={
                "api-version": "2025-09-01",
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def get_incident_alerts(
        self,
        incident_id: str,
    ) -> list[dict[str, Any]]:
        credential = self._build_azure_credential()

        token = credential.get_token(
            "https://management.azure.com/.default"
        )

        url = (
            "https://management.azure.com/"
            f"subscriptions/{self.config.subscription_id}/"
            f"resourceGroups/{self.config.resource_group}/"
            "providers/Microsoft.OperationalInsights/"
            f"workspaces/{self.config.workspace_name}/"
            "providers/Microsoft.SecurityInsights/"
            f"incidents/{incident_id}/alerts"
        )

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {token.token}",
            },
            params={
                "api-version": "2025-09-01",
            },
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("value", [])

    def get_incident_entities(self,incident_id: str,) -> list[dict[str, Any]]:
        credential = self._build_azure_credential()

        token = credential.get_token(
            "https://management.azure.com/.default"
        )

        url = (
            "https://management.azure.com/"
            f"subscriptions/{self.config.subscription_id}/"
            f"resourceGroups/{self.config.resource_group}/"
            "providers/Microsoft.OperationalInsights/"
            f"workspaces/{self.config.workspace_name}/"
            "providers/Microsoft.SecurityInsights/"
            f"incidents/{incident_id}/entities"
        )

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {token.token}",
            },
            params={
                "api-version": "2025-09-01",
            },
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("entities", [])