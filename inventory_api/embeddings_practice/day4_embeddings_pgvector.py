import os
import psycopg2
from typing import List


EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")



def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )



def generate_embedding(text: str) -> List[float]:
    try:
        from openai import OpenAI

        model = os.getenv("OPENAI_EMBEDDING_MODEL")
        if not model:
            raise RuntimeError("OPENAI_EMBEDDING_MODEL is not set in environment")

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.embeddings.create(
            model=model,
            input=text
        )

        return response.data[0].embedding

    except Exception as e:
        raise RuntimeError(f"Embedding generation failed: {e}")




def store_embedding(content: str, embedding: List[float]):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO text_embeddings (content, embedding)
        VALUES (%s, %s)
        """,
        (content, embedding)
    )

    conn.commit()
    cur.close()
    conn.close()



def run_demo():
    texts = [
        "Flask is a lightweight web framework",
        "PostgreSQL is a relational database",
        "Embeddings convert text into vectors"
    ]

    for text in texts:
        embedding = generate_embedding(text)
        store_embedding(text, embedding)
        print(f" Stored embedding for: {text}")

if __name__ == "__main__":
    run_demo()
