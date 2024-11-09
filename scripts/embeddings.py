import json
import os
import psycopg2
from transformers import DistilBertTokenizer, DistilBertModel
import torch

# Initialize the BERT tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')

def generate_bert_embeddings(text):
    # Tokenize and process the input text to generate embeddings
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    # Take the mean of all token embeddings to get a single vector
    embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return embedding.tolist()  # Convert to list for JSON serialization

def generate_embeddings(documents):
    embeddings = []
    for doc in documents:
        # Generate embeddings for title and summary
        title_embedding = generate_bert_embeddings(doc['title'])
        summary_embedding = generate_bert_embeddings(doc['summary'])
        
        embeddings.append({
            'title': doc['title'],
            'summary': doc['summary'],
            'title_embedding': title_embedding,
            'summary_embedding': summary_embedding,
            'authors': doc['authors'],
            'published': doc['published']
        })
    return embeddings

def save_embeddings_to_db(embeddings):
    try:
        conn = psycopg2.connect(
            host="localhost",  # Your DB host
            database="ingestion",  # Your DB name
            user="postgres",  # Your DB user
            password="password"  # Your DB password
        )
        cursor = conn.cursor()

        for embed in embeddings:
            # Insert embeddings into TimescaleDB (PostgreSQL with pgAI)
            query = """
            INSERT INTO embeddings_table (title, summary, title_embedding, summary_embedding, authors, published)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                embed['title'],
                embed['summary'],
                json.dumps(embed['title_embedding']),  # Store embeddings as JSON
                json.dumps(embed['summary_embedding']),
                ', '.join(embed['authors']),
                embed['published']
            ))
        
        conn.commit()
        print("Embeddings saved to database.")
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()

def main():
    # Load preprocessed documents
    input_path = '../data/processed/processed_documents.json'
    with open(input_path, 'r') as f:
        documents = json.load(f)
    
    # Generate embeddings
    embeddings = generate_embeddings(documents)
    
    # Save embeddings to the database
    save_embeddings_to_db(embeddings)
    
    # Optionally, save the embeddings as a JSON file locally
    output_path = '../data/embeddings/embeddings.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(embeddings, f, indent=2)
    print("Embeddings saved to file.")

if __name__ == "__main__":
    main()

