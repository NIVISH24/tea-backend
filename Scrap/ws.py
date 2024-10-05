import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import os

def search_and_save_to_pdf(query, search_engine='google', directory='data'):
    # Create the directory if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Prepare the search URL based on the chosen search engine
    if search_engine == 'google':
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    elif search_engine == 'bing':
        url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
    else:
        raise ValueError("Unsupported search engine. Use 'google' or 'bing'.")

    # Send a GET request to the search engine
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to retrieve search results.")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the search results based on the search engine
    results = []
    if search_engine == 'google':
        for g in soup.find_all('div', class_='BVG0Nb'):
            title = g.find('h3').text if g.find('h3') else 'No Title'
            link = g.find('a')['href'] if g.find('a') else 'No Link'
            results.append((title, link))
    elif search_engine == 'bing':
        for g in soup.find_all('li', class_='b_algo'):
            title = g.find('h2').text if g.find('h2') else 'No Title'
            link = g.find('a')['href'] if g.find('a') else 'No Link'
            results.append((title, link))

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Search Results for: {query}", ln=True, align='C')
    pdf.ln(10)  # Add a line break

    for title, link in results:
        pdf.cell(0, 10, txt=title, ln=True, link=link)
        pdf.cell(0, 10, txt=link, ln=True)
        pdf.ln(5)  # Add space between results

    pdf_file_path = os.path.join(directory, f"{query.replace(' ', '_')}.pdf")
    pdf.output(pdf_file_path)

    print(f"PDF saved to {pdf_file_path}")

