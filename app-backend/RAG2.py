import os
import pickle
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama
import chromadb
import numpy as np

def initialize_database(pdf_directory="data", metadata_file="metadata.pkl"):
    # Load existing metadata if available
    if os.path.exists(metadata_file):
        with open(metadata_file, 'rb') as f:
            metadata = pickle.load(f)
    else:
        metadata = {}

    # Load PDFs and split them into chunks
    docs = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=150,
        length_function=len,
        is_separator_regex=False,
    ).split_documents(PyPDFDirectoryLoader(pdf_directory).load())

    # Create a ChromaDB collection and store document embeddings
    client = chromadb.Client()
    collection = client.create_collection(name="docs")

    # Import documents into the database only if not already imported
    for d in docs:
        doc_id = str(d.metadata)
        if doc_id not in metadata:
            embedding = ollama.embeddings(model="nomic-embed-text", prompt=d.page_content)["embedding"]
            collection.add(ids=[doc_id], embeddings=[embedding], documents=[d.page_content])
            metadata[doc_id] = d.metadata  # Save metadata of imported document

    # Save metadata to a pickle file
    with open(metadata_file, 'wb') as f:
        pickle.dump(metadata, f)

    return collection

# Function to compute the cosine similarity between two vectors
def compute_cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    return (u @ v) / (np.linalg.norm(u) * np.linalg.norm(v))

def query_document(prompt, collection):
    # Query the most relevant document for the given prompt
    query_embedding = ollama.embeddings(model="nomic-embed-text", prompt=prompt)["embedding"]
    results = collection.query(query_embeddings=[query_embedding], n_results=5)
    context = str(results["documents"])

    # Generate a response using the most relevant document context
    output = ollama.generate(model="llama3.2", prompt=f"This is the data obtained from internet: {context} use this if you need to correct the outputs: . Respond to this prompt, if needed, refer the data: {prompt}")

    return output['response']

def query_rag(user_input, collection=initialize_database()):
    response = query_document(user_input, collection)
    return response

if __name__ == '__main__':
    pdf_directory = "data"  # Directory containing PDFs
    metadata_file = "metadata.pkl"  # File to store metadata

    # Initialize the database and load documents
    collection = initialize_database(pdf_directory, metadata_file)

    # Example input from the user
    user_input = input("Enter your data string (prompt): ")
    response = query_document(user_input, collection)
    print("Response:", response)
