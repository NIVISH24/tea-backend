from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama
import chromadb
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load PDFs and split them into chunks once when the server starts
docs = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=300,
    length_function=len,
    is_separator_regex=False,
).split_documents(PyPDFDirectoryLoader("data").load())

# Create a ChromaDB collection and store document embeddings
client = chromadb.Client()
collection = client.create_collection(name="docs")
for d in docs:
    embedding = ollama.embeddings(model="nomic-embed-text", prompt=d.page_content)["embedding"]
    collection.add(ids=[str(d.metadata)], embeddings=[embedding], documents=[d.page_content])

# Function to compute the cosine similarity between two vectors
def compute_cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    return (u @ v) / (np.linalg.norm(u) * np.linalg.norm(v))

@app.route('/query', methods=['POST'])
def query_document():
    data = request.json
    prompt = data.get("prompt")

    # Query the most relevant document for the given prompt
    query_embedding = ollama.embeddings(model="nomic-embed-text", prompt=prompt)["embedding"]
    results = collection.query(query_embeddings=[query_embedding], n_results=5)
    context = str(results["documents"])

    # Generate a response using the most relevant document context
    output = ollama.generate(model="llama3.2", prompt=f"Using this data: {context}. Respond to this prompt: {prompt}")

    return jsonify({'response': output['response']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
