import os
from soc_intel.auth.base import CredentialResolver
from soc_intel.models.credentials import ClientSecretCredentials

#for getting client secrets
class EnvironmentCredentialResolver(CredentialResolver):
    def resolve(self, credential_ref:str,)-> ClientSecretCredentials:
        prefix=credential_ref.upper().replace("-","_")

        client_id=os.getenv(f"{prefix}_CLIENT_ID")
        client_secret=os.getenv(f"{prefix}_CLIENT_SECRET")

        if not client_id or not client_secret:
            raise ValueError(f"Credentials not found for reference:{credential_ref}")


        return ClientSecretCredentials(
            client_id=client_id,
            client_secret=client_secret,
        )
        
        
