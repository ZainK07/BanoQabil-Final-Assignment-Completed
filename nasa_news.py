# Scrapping NASA By Using Phython Programming.

import csv
import requests
from bs4 import BeautifulSoup
import re

total_pages = 49  # Total number of pages to process

# Define CSV header
csv_header = ["Category", "Title", "Content"]

print("Initializing Connection, Please Standby...")

with open("nasa_news.csv", "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write header row
    csv_writer.writerow(csv_header)

    for count in range(1, total_pages + 1):
        try:
            response = requests.get(f"https://www.nasa.gov/news/all-news/page/{count}/")
            response.raise_for_status()  # Raise exception for bad status codes
        except requests.RequestException as e:
            print(f"Failed to fetch page {count}...")
            continue

        soup = BeautifulSoup(response.content, "html.parser")

        last_page_link = soup.find("a", class_="page-link", title="Go to last page")
        if last_page_link:
            last_page = int(last_page_link.text)
        else:
            last_page = count

        entry_contents = soup.find_all("div", class_="entry-content")
        print(f"Processing page {count}...")

        for entry_content in entry_contents:
            content_text = entry_content.get_text(strip=True)
            sentences = re.split(r'(?<=[.!?]) +', content_text)

            # Extracting category and title
            first_sentence = sentences[0]
            category_end_index = first_sentence.find("NASA")
            category = first_sentence[:category_end_index].strip()
            title = first_sentence[category_end_index:].strip()

            # Write each sentence to the CSV file
            for sentence in sentences[1:]:
                csv_writer.writerow([category, title, sentence.strip()])

        # Calculate and print loading percentage
        loading_percentage = (count / total_pages) * 100
        print(f"Parsed: {loading_percentage:.2f}%")

print("Data processing completed.")
