# PDF Metadata Extractor

## Overview

This project extracts metadata from PDF files and renames them according to APA conventions based on author names and publication years. It processes PDF files in a specified directory, extracts DOIs from the content, fetches metadata using the Crossref API, and renames the files to follow APA formatting.

## Features

- Extracts text from PDF files using the PyPDF2 library.
- Identifies DOIs from the extracted text.
- Retrieves metadata (author names and publication year) from Crossref.
- Renames PDF files in the specified folder based on APA naming conventions:
  - **One author:** `lastname_year.pdf`
  - **Two authors:** `lastname1_&_lastname2_year.pdf`
  - **Three or more authors:** `lastname1_et_al_year.pdf`

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - PyPDF2
  - requests
  - ratelimit

Install the required packages:

```bash
pip install PyPDF2 requests ratelimit
```

## How It Works

1. **PDF Text Extraction:** The script extracts text from the first page of each PDF file in the specified folder.
2. **DOI Identification:** It searches for a DOI in the extracted text using a regular expression.
3. **Metadata Retrieval:** Using the identified DOI, the script retrieves author names and the publication year from Crossref.
4. **File Renaming:** The PDF files are renamed based on APA conventions, depending on the number of authors and publication year.

## Usage

1. Place all PDF files in a directory named `data`, located one level above the script directory.
2. Run the main script:
```bash
python main.py
```
3. The script will process each PDF, extract the metadata, and rename the files based on APA conventions.

## Example Output
For a PDF with:

1. One author named "John Doe" and published in 2020, the file is renamed to: **Doe_2020.pdf**
2. Two authors named "Jane Smith" and "Alice Johnson" published in 2019, the file is renamed to: **Smith_&_Johnson_2019.pdf**
3. Three authors named "Robert Brown," "Emily Clark," and "Michael Davis" published in 2021, the file is renamed to: **Brown_et_al_2021.pdf**