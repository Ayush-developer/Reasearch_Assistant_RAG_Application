import psycopg2
import json
import os
import numpy as np

# Load data from processed_documents.json
def load_processed_documents():
    file_path = os.path.join('..', 'data', 'processed', 'processed_documents.json')
    with open(file_path, 'r') as file:
        return json.load(file)

processed_documents = load_processed_documents()

def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="password"
        )
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_table():
    conn = connect_db()
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS new_documents (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    summary TEXT,
                    authors TEXT[],
                    published TIMESTAMP,
                    embedding VECTOR(128)
                );
            """)
            conn.commit()
            cur.close()
        finally:
            conn.close()

def generate_embedding(text, target_dim=128):
    conn = connect_db()
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute("SET ai.ollama_host = 'http://host.docker.internal:11434/';")
            cur.execute("SELECT ai.ollama_embed('nomic-embed-text', %s);", (text,))
            embedding = cur.fetchone()
            if embedding and embedding[0]:
                embedding = json.loads(embedding[0])
                if isinstance(embedding, list):
                    embedding = np.array(embedding)
                elif not isinstance(embedding, np.ndarray):
                    return None
                return embedding[:target_dim] if len(embedding) >= target_dim else np.pad(embedding, (0, target_dim - len(embedding)))
        finally:
            conn.close()
    return None

def insert_data():
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            for doc in processed_documents:
                embedding = generate_embedding(f"{doc['title']} - {doc['summary']}")
                if embedding is not None and embedding.size > 0:
                    cur.execute("""
                        INSERT INTO new_documents (title, summary, authors, published, embedding)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (doc['title'], doc['summary'], doc['authors'], doc['published'], embedding.tolist()))
            conn.commit()
        finally:
            conn.close()

def fetch_data():
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT title, summary, authors, published, embedding FROM new_documents;")
            rows = cur.fetchall()
            return rows
        finally:
            conn.close()
    return []

def retrieve_and_generate_response(query):
    # Load the query from query.json (or from a direct argument)
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SET ai.ollama_host = 'http://host.docker.internal:11434/';")
            query_embedding = generate_embedding(query)

            if query_embedding is not None and query_embedding.size > 0:
                cur.execute("""
                    SELECT title, summary, authors, published, 1 - (embedding <=> %s::VECTOR) AS similarity
                    FROM new_documents
                    ORDER BY similarity DESC
                    LIMIT 5;
                """, (query_embedding.tolist(),))

                rows = cur.fetchall()
                context = "\n\n".join([f"Title: {row[0]}\nSummary: {row[1]}\nAuthors: {row[2]}\nPublished: {row[3]}" for row in rows])

                cur.execute("SELECT ai.ollama_generate('llama2', %s)", (f"Query: {query}\nContext: {context}",))
                model_response = cur.fetchone()
                if model_response:
                    response = model_response[0]
                    print(response['response'])
                else:
                    print("No response received from Ollama.")
            else:
                print("Failed to generate query embedding.")
        finally:
            conn.close()

def main(query):
    create_table()
    insert_data()
    retrieve_and_generate_response(query)

if __name__ == "__main__":
    # You will pass the query as a command-line argument or environment variable
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "default query"
    main(query)

