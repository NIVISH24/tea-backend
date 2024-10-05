from LLM import search_suggestions

prompt = input("What do you want to learn today? \n")

# Send to LLM to ask what it would like to search for
search_queries = search_suggestions(prompt)
print(search_queries)

