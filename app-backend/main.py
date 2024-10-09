from LLM import search_suggestions, generate_subheadings_and_related_topics, generate_topic_name
from scrape import scrape_and_save_to_pdf
from RAG2 import query_rag
import ollama

prompt = "Teach me about DBMS"

topic_name = generate_topic_name(prompt)

# Send to LLM to ask what it would like to search for
search_queries = search_suggestions(topic_name)
search_queries_list = eval(search_queries)

# scrape them all

for query in search_queries_list:
    scrape_and_save_to_pdf(query)
    print(f"Scraped and saved {query} to PDF")

# Send to RAG to generate a response
response = query_rag(generate_subheadings_and_related_topics(prompt))
response = ollama.generate(model="llama3.2", prompt=f"{response} convert this to python one dimensional list of strings and nothing else, no explanations")
print(f"Response: {response['response']}")
    


