from PIL import Image


def stitch(images: list[Image.Image]) -> Image.Image:
    background_width = max([image.width for image in images])
    background_height = sum([image.height for image in images])
    background = Image.new(mode="1", size=(background_width, background_height))
    y = 0
    for image in images:
        background.paste(image, (0, y))
        y += image.height

    return background
