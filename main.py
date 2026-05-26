from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

from converter import (
    convert_pdf_to_pngs,
    convert_tiff_to_pngs
)

from chandra_runner import run_chandra

from langflow_client import (
    LangflowExtractor
)


INPUT_FILE = (
    "invoice.tif"
)

LANGFLOW_API = os.getenv(
    "LANGFLOW_API"
)

LANGFLOW_API_KEY = os.getenv(
    "LANGFLOW_API_KEY"
)


def main():

    input_path = Path(INPUT_FILE)

    suffix = input_path.suffix.lower()

    page_files = []

    # TIFF
    if suffix in [".tif", ".tiff"]:

        page_files = (
            convert_tiff_to_pngs(
                input_path,
                "temp_pages"
            )
        )

    # PDF
    elif suffix == ".pdf":

        page_files = (
            convert_pdf_to_pngs(
                input_path,
                "temp_pages"
            )
        )

    # PNG/JPG
    else:
        page_files = [str(input_path)]

    full_markdown = ""

    # Run Chandra on every page
    for page_file in page_files:

        markdown_path = run_chandra(
            page_file,
            "outputs"
        )

        with open(
            markdown_path,
            "r",
            encoding="utf-8"
        ) as f:

            full_markdown += (
                f.read() + "\n"
            )

    # Send markdown to Langflow
    extractor = LangflowExtractor(
        LANGFLOW_API,
        LANGFLOW_API_KEY
    )

    result = extractor.extract_fields(
        full_markdown
    )

    print(result)


if __name__ == "__main__":
    main()
