# AI-Assisted Resume Portfolio Generator

An AI-powered tool that converts a plain-text resume into a fully generated portfolio webpage. Built as part of the AIML GLA Bootcamp '26.

---

## Overview

This project reads a candidate's resume from a plain text file, sends it to Google's Gemini API with a tightly controlled prompt, receives structured JSON in return, and uses that data to auto-generate a clean, styled `portfolio.html` page — without any manual copy-pasting of AI output.

```
resume.txt  →  Python (main.py)  →  Gemini API  →  Structured JSON  →  HTML template  →  portfolio.html
```

---

## Features

- Reads and validates resume text from `resume.txt` (handles missing/empty/too-short files gracefully)
- Sends a strict, controlled prompt to Gemini — instructed to use only information present in the resume, never invent details
- Parses and validates the JSON response safely, with error handling for malformed output
- Automatically injects the parsed data into a separate HTML/CSS template (no manual editing of the final file)
- Hides or leaves empty any section with no corresponding resume data
- Fully tested against required edge cases (see [Testing](#testing) below)

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | File I/O, API calls, JSON processing, HTML generation |
| Gemini API (`google-genai`, Interactions API) | Extracts and structures resume content |
| JSON | Intermediate structured data format |
| HTML / CSS | Portfolio webpage and styling |
| GitHub | Version control and submission |

---

## Project Structure

```
resume-portfolio-generator/
│
├── main.py              # Core Python program
├── resume.txt             # Sample resume input (plain text)
├── template.html           # HTML skeleton with placeholder tags
├── style.css               # Portfolio styling
├── requirements.txt         # Python dependencies
├── .env.example              # Example environment file (no real key)
├── .gitignore                  # Excludes venv, .env, cache files
├── portfolio.html               # Auto-generated final output
├── index.html                    # Copy of portfolio.html, used for Vercel hosting
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/resume-portfolio-generator.git
cd resume-portfolio-generator
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your Gemini API key
1. Get a free API key from [Google AI Studio](https://aistudio.google.com/).
2. Create a `.env` file in the project root (copy `.env.example` as a starting point):
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```
3. **Never commit your real `.env` file or paste your key into `.env.example`.**

### 5. Add your resume
Replace the contents of `resume.txt` with your own resume as plain text.

---

## Running the Project

```bash
python main.py
```

Expected console output:
```
📄 Reading resume.txt ...
🧠 Building prompt and calling Gemini ...
🔍 Parsing JSON response ...
🏗️  Generating portfolio.html ...
✅ portfolio.html generated successfully! Open it in your browser.
```

Open `portfolio.html` in any browser to view the generated portfolio.

---

## Workflow

1. `resume.txt` is read and cleaned (extra whitespace and blank lines removed).
2. Input is validated — the program exits safely with a clear message if the file is missing or too short.
3. A structured prompt is built and sent to the Gemini API via `client.interactions.create()`.
4. The raw response is cleaned (in case of stray markdown fences) and parsed as JSON.
5. Parsed data is injected into `template.html` by replacing placeholder tags (e.g. `{{name}}`, `{{skills}}`).
6. The final page is saved as `portfolio.html`.

---

## Prompt Design

The prompt sent to Gemini enforces the following rules:
- Use only information explicitly present in the resume text.
- Never invent skills, companies, dates, projects, achievements, or links.
- Use empty strings/lists for any missing information rather than guessing.
- Return valid JSON only — no markdown formatting, no explanatory text.
- Keep the professional summary concise and factual.

The expected JSON structure covers: `name`, `headline`, `summary`, `skills`, `education`, `experience`, `projects`, `achievements`, and `contact`.

---

## Testing

The following required test cases were run against `main.py`:

| # | Test Case | Expected Behavior | Result |
|---|---|---|---|
| 1 | Missing `resume.txt` | Clear error, safe exit | ✅ Pass |
| 2 | Empty / very short resume | Rejected with a clear message | ✅ Pass |
| 3 | Valid resume | `portfolio.html` generated successfully | ✅ Pass |
| 4 | Resume with missing sections | Generates available sections only, no invented data | ✅ Pass |
| 5 | Missing API key | Clear configuration error | ✅ Pass |
| 6 | API failure (invalid key) | Error handled without crashing | ✅ Pass |
| 7 | Invalid JSON response | Handled via try/except in `parse_json_response()` | ✅ Pass |

*(Screenshots of each test run are included in the `/screenshots` folder — add this folder if not already present.)*

---

## Responsible AI & Privacy Notes

- All generated content was manually cross-checked against the original resume before submission — no invented skills, dates, or achievements were included.
- The sample `resume.txt` in this repo contains no sensitive personal information (no passwords, ID numbers, or financial details).
- The Gemini API is called only from the Python backend — never from client-side JavaScript — so the API key is never exposed to a browser.
- The real API key is stored in a local `.env` file, which is excluded from version control via `.gitignore`.

---

## Limitations & Hallucination Risks

- Gemini's output is a draft and may occasionally misread poorly formatted or ambiguous resumes (e.g. mixing up experience and project sections).
- The system prompt reduces but cannot fully eliminate the risk of AI hallucination — manual verification of generated content against the source resume is required before publishing.
- Gemini's available models and SDKs are updated periodically by Google; if a "model not found" error occurs, check the [Gemini API docs](https://ai.google.dev/gemini-api/docs) for the current recommended model name and SDK version.

---

## AI Development Tools Used

| Tool | Purpose |
|---|---|
| Google Antigravity | Generated and iterated on `template.html` and `style.css` |
| Claude | Assisted with debugging, migrating to the current Gemini SDK/API, and general troubleshooting |
| Gemini API | Core resume-to-JSON extraction logic (the project's primary function, not a dev tool) |

All AI-generated code was reviewed, tested, and understood before inclusion in this project.

---

## Optional Enhancements

- [x] Deployed the generated portfolio via Vercel
- [ ] Additional CSS themes
- [ ] Second HTML portfolio template
- [ ] Additional sections (certifications, languages, interests)

---

## License

This project was built for educational purposes as part of the AIML GLA Bootcamp '26.
