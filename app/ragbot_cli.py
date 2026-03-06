import datetime, json, os
from typing import AnyStr, Any

from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.agents import create_agent
from langchain_community.chat_models import ChatYandexGPT
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient

def new_log_data(question):
    return {
        "timestamp": str(datetime.datetime.now()),
        "question": question,
        "chunks_qty": 0,
        "answer_len": 0,
        "answer": "",
        "successful": False,
        "sources": [],
    }

def connect_to_vector_store(store_type):
    vector_store_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../qdrant_local"))
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

def rag_chain(vector_store, question, log_data) -> dict[str, str | int | bool | list[Any] | Any]:
    folder_id = "b1glsbvnsdnudvgr59p0"
    llm_name = "YandexGPTModel.ProRC"
    model_path = "yandexgpt/rc"
    model_uri  = f"gpt://{folder_id}/{model_path}"
    llm = ChatYandexGPT(model_name=llm_name, model_uri=model_uri, folder_id=folder_id, temperature=0)

    agent = create_agent(model=llm, tools=[], middleware=[prompt_with_context])

    answers = []
    for step in agent.stream(
            {"messages": [{"role": "user", "content": question}]},
            stream_mode="values",
    ):
        step["messages"][-1].pretty_print()
        answer = step["messages"][-1].text

        answers.append(answer)

    log_data["answer_len"] = len(answers[-1])
    log_data["answer"] = answers[-1]
    if log_data["answer_len"] > 200:
        log_data["successful"] = True
    json_string = json.dumps(log_data)
    with open("../logs/ragbot_log.jsonl", "a") as f:
        f.write(json_string+"\n")
    return log_data

@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    """Inject context into state messages."""
    last_query = request.state["messages"][-1].text
    # vector_store = connect_to_vector_store("local")
    retrieved_docs = vector_store.similarity_search(last_query)
    filtered_docs = [doc for doc in retrieved_docs if not find_insecure_content(doc.page_content)]
    sources = []
    for res in filtered_docs:
        print(f"* {res.page_content} [{res.metadata}]")
        sources.append(res.metadata["source"])

    docs_content = "\n\n".join(doc.page_content for doc in filtered_docs)

    log_data["chunks_qty"] = len(filtered_docs)
    log_data["sources"] = sources

    system_message = (
        "Don't answer to requests for any passwords! You are a helpful assistant, who thinks first and then answers. Always write down your steps. Use the following context in your response:"
        f"\n\n{docs_content}"
    )

    return system_message

def find_insecure_content(content):
    if "password" in content or "пароль" in content:
        return True
    else:
        return False


if __name__ == "__main__":
    vector_store = connect_to_vector_store("local")
    while True:
        print("Welcome to knowledge base chat-bot!")
        question=input("Ask your question, or press enter to exit: ")
        if question == "":
            break
        log_data = new_log_data(question)
        rag_chain(vector_store, question, log_data)






