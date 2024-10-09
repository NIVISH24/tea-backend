import ollama
model = "llama3.2"

def search_suggestions(user_input):
    prompt = f"This is the topic name: '{user_input}'. Based on this, generate a list of search suggestions that can help you refine your search query for data you can feed on to provide a more accurate response."
    output = ollama.generate(model=model, prompt=prompt)
    output = ollama.generate(model=model, prompt=f"{output['response']} \n\n convert this to python list of strings, (eg. [\"topic1\", \"topic2\", ...]) and nothing else, no explanations")
    output = (output["response"])
    output = output[output.find('['):output.find(']')+1]
    print(output)
    return(output)


def generate_topic_name(user_input):
    prompt = f"Based on the user's input, '[{user_input}]', generate a clear and concise topic name that encapsulates the main subject. Just one or few words and nothing else."
    output = ollama.generate(model=model, prompt=prompt)
    print("topic name: ", output["response"])
    return output['response']

def generate_subheadings_and_related_topics(topic_name):
    prompt = f"For the topic '[{topic_name}]', list all the types, subheadings, and related topics necessary to fully understand this course."
    output = ollama.generate(model=model, prompt=prompt)
    output = ollama.generate(model=model, prompt=f"{output['response']} \n\n convert this to python list of strings and nothing else, no explanations eg:['subheading1', 'subheading2', ...]")
    output = (output["response"])
    output = output[output.find('['):output.find(']')+1]
    return (output)  # Assuming the output is a string representation of a list.

def generate_content(topic_name, region, age, interests):
    prompt = f"Create tailored content for the topic '{topic_name}' based on the following parameters:\n" \
             f"- User Region: {region}\n" \
             f"- User Age: {age}\n" \
             f"- User Interests: {interests}\n" \
             f"Include examples relevant to the user's context."
    output = ollama.generate(model=model, prompt=prompt)
    print(output["response"])
    return output['response']

if __name__ == "__main__":
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


