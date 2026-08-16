<div align="center">

# 🧑‍💻 AI-Assisted Resume Portfolio Generator

### Turn any resume into a live portfolio webpage — powered by Gemini AI

A lightweight Python pipeline that reads a plain-text resume, sends it to **Google's Gemini API**
with a tightly controlled prompt, gets back clean structured **JSON**, and auto-generates a fully
styled **HTML/CSS** portfolio page — with zero manual copy-pasting of AI output.

[![Made with Python](https://img.shields.io/badge/Backend-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Powered by Gemini](https://img.shields.io/badge/AI-Gemini_API-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white)](https://ai.google.dev)
[![Built with Antigravity](https://img.shields.io/badge/Frontend-Google_Antigravity-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://antigravity.google)

</div>

---

## ✨ Overview

This project is an **AI-Assisted Resume Portfolio Generator** built as part of the **AIML GLA
Bootcamp '26 — Summer 2026** curriculum. It takes a candidate's raw resume text, extracts and
structures it using the Gemini API, and injects that structured data into an HTML template to
produce a ready-to-view portfolio page.

**No manual data entry. No copy-pasting AI output. No invented content.** Every generated field
is instructed to come strictly from the resume itself — nothing is fabricated.

```
resume.txt  →  Python (main.py)  →  Gemini API  →  Structured JSON  →  HTML Template  →  portfolio.html
```

---

## 🖥️ Live Demo

> Hosting was marked **optional** in the project requirements. This project focuses on the
> core resume → portfolio generation pipeline, run locally via Python.


---

## 🎯 Features

| Feature | Description |
|---|---|
| 📄 **Smart Resume Parsing** | Reads and cleans `resume.txt`, stripping extra whitespace and blank lines before processing |
| 🛡️ **Strict Input Validation** | Gracefully handles missing, empty, or too-short resumes with clear error messages instead of crashing |
| 🧠 **Controlled AI Prompting** | Gemini is explicitly instructed to use *only* resume content — no invented skills, dates, or companies |
| 🔍 **Safe JSON Parsing** | Cleans and validates the AI response, with error handling for malformed or non-JSON output |
| 🏗️ **Automatic HTML Generation** | Structured data is injected into a separate HTML/CSS template — no manual editing of the final file |
| 🕳️ **Graceful Empty Sections** | Sections with no resume data (e.g. no achievements) are left empty rather than filled with fake content |
| ✅ **Fully Tested** | Verified against 7 required edge cases — missing files, bad input, API failures, and more |

---

## 🏗️ Architecture

```
┌────────────────┐      ┌──────────────────────┐      ┌───────────────────────┐      ┌──────────────────┐
│   resume.txt    │      │      main.py          │      │   Gemini API           │      │  template.html    │
│ (plain text      │────▶│  Read → Clean →        │────▶│  Interactions API      │────▶│  + style.css       │
│  resume input)    │     │  Validate → Prompt      │     │  Returns structured    │     │  Placeholder tags  │
└────────────────┘      │  Build → Parse JSON     │      │  JSON only              │     │  get filled in →   │
                          └──────────────────────┘      └───────────────────────┘      │  portfolio.html    │
                                                                                          └──────────────────┘
```

1. **`resume.txt`** holds the raw resume as plain text
2. **`main.py`** reads, cleans, and validates the input, then builds a strict extraction prompt
3. The prompt is sent to **Gemini** (via `client.interactions.create()`), which returns structured JSON
4. The JSON is parsed and safely injected into **`template.html`** by replacing placeholder tags
5. The final result is saved as **`portfolio.html`**, ready to open in any browser

---

## 🧰 Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **AI Engine** | Gemini API (`google-genai`, Interactions API) |
| **Data Format** | JSON |
| **Frontend** | HTML5, CSS3 (built with Google Antigravity) |
| **Config Management** | `python-dotenv` |
| **Version Control** | GitHub |
| **Hosting (optional)** | Vercel |

</div>

---

## 📁 Project Structure

```
resume-portfolio-generator/
├── main.py                # Core pipeline: read → validate → prompt → parse → generate
├── resume.txt               # Sample resume input (plain text)
├── template.html             # HTML skeleton with {{placeholder}} tags
├── style.css                 # Portfolio styling
├── requirements.txt           # Python dependencies (google-genai, python-dotenv)
├── .env.example                # Placeholder for GEMINI_API_KEY (no real key)
├── .gitignore                    # Excludes venv/, .env, __pycache__/
├── portfolio.html                 # Auto-generated final output
└── README.md
```

---

## 🔌 Prompt Design

The prompt sent to Gemini enforces strict, factual extraction:

```
- Use ONLY information present in the resume text.
- Do NOT invent skills, companies, dates, projects, achievements, or links.
- Use empty string "" or empty list [] for anything missing.
- Reply with VALID JSON ONLY — no markdown, no explanations.
```

**Expected JSON shape:**
```json
{
  "name": "",
  "headline": "",
  "summary": "",
  "skills": [],
  "education": [{ "degree": "", "institution": "", "years": "" }],
  "experience": [{ "role": "", "company": "", "duration": "", "description": "" }],
  "projects": [{ "title": "", "description": "", "technologies": "" }],
  "achievements": [],
  "contact": { "email": "", "phone": "", "linkedin": "", "github": "" }
}
```

> 💡 Every generated field was manually cross-checked against the source resume before
> submission — this is a draft generator, not a final source of truth.

---

## ⚙️ Setup & Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/resume-portfolio-generator.git
cd resume-portfolio-generator

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate      # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt
```

Create your `.env` file from the example:
```bash
cp .env.example .env
```

Then edit `.env` with your own Gemini API key (get one free at [Google AI Studio](https://aistudio.google.com/)):
```
GEMINI_API_KEY=your_actual_key_here
```

Add your resume content to `resume.txt`, then run:
```bash
python main.py
```

Open the generated `portfolio.html` in your browser. No build step required!

---

## 🧪 Testing

| # | Test Case | Expected Behavior | Result |
|---|---|---|---|
| 1 | Missing `resume.txt` | Clear error, safe exit | ✅ Pass |
| 2 | Empty / very short resume | Rejected with a clear message | ✅ Pass |
| 3 | Valid resume | `portfolio.html` generated successfully | ✅ Pass |
| 4 | Resume with missing sections | Generates available sections only, nothing invented | ✅ Pass |
| 5 | Missing API key | Clear configuration error | ✅ Pass |
| 6 | Invalid API key | Error handled without crashing | ✅ Pass |
| 7 | Invalid JSON response | Handled via try/except in `parse_json_response()` | ✅ Pass |

---

## 🔒 Security & Responsible AI Notes

- ✅ Gemini is called **only** from the Python backend — never from client-side JavaScript, so the API key is never exposed to a browser
- ✅ The real API key lives only in a local `.env` file, excluded from version control via `.gitignore`
- ✅ `resume.txt` in this repo contains no sensitive personal data (no passwords, ID numbers, or financial details)
- ⚠️ Gemini output is a **draft** — every generated claim was manually verified against the original resume before use
- ⚠️ Gemini's model names and SDKs change periodically; see the [Gemini API docs](https://ai.google.dev/gemini-api/docs) if you hit a "model not found" error

---

## 📌 Roadmap / Possible Enhancements

- [ ] Additional CSS themes to choose from
- [ ] A second HTML portfolio template style
- [ ] Extra sections — certifications, languages, interests
- [ ] Live deployment via Vercel

---

## 🙌 Acknowledgements

Built as part of the **AIML GLA Bootcamp '26 — Summer 2026** curriculum, covering Python,
API integration, prompt design, JSON handling, and responsible AI development. Frontend
scaffolded with **Google Antigravity**; backend debugging assisted by **Claude**.

---

<div align="center">

**⭐ If you found this project interesting, consider giving it a star!**

Made with ☕ and a lot of `{{placeholder}}` tags.

</div>
