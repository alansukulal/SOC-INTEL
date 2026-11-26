from typing import Any

import requests
from azure.identity import ClientSecretCredential

from soc_intel.auth.base import CredentialResolver
from soc_intel.models.capabilities import SecurityEnvironmentCapabilities
from soc_intel.models.sentinel import SentinelConfig


class SentinelQueryTool:
    def __init__(
        self,
        config: SentinelConfig,
        credential_resolver: CredentialResolver,
    ) -> None:
        self.config = config
        self.credential_resolver = credential_resolver

    def _build_credential(self) -> ClientSecretCredential:
        credentials = self.credential_resolver.resolve(
            self.config.credential_ref
        )

        return ClientSecretCredential(
            tenant_id=self.config.tenant_id,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
        )

    def _get_token(self) -> str:
        credential = self._build_credential()

        token = credential.get_token(
            "https://api.loganalytics.io/.default"
        )

        return token.token

    def run_query(
        self,
        kql: str,
        timespan: str = "PT24H",
    ) -> dict[str, Any]:
        token = self._get_token()

        url = (
            "https://api.loganalytics.azure.com/"
            f"v1/workspaces/{self.config.workspace_id}/query"
        )

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={
                "query": kql,
                "timespan": timespan,
            },
            timeout=30,
        )

        if not response.ok:
            try:
                error_details = response.json()
            except ValueError:
                error_details = {
                    "message": response.text
                }

            raise RuntimeError(
                "Sentinel query failed. "
                f"Status: {response.status_code}. "
                f"Details: {error_details}"
            )

        return response.json()

    def discover_capabilities(
        self,
    ) -> SecurityEnvironmentCapabilities:
        token = self._get_token()

        url = (
            "https://api.loganalytics.azure.com/"
            f"v1/workspaces/{self.config.workspace_id}/metadata"
        )

        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=30,
        )

        response.raise_for_status()

        metadata = response.json()

        available_tables = sorted(
            {
                table["name"]
                for table in metadata.get("tables", [])
                if table.get("name")
            }
        )

        return SecurityEnvironmentCapabilities(
            siem_provider="sentinel",
            available_tables=available_tables,
        )