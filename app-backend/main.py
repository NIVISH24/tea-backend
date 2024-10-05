from LLM import search_suggestions, generate_subheadings_and_related_topics, generate_topic_name
from scrape import scrape_and_save_to_pdf
from RAG2 import query_rag

prompt = input("What do you want to learn today? \n")


topic_name = generate_topic_name(prompt)

# Send to LLM to ask what it would like to search for
search_queries = search_suggestions(prompt)
search_queries_list = eval(search_queries)

# scrape them all

for query in search_queries_list:
    scrape_and_save_to_pdf(query)
    print(f"Scraped and saved {query} to PDF")

# Send to RAG to generate a response
response = query_rag(generate_subheadings_and_related_topics(prompt))
    


