import pypdfium2 as pdfium
from pypdfium2._helpers.bitmap import PdfBitmap

from .decorators import timing


@timing
def convert_pdf_to_images(bytes):
    pdf = pdfium.PdfDocument(bytes)
    images = []
    for page_number in range(len(pdf)):
        page = pdf.get_page(page_number)
        pil_image = page.render(
            scale=2,
            rotation=0,
            crop=(0, 0, 0, 0),
            may_draw_forms=True,
            bitmap_maker=PdfBitmap.new_native,
            color_scheme=None,
            fill_to_stroke=False,
            grayscale=True,
            optimize_mode="lcd",
        ).to_pil()
        images.append(pil_image)

    return images
