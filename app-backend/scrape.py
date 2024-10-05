import os
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from fpdf import FPDF

def scrape_and_save_to_pdf(query):
    try:
        # Perform Google search and get the first link
        first_link = next(search(query))
        print(f"First link found: {first_link}")
        
        # Send a GET request to the URL
        response = requests.get(first_link)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text_content = '\n'.join([para.get_text() for para in paragraphs])

        print("Extracted Text:")
        print(text_content)

        # Ensure the data folder exists
        os.makedirs('./data', exist_ok=True)

        # Save the text content to a PDF using fpdf2
        pdf_filename = f"./data/{query.replace(' ', '_')}.pdf"
        pdf = FPDF()
        pdf.add_page()
        
        # Set font to a TTF font for better Unicode support
        pdf.add_font("Arial", "", "arial.ttf")  # Make sure arial.ttf is in the same directory or provide a correct path
        pdf.set_font("Arial", size=12)

        # Define maximum width for the multi-cell
        max_width = 190  # Adjust as necessary, considering page margins

        # Add text to PDF with consideration for long lines
        for line in text_content.split('\n'):
            if len(line) > 0:
                pdf.multi_cell(max_width, 10, line)  # Use multi_cell for wrapping

        # Save the PDF to the specified filename
        pdf.output(pdf_filename)
        print(f"PDF saved as: {pdf_filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    query = input("Enter your search query: ")
    scrape_and_save_to_pdf(query)
