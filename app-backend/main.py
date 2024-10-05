from LLM import search_suggestions
from scrape import scrape_and_save_to_pdf

prompt = input("What do you want to learn today? \n")

# Send to LLM to ask what it would like to search for
search_queries = search_suggestions(prompt)
search_queries_list = eval(search_queries)

# scrape them all

for query in search_queries_list:
    scrape_and_save_to_pdf(query)
    print(f"Scraped and saved {query} to PDF")
    


