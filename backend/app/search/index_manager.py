from app.search.opensearch_client import (
    opensearch_client,
    INCIDENT_INDEX,
    ASSET_INDEX,
    INCIDENT_INDEX_MAPPING,
    ASSET_INDEX_MAPPING
)

def create_index(index_name: str, mapping: dict, recreate: bool = False):
    exists = opensearch_client.indices.exists(index=index_name)

    if exists and recreate:
        opensearch_client.indices.delete(index=index_name)
        print(f"Deleted existing index: {index_name}")
        exists = False

    if not exists:
        opensearch_client.indices.create(
            index=index_name,
            body=mapping
        )
        print(f"Created index: {index_name}")
    else:
        print(f"Index already exists: {index_name}")

def create_all_indexes(recreate: bool = False):
    create_index(INCIDENT_INDEX, INCIDENT_INDEX_MAPPING, recreate)
    create_index(ASSET_INDEX, ASSET_INDEX_MAPPING, recreate)
    print("All indexes ready.")

def get_index_stats():
    stats = {}
    for index in [INCIDENT_INDEX, ASSET_INDEX]:
        try:
            count = opensearch_client.count(index=index)
            stats[index] = count["count"]
        except Exception:
            stats[index] = "index not found"
    return stats