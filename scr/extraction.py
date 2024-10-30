from logging import raiseExceptions

from PyPDF2 import PdfReader
import re


class Extraction:
    def __init__(self, path: str, file_type: str = 'pdf', *args, **kwargs):
        self.path = path
        self.file_type = file_type

    #TODO: modify the code to accept a list of page. For now, single page is accepted
    def pdf_extraction(self, pages: [int, list], *args, **kwargs) -> [str, None]:
        """
        Function to extract pdf from given path

        :param pages: Can be an int (single page), list (specific pages)
        :param args:
        :param kwargs:
        :return: text if pages are found else None
        """
        try:
            with open(self.path, 'rb') as pdf_file:
                # Create a pdf object
                pdf_reader = PdfReader(pdf_file)

                # Check if the pdf has page > 0
                if len(pdf_reader.pages) > 0:
                    # Extract the first page
                    first_page = pdf_reader.pages[pages]

                    # Extract text from selected page
                    text = first_page.extract_text()

                    return text
                else:
                    print(f'The PDF has no pages')
                    return None
        except FileNotFoundError:
            print(f'Error: File not found at path {self.path}')
            return None
        except Exception as e:
            print(f'Error: {e}')
            return None

    def doi_extraction(self, text: str, *args, **kwargs) -> str:
        """
        Function to extract doi from given text. Used this as a standalone function
        or after extracting text through pdf

        :param text: document with doi to be extracted
        :param args:
        :param kwargs:
        :return: string of article's doi
        """
        # Define regrex pattern for doi
        doi_pattern = r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+"

        # Search for doi in the text
        doi_match = re.search(doi_pattern, text, re.IGNORECASE)

        if doi_match:
            # Extract and clean the DOI by removing trailing components
            full_doi = doi_match.group(0)
            clean_doi = re.sub(r'\.supp.*$', '', full_doi, flags=re.IGNORECASE)  # Remove '.supp' and anything after
            return clean_doi
        else:
            raise Exceptions(f'Text does not contain doi code')