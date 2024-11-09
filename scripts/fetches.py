import requests
import json
import spacy
import xml.etree.ElementTree as ET
import sys

# Load the spaCy model for keyword extraction
nlp = spacy.load("en_core_web_sm")

# Define common intents for research queries
INTENT_KEYWORDS = {
    "survey": ["survey", "review", "overview", "summary"],
    "application": ["application", "implementation", "use case", "practical"],
    "comparison": ["comparison", "comparative", "benchmark", "vs"],
    "experimental": ["experiment", "study", "analysis", "evaluation"],
}

def detect_intent(query):
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in query.lower() for keyword in keywords):
            return intent
    return "general"

def extract_keywords(query):
    doc = nlp(query)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
    return " OR ".join(keywords)

def fetch_arxiv_documents(query, start=0, max_results=5):
    intent = detect_intent(query)
    keywords = extract_keywords(query)
    
    if intent != "general":
        keywords += f" AND {intent}"

    url = f'http://export.arxiv.org/api/query?search_query=all:{keywords}&start={start}&max_results={max_results}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        documents = []

        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            doc = {
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text,
                'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text,
                'authors': [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
                'published': entry.find('{http://www.w3.org/2005/Atom}published').text
            }
            documents.append(doc)

        with open('../data/raw/arxiv_documents.json', 'w') as f:
            json.dump(documents, f)

        # Save the query to a JSON file
        with open('../data/raw/query.json', 'w') as f:
            json.dump({"query": query}, f)

        print("arXiv documents fetched and saved to data/raw/arxiv_documents.json")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")

if __name__ == "__main__":
    # Get query from command-line argument
    user_query = sys.argv[1] if len(sys.argv) > 1 else ""
    
    if user_query:
        fetch_arxiv_documents(query=user_query, start=0, max_results=5)
    else:
        print("No query provided.")

