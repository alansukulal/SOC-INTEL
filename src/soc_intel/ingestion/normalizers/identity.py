from soc_intel.models.entity import Entity, EntityType


def build_entity_identity(entity: Entity) -> str:
    attributes = entity.attributes

    if entity.entity_type == EntityType.USER:
        if attributes.get("aadUserId"):
            return f"user:aad:{attributes['aadUserId'].lower()}"

        if attributes.get("sid"):
            return f"user:sid:{attributes['sid'].lower()}"

        account_name = attributes.get("accountName")
        upn_suffix = attributes.get("upnSuffix")

        if account_name and upn_suffix:
            return f"user:upn:{account_name.lower()}@{upn_suffix.lower()}"

    if entity.entity_type == EntityType.HOST:
        if attributes.get("azureID"):
            return f"host:azure:{attributes['azureID'].lower()}"

        if attributes.get("omsAgentID"):
            return f"host:oms:{attributes['omsAgentID'].lower()}"

        host_name = attributes.get("hostName")
        dns_domain = attributes.get("dnsDomain")

        if host_name and dns_domain:
            return f"host:dns:{host_name.lower()}.{dns_domain.lower()}"

        nt_domain = attributes.get("ntDomain")

        if host_name and nt_domain:
            return f"host:nt:{nt_domain.lower()}\\{host_name.lower()}"

    if entity.entity_type == EntityType.FILE_HASH:
        algorithm = attributes.get("algorithm")
        hash_value = attributes.get("hashValue") or attributes.get("value")

        if algorithm and hash_value:
            return f"file_hash:{algorithm.lower()}:{hash_value.lower()}"

    if entity.entity_type == EntityType.IP:
        address = attributes.get("address")
        address_scope = attributes.get("addressScope")

        if address and address_scope:
            return f"ip:{address.lower()}:{address_scope.lower()}"

    if entity.entity_type == EntityType.DOMAIN:
        domain_name = attributes.get("domainName")

        if domain_name:
            return f"domain:{domain_name.lower()}"

    if entity.entity_type == EntityType.URL:
        url = attributes.get("url")

        if url:
            return f"url:{url}"

    if entity.entity_type == EntityType.EMAIL:
        mailbox = attributes.get("mailboxPrimaryAddress")

        if mailbox:
            return f"email:{mailbox.lower()}"

    if entity.entity_type == EntityType.CLOUD_RESOURCE:
        resource_id = attributes.get("resourceId")

        if resource_id:
            return f"cloud_resource:{resource_id.lower()}"

    return f"{entity.entity_type.value}:fallback:{entity.value.lower()}"

def deduplicate_entities(entities: list[Entity],) -> list[Entity]:

    unique_entities = []
    seen_identities = set()

    for entity in entities:
        identity = build_entity_identity(entity)

        # Fallback identities are not strong enough for safe deduplication.
        if ":fallback:" in identity:
            unique_entities.append(entity)
            continue

        if identity in seen_identities:
            continue

        seen_identities.add(identity)
        unique_entities.append(entity)

    return unique_entities