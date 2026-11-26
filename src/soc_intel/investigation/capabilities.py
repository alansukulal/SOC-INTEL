from soc_intel.models.customer import (
    CustomerSecurityProfile,
    SecurityIntegration,
)


def get_integration(customer: CustomerSecurityProfile,capability: str,) -> SecurityIntegration | None:
    """
    Return the enabled integration that provides
    the requested security capability.
    """

    for integration in customer.integrations:
        if (
            integration.enabled
            and integration.capability.lower() == capability.lower()
        ):
            return integration

    return None