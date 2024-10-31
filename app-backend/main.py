from LLM import search_suggestions, generate_subheadings_and_related_topics, generate_topic_name, generate_content
from scrape import scrape_and_save_to_pdf
from RAG2 import query_rag
import ollama

prompt = """Teach me these concepts
Module:1 Introduction to Statistics 6 hours
Statistics and data analysis; Measures of central tendency; Measure of Dispersion,
Moments-Skewness-Kurtosis (Concepts only).
Module:2 Random variables 8 hours
Random variables- Probability mass function, distribution and density functions-Joint
probability distribution and Joint density functions; Marginal, Conditional distribution and
Density functions- Mathematical expectation and its properties- Covariance, Moment
generating function.
Module:3 Correlation and Regression 4 hours
Correlation and Regression – Rank Correlation; Partial and Multiple correlation; Multiple
regression.
Module:4 Probability Distributions 7 hours
Binomial distribution; Poisson distributions; Normal distribution; Gamma distribution;
Exponential distribution; Weibull distribution.
Module:5 Hypothesis Testing-I 4 hours

Testing of hypothesis –Types of errors - Critical region, Procedure for testing of hypothesis-
Large sample tests- Z test for Single Proportion- Difference of Proportion- Mean and

difference of means.
Module:6 Hypothesis Testing-II 9 hours
Small sample tests- Student’s t-test, F-test- chi-square test- goodness of fit - independence
of attributes- Design of Experiments - Analysis of variance – One way-Two way-Three way
classifications - CRD-RBD- LSD.
Module:7 Reliability 5 hours
Basic concepts- Hazard function-Reliabilities of series and parallel systems- System
Reliability - Maintainability-Preventive and repair maintenance- Availability."""

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
response = ollama.generate(model="llama3.2", prompt=f"{response} \n\n convert this to python list of strings and nothing else, no explanations eg:['subheading1', 'subheading2', ...]")
output = (response["response"])
output = output[output.find('['):output.find(']')+1]
response = eval(output)


region = "Chennai, TN, India"
age = 20
interests = ["pursuing 3rd year engineering at VIT University", "Coder, Programmer, Tech enthusiast"]
content = [generate_content(i, region, age, interests) for i in response]

# save this to separate text files

for i, c in enumerate(content):
    with open(f"{response[i]}.txt", "w") as f:
        f.write(c)
        print(f"Content for {response[i]} saved to {response[i]}.txt")
        
