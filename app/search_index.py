from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient

def connect_to_vector_store(store_type):
    vector_store_path = "../local_qdrant"
    collection_name = "knowledge_base"
    server_url = "http://localhost:6333"

    if store_type == "local":
        client = QdrantClient(path=vector_store_path)
    else:
        client = QdrantClient(url=server_url)

    embeddings_path = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = SentenceTransformerEmbeddings(model_name=embeddings_path)

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
        retrieval_mode=RetrievalMode.DENSE,
    )

    return vector_store

# Загружаем документы
def search(vector_store, query):

    results = vector_store.similarity_search(
        query, k=3
    )
    for res in results:
        print(f"* {res.page_content} [{res.metadata}]")

if __name__ == "__main__":
    vector_store = connect_to_vector_store("server")
    while True:
        print("Welcome to knowledge base chat-bot!")
        query=input("Ask your question, or press enter to exit: ")
        if query == "":
            break
        search(vector_store, query)

