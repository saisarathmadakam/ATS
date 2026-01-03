# ATS — ATS Analyzer

A small project that analyzes resumes against job descriptions using a simple Flask API and the Gemini LLM for parsing and scoring.

---

## Table of contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation & Dependencies](#installation--dependencies)
- [Configuration](#configuration)
- [How it works (functions)](#how-it-works-functions)
- [API Usage](#api-usage)
- [Examples](#examples)
- [Security & Secrets](#security--secrets)
- [Development & Contributing](#development--contributing)
- [FAQ & Troubleshooting](#faq--troubleshooting)
- [License](#license)

---

## Overview

This project extracts text from uploaded PDF resumes, parses resume content and job descriptions using a generative model, and produces an ATS-style analysis and score comparing resume to the job description.

## Features

- Extract text from PDF resumes using `PyPDF2`
- Parse resumes and job descriptions using Gemini LLM prompts
- Compare resume against a job description and return a structured score and recommendations
- Simple web UI (`templates/index.html`) and a JSON API endpoint (`/analyze`)

---

## 🚀 Quick Start

1. Create and activate a Python virtual environment (Windows PowerShell):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Set your Gemini API key in a local `.env` file (see Configuration):

   ```text
   GEMINI_API_KEY=sk-...
   ```

3. Run the app:

   ```powershell
   python python.py
   ```

4. Open `http://localhost:5000` to use the simple front-end or call the `/analyze` endpoint programmatically.

---

## Installation & Dependencies

Required packages (example):

- Flask
- google-genai (or `google` package the code imports) — Gemini client
- PyPDF2
- python-dotenv

Install them via:

```bash
pip install Flask PyPDF2 python-dotenv google-genai
```

(If your environment uses a different Gemini client package name, please install the recommended client and update `python.py` accordingly.)

---

## Configuration

- Create a `.env` file in the repo root and add your Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

- `.env` is included in `.gitignore`. Do NOT commit secrets.

---

## How it works (functions)

This section documents the main functions defined in `python.py` and how they are used.

### extract_text_from_pdf(file)

- Purpose: Extracts and concatenates text from each page of an uploaded PDF file.
- Input: `file` — a file-like object (uploaded via Flask `request.files`).
- Output: `str` — the extracted text.
- Notes: Uses `PyPDF2.PdfReader` and safely handles empty page text.

### parse_resume(resume_text)

- Purpose: Sends a prompt to the Gemini LLM to extract structured resume fields (skills, experience, education) from raw resume text.
- Input: `resume_text` — raw text extracted from a resume PDF.
- Output: `str` — text response from the LLM containing structured resume information.
- Notes: The prompt expects the model to return labelled fields in the format:

```
SKILLS:
EXPERIENCE:
EDUCATION:
```

### parse_job_description(jd_text)

- Purpose: Sends a prompt to the LLM to extract required skills and qualifications from a job description.
- Input: `jd_text` — raw job description text.
- Output: `str` — LLM response in a structured format:

```
REQUIRED_SKILLS:
REQUIREMENTS:
```

### ats_analysis(resume_text, jd_text=None)

- Purpose: Compares the parsed resume (and optionally parsed job description) to produce an ATS-style evaluation.
- Behavior:
  - Calls `parse_resume` and optionally `parse_job_description`.
  - Constructs a strict evaluation prompt asking the LLM to return a fixed structured output.
  - If a job description is provided, the response format includes `SCORE`, `PROS`, `CONS`, `MATCHED_SKILLS`, `MISSING_SKILLS`, and `RECOMMENDATIONS`.
  - If no job description is provided, the response format includes `SCORE`, `PROS`, `CONS`, `CRITICAL_ISSUES`, `MISSING_KEYWORDS`, and `RECOMMENDATIONS`.
- Output: `str` — the LLM-produced ATS analysis text.

### Flask routes

- `GET /` — serves `templates/index.html` (basic front-end form).
- `POST /analyze` — accepts a multipart form with keys:
  - `file` — the resume PDF file (required)
  - `job_description` — optional text field containing the JD

Response: JSON `{"result": <string>}` on success or `{"error": "..."}` on failure.

---

## API Usage

Example curl call (replace `resume.pdf` and the URL if needed):

```bash
curl -X POST "http://localhost:5000/analyze" \
  -F "file=@resume.pdf" \
  -F "job_description=Example job description text"
```

Response (example):

```json
{ "result": "SCORE: 78/100\nPROS:\n- strong experience in X\n..." }
```

---

## Examples & Tips

- For local testing, create a small `.env` with a valid Gemini key and test using the curl request above.
- Use `templates/index.html` to manually upload PDF resumes.
- If you frequently test with many resumes, consider adding caching or rate-limiting to avoid excessive LLM usage.

---

## Security & Secrets

- **Rotate** any credentials if they were ever exposed in the repo history.
- Never check-in `.env` or secrets. Use a secret manager for production deployments (GitHub Secrets, Azure Key Vault, AWS Secrets Manager).

---

## Development & Contributing

- Run locally and edit `python.py` to change prompts or add more robust parsing logic.
- Add unit tests for `extract_text_from_pdf` (use small sample PDFs) and for `ats_analysis` by mocking the LLM client.
- Open issues or PRs describing your changes.

---

## FAQ & Troubleshooting

Q: I see an import error for `google.genai` or a different Gemini client.
A: Install the correct Gemini client package or update the import and client initialization to match your installed package.

Q: My PDF text extraction returns empty strings.
A: Some PDFs are image-based (scans). For scanned PDFs you may need OCR (e.g., Tesseract + pytesseract) before parsing.

---

## License

This project is licensed under the terms in the `LICENSE` file.

---

If you'd like, I can also add example unit tests, a sample `.env.example`, and a more detailed troubleshooting section for the most common LLM/credential errors.
