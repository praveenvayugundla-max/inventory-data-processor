import os
from typing import List
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document

# find .env file in project root
project_root = Path(__file__).parent.parent.parent
env_file = project_root / '.env'
load_dotenv(dotenv_path=env_file)

# db config
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

CONNECTION_STRING = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def get_embedding_function() -> OpenAIEmbeddings:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set")
    
    return OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

def get_vector_store() -> PGVector:
    return PGVector(
        connection_string=CONNECTION_STRING,
        embedding_function=get_embedding_function(),
        collection_name="text_embeddings",
    )

def store_texts(texts: List[str]) -> None:
    vector_store = get_vector_store()
    docs = [Document(page_content=text) for text in texts]
    vector_store.add_documents(docs)

def run_demo():
    texts = [
        "Flask is a lightweight web framework",
        "PostgreSQL is a relational database",
        "Embeddings convert text into vectors",
    ]
    
    store_texts(texts)
    print("Successfully stored embeddings using PGVector")

if __name__ == "__main__":
    run_demo()