from PIL import Image
import fitz
from pathlib import Path


def convert_tiff_to_pngs(
    input_path,
    output_dir
):

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    img = Image.open(input_path)

    generated = []

    index = 0

    while True:

        try:
            img.seek(index)

            page = img.copy()

            output_path = (
                output_dir /
                f"page_{index + 1}.png"
            )

            page.save(output_path)

            generated.append(
                str(output_path)
            )

            index += 1

        except EOFError:
            break

    return generated


def convert_pdf_to_pngs(
    pdf_path,
    output_dir
):

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    doc = fitz.open(pdf_path)

    generated = []

    for page_num in range(len(doc)):

        page = doc.load_page(page_num)

        pix = page.get_pixmap(
            matrix=fitz.Matrix(2, 2)
        )

        image_path = (
            output_dir /
            f"page_{page_num + 1}.png"
        )

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        img.save(image_path)

        generated.append(
            str(image_path)
        )

    return generated