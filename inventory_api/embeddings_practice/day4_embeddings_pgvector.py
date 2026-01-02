import os
import psycopg2
from typing import List

def get_db_connection():
    return psycopg2.connect(
        dbname="inventory_db",
        user="postgres",
        password="70722109",   # same as your .env
        host="localhost",
        port=5432
    )



def generate_embedding(text: str) -> List[float]:
    """
    Generates embedding for given text.
    Falls back to dummy embedding if API quota fails.
    """
    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding

    except Exception as e:
        print(" OpenAI embedding failed, using dummy vector:", e)
        # Dummy embedding (1536 dimensions)
        return [0.0] * 1536




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
