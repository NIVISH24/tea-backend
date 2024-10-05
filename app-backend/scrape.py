import requests
from bs4 import BeautifulSoup
from googlesearch import search
from fpdf import FPDF
import os

def search_and_save_as_pdf(query, output_folder='./data'):
    try:
        # Perform Google search and get the first link
        first_link = next(search(query))
        print(f"First link found: {first_link}")

        # Send a GET request to the URL
        response = requests.get(first_link)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text (you can refine this based on the specific structure of the page)
        paragraphs = soup.find_all('p')
        text_content = '\n'.join([para.get_text() for para in paragraphs])

        # Create a PDF document
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        # Add text content to the PDF
        for line in text_content.split('\n'):
            pdf.multi_cell(0, 10, line)

        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Save the PDF to the specified folder
        output_path = os.path.join(output_folder, 'output.pdf')
        pdf.output(output_path)
        print(f"PDF saved to {output_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    query = input("Enter your search query: ")
    search_and_save_as_pdf(query)