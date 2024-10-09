from LLM import search_suggestions, generate_subheadings_and_related_topics, generate_topic_name, generate_content
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
response = ollama.generate(model="llama3.2", prompt=f"{response} \n\n convert this to python list of strings and nothing else, no explanations eg:['subheading1', 'subheading2', ...]")
output = (response["response"])
output = output[output.find('['):output.find(']')+1]
response = eval(output)

user_input = "Teach me about DBMS"
region = "Chennai, TN, India"
age = 19
interests = ["singing", "dancing", "gazing through the stars", "pursuing engineering at VIT University", "President of Seraphic club - VIT Chennai (mental health club)"]
content = [generate_content(i, region, age, interests) for i in response]

# save this to separate text files

for i, c in enumerate(content):
    with open(f"{response[i]}.txt", "w") as f:
        f.write(c)
        print(f"Content for {response[i]} saved to {response[i]}.txt")
        
    


