# Get an input from the user and scrape the data from the website and convert into pdf and save it in ./data folder

import requests
from bs4 import BeautifulSoup
from googlesearch import search

def get_first_link(query):
    # Perform Google search and return the first link
    try:
        for url in search(query):
            return url
    except Exception as e:
        print(f"Error during Google search: {e}")
        return None

def extract_text_from_url(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text (you can refine this based on the specific structure of the page)
        paragraphs = soup.find_all('p')
        text_content = '\n'.join([para.get_text() for para in paragraphs])
        
        return text_content

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

if __name__ == "__main__":
    query = input("Enter your search query: ")
    first_link = get_first_link(query)
    
    if first_link:
        print(f"First link found: {first_link}")
        text_content = extract_text_from_url(first_link)
        
        if text_content:
            print("Extracted Text:")
            print(text_content)