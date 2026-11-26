import os

from dotenv import load_dotenv

from soc_intel.models.sentinel import SentinelConfig


load_dotenv()


def load_sentinel_config() -> SentinelConfig:
    return SentinelConfig(
        tenant_id=os.environ[
            "SOC_INTEL_SENTINEL_TENANT_ID"
        ],
        subscription_id=os.environ[
            "SOC_INTEL_SENTINEL_SUBSCRIPTION_ID"
        ],
        resource_group=os.environ[
            "SOC_INTEL_SENTINEL_RESOURCE_GROUP"
        ],
        workspace_name=os.environ[
            "SOC_INTEL_SENTINEL_WORKSPACE_NAME"
        ],
        workspace_id=os.environ[
            "SOC_INTEL_SENTINEL_WORKSPACE_ID"
        ],
        credential_ref="soc-intel-dev",
    )