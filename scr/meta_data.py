from extraction import Extraction
from ratelimit import limits, sleep_and_retry
import requests

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

