# Pipeline_MLKG2025

This repository contains utilities for processing a folder of PDF files and extracting data from section **4.8 Undesirable effects** using the Gemini API.

## Setup

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main script specifying the folder containing PDF files and your Gemini API key:

```bash
python -m scripts.process_pdfs /path/to/pdfs --api-key YOUR_API_KEY
```

Results will be written to `results.json` and logs to `process.log`.

