from pathlib import Path
from meta_data import MetaData

if __name__ == "__main__":
    # Get the data folder path
    data_folder = Path.cwd().parent / "data"

    # Process all PDFs in the folder
    MetaData.replace_name(data_folder)
