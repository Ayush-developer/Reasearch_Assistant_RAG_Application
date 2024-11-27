
# Reasearch Assistant RAG Application

Research Assistant Application Overview This repository contains a Research Assistant application designed to assist users in querying research papers from arXiv based on their prompts. The system processes the retrieved papers, generates summaries and insights using LLM (Ollama-Llama), and fact-checks the outputs with Mistral. The application includes a React-based frontend for user interaction and a Python backend for pipeline execution and data management.




## Features

**Fetch Research Papers**: Fetches papers from arXiv based on user queries.

**Preprocessing Pipeline**: Processes raw data to extract and structure key insights.

**Embedding & Vectorization**: Utilizes PGVector for vectorizing document data.

**Text Generation**: Generates insights and summaries using Ollama-Llama.

**Fact-Checking**: Uses Mistral to verify the accuracy of generated insights.

**Database Management**: Stores metadata and embeddings in a TimescaleDB (Postgres) database running on Docker.

**Interactive Frontend**: React-based frontend for prompt submission and result visualization.
## Installation

To run this project, you will need to add the following libraries

1. Python (version >= 3.8)
2. Node.js (version >= 14)
3. Docker (for TimescaleDB)
4. Postgres (PGVector extension)

