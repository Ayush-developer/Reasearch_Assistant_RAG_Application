import re
import json
import os

def preprocess_text(text):

    text = re.sub(r'[^a-zA-Z0-9.,;:?!\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

def preprocess_documents(input_path, output_path):
    os.makedirs(output_path, exist_ok=True)

    with open(input_path, 'r') as f:
        documents = json.load(f)
    
    processed_documents = []
    
    for doc in documents:

        title = preprocess_text(doc.get('title', ''))
        summary = preprocess_text(doc.get('summary', ''))
        authors = doc.get('authors', [])
        
        processed_doc = {
            'title': title,
            'summary': summary,
            'authors': authors,
            'published': doc.get('published', '')
        }
        
        processed_documents.append(processed_doc)
    
    with open(os.path.join(output_path, 'processed_documents.json'), 'w') as f:
        json.dump(processed_documents, f, indent=2)
    print("Documents preprocessed and saved to", output_path)

if __name__ == "__main__":

    input_path = '../data/raw/arxiv_documents.json'  # Or your JSON API file
    output_path = '../data/processed'
    
    preprocess_documents(input_path, output_path)

