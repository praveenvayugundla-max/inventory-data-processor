import os
from langchain_openai import OpenAIEmbeddings

def run_demo():
    """
    Demonstrates embedding generation using LangChain.
    This complements the PGVector-based implementation.
    """

    embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
    )


    texts = [
        "Flask is a lightweight web framework",
        "PostgreSQL is a relational database",
        "LangChain simplifies LLM workflows"
    ]

    vectors = embeddings.embed_documents(texts)

    for text, vector in zip(texts, vectors):
        print(f"Text: {text}")
        print(f"Vector length: {len(vector)}")
        print("-" * 40)

if __name__ == "__main__":
    run_demo()
