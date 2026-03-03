import os, logging
import shutil
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings
from huggingface_hub import snapshot_download
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from uuid import uuid4

# Загружаем документы
def update_vector_store(store_type):
    logging.info("Читаем документы...")
    snapshot_download("sentence-transformers/all-MiniLM-L6-v2")
    # Загрузка документов
    documents = []
    input_dir = "../import_docs"
    imported_dir = "../imported_docs"
    for filename in os.listdir(input_dir):
        if filename.endswith(".md"):
            file_path = os.path.join(input_dir, filename)
            loader = TextLoader(file_path, encoding="utf-8")
            current_documents = loader.load()
            documents.extend(current_documents)
            shutil.move(file_path, imported_dir)
            logging.info(f" {file_path}")
    logging.info(f"Прочитано {len(documents)} документов")

    # Разделение на чанки
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", "(?<=\\. )", " ", ""],
        keep_separator=False
    )
    chunks = text_splitter.split_documents(documents)
    logging.info(f"Документы разбиты на {len(chunks)} чанков")

    vector_store_path = "../local_qdrant"
    collection_name = "knowledge_base"
    server_url = "http://localhost:6333"

    if store_type == "local":
        client = QdrantClient(path=vector_store_path)
        logging.info("Выбран локальный Qdrant")
    else:
        client = QdrantClient(url=server_url)
        logging.info("Выбран серверный Qdrant")

    # Создание эмбеддингов и векторного хранилища
    embeddings_path = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = SentenceTransformerEmbeddings(model_name=embeddings_path)

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )

    uuids = [str(uuid4()) for _ in range(len(chunks))]
    # vector_store.add_documents(documents=chunks, ids=uuids)
    logging.info(f"Загружено в Qdrant {len(chunks)} чанков")
    collection_info = client.get_collection(collection_name=collection_name)
    logging.info(f"Информация о коллекции {collection_info}")

    print(f"Создано {len(chunks)} чанков")
    print("Векторное хранилище сохранено в 'knowledge_base'")

    return vector_store

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        filename="../logs/update_index.log",
        filemode="a",
        format="%(asctime)s %(levelname)s %(message)s",
    )
    vector_store = update_vector_store("server")

