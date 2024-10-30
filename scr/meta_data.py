import os
import requests
import glob
from pathlib import Path
from extraction import Extraction
from ratelimit import limits, sleep_and_retry


class MetaData:
    def __init__(self):
        pass

    @sleep_and_retry
    @limits(calls=3, period=1)
    def crossref_request(self, doi: str) -> [list, int]:

        # Getting url of request
        url = f"https://api.crossref.org/works/{doi}"

        try:
            # Retrieving response
            response = requests.get(url)

            # Retrieving metadata
            if response.status_code == 200:
                data = response.json()
                # Extract the author names and publication year
                authors = data['message'].get('author', [])
                publication_year = data['message'].get('issued', {}).get('date-parts', [[None]])[0][0]

                # Extract author names
                author_names = [f"{author['given']} {author['family']}" for author in authors if
                                'given' in author and 'family' in author]

                print(author_names, publication_year)
                return author_names, publication_year
            else:
                print(f"Error: {response.status_code} - {response.text}")
                print(None, None)

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as e:
            print(f"Error: {e}")

        return None, None

    @staticmethod
    def format_apa_file_name(authors, publication_year):
        """
        Formats the file name according to the APA convention.
        """
        if len(authors) == 1:
            # Single author: last_name, year
            new_name = f"{authors[0].split()[-1]}_{publication_year}.pdf"
        elif len(authors) == 2:
            # Two authors: last_name1 & last_name2, year
            new_name = f"{authors[0].split()[-1]}_&_{authors[1].split()[-1]}_{publication_year}.pdf"
        else:
            # Three or more authors: last_name1 et al., year
            new_name = f"{authors[0].split()[-1]}_et_al_{publication_year}.pdf"

        return new_name

    @staticmethod
    def replace_name(data_folder):
        """
        Iterates through PDF files, extracts metadata, and renames them based on APA formatting.
        """
        # Find all PDF files in the data folder
        pdf_files = list(Path(data_folder).rglob("*.pdf"))

        # Initialize the MetaData class
        meta_data = MetaData()

        # Iterate through each PDF file
        for pdf_file in pdf_files:
            print(f"Processing file: {pdf_file}")

            # Initialize the Extraction class for the current PDF
            extractor = Extraction(path=str(pdf_file))

            # Extract text from the first page (or modify the page range as needed)
            text = extractor.pdf_extraction(pages=0)  # Extract from the first page

            if text:
                # Extract DOI from the text
                doi = extractor.doi_extraction(text)

                if doi:
                    # Get author names and publication year using the DOI
                    authors, publication_year = meta_data.crossref_request(doi)

                    if authors and publication_year:
                        print(f"Authors: {authors}, Year: {publication_year}")

                        # Format new file name using the MetaData class method
                        new_file_name = meta_data.format_apa_file_name(authors, publication_year)

                        # Define the new file path
                        new_file_path = pdf_file.parent / new_file_name

                        # Rename the PDF file to the new APA-style file name
                        try:
                            os.rename(pdf_file, new_file_path)
                            print(f"Renamed to: {new_file_path}")
                        except FileExistsError:
                            print(f"File already exists: {new_file_path}, skipping renaming.")
                        except Exception as e:
                            print(f"Error renaming file: {e}")
                    else:
                        print("Failed to retrieve metadata from Crossref.")
                else:
                    print("No DOI found in the PDF text.")
            else:
                print("Failed to extract text from the PDF.")
