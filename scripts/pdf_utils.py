from __future__ import annotations

import os
from pathlib import Path
from typing import List

from pdf2image import convert_from_path
from PIL import Image


def pdf_to_images(pdf_path: str | Path) -> List[Image.Image]:
    """Convert a PDF file to a list of PIL Images."""
    return convert_from_path(str(pdf_path))


def merge_images(images: List[Image.Image], max_pages: int = 4, orientation: str = "vertical") -> List[Image.Image]:
    """Merge groups of images together either vertically or horizontally."""
    merged = []
    for i in range(0, len(images), max_pages):
        group = images[i : i + max_pages]
        widths, heights = zip(*(img.size for img in group))
        if orientation == "vertical":
            total_width = max(widths)
            total_height = sum(heights)
            new_img = Image.new("RGB", (total_width, total_height))
            y_offset = 0
            for img in group:
                new_img.paste(img, (0, y_offset))
                y_offset += img.height
        else:
            total_width = sum(widths)
            total_height = max(heights)
            new_img = Image.new("RGB", (total_width, total_height))
            x_offset = 0
            for img in group:
                new_img.paste(img, (x_offset, 0))
                x_offset += img.width
        merged.append(new_img)
    return merged
