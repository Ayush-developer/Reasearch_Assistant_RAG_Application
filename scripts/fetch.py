import requests
import json
import urllib, urllib.request

import requests
import json
import urllib.request
import xml.etree.ElementTree as ET
def fetch_arxiv_documents(query, start=0, max_results=5):

    url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start={start}&max_results={max_results}'
    data = urllib.request.urlopen(url)
    xml_data = data.read().decode('utf-8')

    root = ET.fromstring(xml_data)
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
    print("arXiv documents fetched and saved to data/raw/arxiv_documents.json")

if __name__ == "__main__":
    fetch_arxiv_documents(query='electron', start=0, max_results=5)
