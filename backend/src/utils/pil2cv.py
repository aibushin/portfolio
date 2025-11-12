from PIL import Image

import numpy as np
import cv2


def pil2cv(image: Image) -> np.ndarray:  # noqa: C901
    mode = image.mode
    new_image: np.ndarray

    match mode:
        case "1":
            new_image = np.array(image, dtype=np.uint8)
            new_image *= 255
        case "L":
            new_image = np.array(image, dtype=np.uint8)
        case "LA" | "La":
            new_image = np.array(image.convert("RGBA"), dtype=np.uint8)
            new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
        case "RGB":
            new_image = np.array(image, dtype=np.uint8)
            new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
        case "RGBA":
            new_image = np.array(image, dtype=np.uint8)
            new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
        case "LAB":
            new_image = np.array(image, dtype=np.uint8)
            new_image = cv2.cvtColor(new_image, cv2.COLOR_LAB2BGR)
        case "HSV":
            new_image = np.array(image, dtype=np.uint8)
            new_image = cv2.cvtColor(new_image, cv2.COLOR_HSV2BGR)
        case "YCbCr":
            new_image = np.array(image, dtype=np.uint8)
            new_image = cv2.cvtColor(new_image, cv2.COLOR_YCrCb2BGR)
        case "P" | "CMYK":
            new_image = np.array(image.convert("RGB"), dtype=np.uint8)
            new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
        case "PA" | "Pa":
            new_image = np.array(image.convert("RGBA"), dtype=np.uint8)
            new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
        case _:
            raise ValueError(f"unhandled image color mode: {mode}")

    return new_image
