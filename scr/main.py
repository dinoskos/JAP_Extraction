import os
import glob
from pathlib import Path
from extraction import Extraction
from meta_data import MetaData

if __name__ == "__main__":
    # Get the data folder path
    data_folder = Path.cwd().parent / "data"

    # Find all PDF files in the data folder
    pdf_files = glob.glob(str(data_folder / "*.pdf"))

    # Initialize MetaData class
    meta_data = MetaData()

    # Iterate through each PDF file and extract author names and publication year
    for pdf_file in pdf_files:
        print(f"Processing file: {pdf_file}")

        # Initialize the Extraction class for the current PDF
        extractor = Extraction(path=pdf_file)

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
                    new_file_path = data_folder / new_file_name

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




