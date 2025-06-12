from __future__ import annotations

import json
import logging
import os
from typing import Iterable, List

from PIL import Image
import google.generativeai as genai

logger = logging.getLogger(__name__)

API_KEY_ENV = "GEMINI_API_KEY"


def configure_api(api_key: str | None = None) -> None:
    """Configure the Gemini API with the provided key or environment variable."""
    key = api_key or os.getenv(API_KEY_ENV)
    if not key:
        raise ValueError("API key for Gemini is missing")
    genai.configure(api_key=key)


def extract_section(images: Iterable[Image.Image], section: str = "4.8 Undesirable effects") -> tuple[str, int]:
    """Call Gemini API to extract a section from the document images.

    Returns a tuple of the content and the number of tokens used.
    """
    model = genai.GenerativeModel("gemini-pro-vision")
    prompt = (
        "Extract the text from section '" + section + "' in the following document. "
        "Return ONLY a JSON object with a single key 'content'."
    )
    logger.info("Sending request to Gemini API for section %s", section)
    response = model.generate_content([prompt, *images], stream=False)
    tokens = response.usage_metadata.total_tokens if response.usage_metadata else 0
    try:
        data = json.loads(response.text)
        content = data.get("content", "")
    except json.JSONDecodeError:
        content = response.text
    return content, tokens
