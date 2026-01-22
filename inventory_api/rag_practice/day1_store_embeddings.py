import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import PGVector

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

CONNECTION_STRING = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

COLLECTION_NAME = "rag_laptop_setup_docs"

def store_chunks(chunks):
    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    )
    
    vector_store = PGVector(
        connection_string=CONNECTION_STRING,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )
    
    vector_store.add_documents(chunks)
    print(f"Stored {len(chunks)} chunks in PGVector")

if __name__ == "__main__":
    from inventory_api.rag_practice.day1_pdf_ingestion import load_and_split_pdf
    store_chunks(load_and_split_pdf())