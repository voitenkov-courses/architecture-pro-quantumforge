from qdrant_client import QdrantClient

def backup_quadrant_collection(url, collection_name):

    client = QdrantClient(url=url)
    client.create_snapshot(collection_name=collection_name)

    return

if __name__ == "__main__":
    server_url = "http://localhost:6333"
    collection_name = "knowledge_base"
    backup_quadrant_collection(server_url, collection_name)

