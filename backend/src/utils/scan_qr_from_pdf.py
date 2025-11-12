import logging

import fitz


logger = logging.getLogger(__name__)

output_jpg = r"merged_pdf.jpg"


# The code splits the first page of pdf and converts to jpeg
def split_and_convert(bytes):
    doc = fitz.open(stream=bytes)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    pix.save(output_jpg, "jpeg")
    doc.close()


logger.info("Done!")
