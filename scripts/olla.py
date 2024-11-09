import ollama

def generate_response(query, context):
    # Generate the response using the Ollama API
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": f"Query: {query}\nContext: {context}"}])
    
    # Print the response text to check the output
    print(f"Response: {response['text']}")

# Example query and context
query = "Give me a paper on electron thermal conductivity and its details and explain about it"
context = "This is a context with related papers and research on thermal conductivity."

# Call the function with the example query and context
generate_response(query, context)

