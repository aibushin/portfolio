from arepl_dump import dump  # type: ignore  # noqa: F401
from pyzbar import pyzbar
from PIL import Image

image = Image.open("/app/src/utils/pdf/app/images/last_merged_images/20250312-175839_improved.png")
# res = pyzbar.decode(image, symbols=[pyzbar.ZBarSymbol.QRCODE])

res = pyzbar.decode(image, symbols=[pyzbar.ZBarSymbol.QRCODE])

result = [r.data for r in res]

for r in res:
    print(r.data)
