from __future__ import annotations

import json
from pathlib import Path
from typing import List

from PIL import Image

from .pdf_utils import pdf_to_images, merge_images
from .gemini_api import configure_api, extract_section
from .logger_config import setup_logger


RESULTS_FILE = "results.json"
LOG_FILE = "process.log"
IMAGES_DIR = "images"


def process_pdf(pdf_path: Path, logger) -> dict:
    images = pdf_to_images(pdf_path)
    merged = merge_images(images, max_pages=4, orientation="vertical")
    image_paths: List[Path] = []
    Path(IMAGES_DIR).mkdir(exist_ok=True)
    for idx, img in enumerate(merged):
        img_path = Path(IMAGES_DIR) / f"{pdf_path.stem}_{idx}.png"
        img.save(img_path)
        image_paths.append(img_path)

    pil_images = [Image.open(p) for p in image_paths]
    content, tokens = extract_section(pil_images)
    logger.info("Processed %s - tokens: %s", pdf_path.name, tokens)
    return {"pdf": str(pdf_path), "content": content, "tokens": tokens}


def main(pdf_folder: str, api_key: str | None = None) -> None:
    configure_api(api_key)
    logger = setup_logger(LOG_FILE)
    results = []
    for pdf_file in Path(pdf_folder).glob("*.pdf"):
        try:
            result = process_pdf(pdf_file, logger)
            results.append(result)
        except Exception as exc:
            logger.error("Failed processing %s: %s", pdf_file, exc)
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process PDFs and extract section 4.8")
    parser.add_argument("pdf_folder", help="Folder containing PDF files")
    parser.add_argument("--api-key", help="Gemini API key", default=None)
    args = parser.parse_args()
    main(args.pdf_folder, args.api_key)
