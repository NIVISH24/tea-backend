import ollama

def search_suggestions(user_input):
    prompt = f"This is the user prompt: '{user_input}'. Based on this prompt, generate a list of search suggestions that can help you refine your search query for data you can feed on to provide a more accurate response."
    output = ollama.generate(model="llama3.2", prompt=prompt)
    return(output["response"])


def generate_topic_name(user_input):
    prompt = f"Based on the user's input, '{user_input}', generate a clear and concise topic name that encapsulates the main subject. Just one sentence and nothing else."
    output = ollama.generate(model="llama3.2", prompt=prompt)
    print(output["response"])
    return output['response']

def generate_subheadings_and_related_topics(topic_name):
    prompt = f"For the topic '{topic_name}', list all the types, subheadings, and related topics necessary to fully understand this course in the form of a 1-Dimensional python list - between a [] Eg: [x, y, z] and no explanations."
    output = ollama.generate(model="llama3.2", prompt=prompt)
    print(output["response"])
    return eval(output['response'])  # Assuming the output is a string representation of a list.

def generate_content(topic_name, region, age, interests):
    prompt = f"Create tailored content for the topic '{topic_name}' based on the following parameters:\n" \
             f"- User Region: {region}\n" \
             f"- User Age: {age}\n" \
             f"- User Interests: {interests}\n" \
             f"Include examples relevant to the user's context."
    output = ollama.generate(model="llama3.2", prompt=prompt)
    print(output["response"])
    return output['response']

# Example usage
user_input = "Teach me about DBMS"
region = "India"
age = 15
interests = ["science", "star wars"]

# Generate topic name
topic_name = generate_topic_name(user_input)

# Generate subheadings and related topics
subheadings_and_related_topics = generate_subheadings_and_related_topics(topic_name)


content = [generate_content(i, region, age, interests) for i in subheadings_and_related_topics]

print("Topic Name:", topic_name)
print("Subheadings and Related Topics:", subheadings_and_related_topics)
print("Generated Content:", content)
"""
Llama.cpp can be used to leverage oneAPI's IPEX(Intel Extension for Pytorch) to run the model on Intel hardware.
RAG could've been used to retrieve content from the web and then generate content based on the user's input.
Complete knowledge about a domain can be gained this way.
"""


