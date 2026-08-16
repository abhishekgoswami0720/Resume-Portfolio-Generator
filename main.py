import os
import json
import re
from dotenv import load_dotenv
from google import genai

# ---------- STEP 1: Load the secret API key from .env ----------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ ERROR: GEMINI_API_KEY not found. Please check your .env file.")
    exit()

client = genai.Client(api_key=API_KEY)

# ---------- STEP 2: Read and clean resume.txt ----------
def read_resume(file_path="resume.txt"):
    if not os.path.exists(file_path):
        print("❌ ERROR: resume.txt not found. Please create it first.")
        exit()

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    lines = [line.strip() for line in text.splitlines() if line.strip() != ""]
    cleaned_text = "\n".join(lines)

    if len(cleaned_text) < 50:
        print("❌ ERROR: resume.txt seems empty or too short. Please add more content.")
        exit()

    return cleaned_text


# ---------- STEP 3: Build the strict prompt ----------
def build_prompt(resume_text):
    prompt = f"""
You are a strict resume-to-portfolio data extractor.

RULES (follow exactly):
- Use ONLY the information present in the resume text below.
- Do NOT invent skills, companies, dates, projects, achievements, or links.
- If some information is missing, use an empty string "" or empty list [].
- Reply with VALID JSON ONLY. No markdown, no ```json fences, no explanations.

Return JSON in exactly this structure:
{{
  "name": "",
  "headline": "",
  "summary": "",
  "skills": [],
  "education": [{{"degree": "", "institution": "", "years": ""}}],
  "experience": [{{"role": "", "company": "", "duration": "", "description": ""}}],
  "projects": [{{"title": "", "description": "", "technologies": ""}}],
  "achievements": [],
  "contact": {{"email": "", "phone": "", "linkedin": "", "github": ""}}
}}

Resume text:
\"\"\"
{resume_text}
\"\"\"
"""
    return prompt


# ---------- STEP 4: Call Gemini API safely ----------
def call_gemini(prompt):
    try:
        interaction = client.interactions.create(
            model="gemini-3.5-flash",
            input=prompt
        )
        return interaction.output_text
    except Exception as e:
        print(f"❌ ERROR: Gemini API call failed: {e}")
        exit()

# ---------- STEP 5: Clean and parse the JSON response ----------
def parse_json_response(raw_text):
    cleaned = re.sub(r"^```json|```$", "", raw_text.strip(), flags=re.MULTILINE).strip()
    try:
        data = json.loads(cleaned)
        return data
    except json.JSONDecodeError:
        print("❌ ERROR: Gemini did not return valid JSON. Please try again.")
        exit()


# ---------- STEP 6: Fill the HTML template with the data ----------
def generate_html(data):
    with open("template.html", "r", encoding="utf-8") as f:
        template = f.read()

    template = template.replace("{{name}}", data.get("name") or "")
    template = template.replace("{{headline}}", data.get("headline") or "")
    template = template.replace("{{summary}}", data.get("summary") or "")

    skills_html = "".join(f"<li>{s}</li>" for s in data.get("skills", []))
    template = template.replace("{{skills}}", skills_html)

    edu_html = ""
    for e in data.get("education", []):
        edu_html += f"<div><strong>{e.get('degree','')}</strong> - {e.get('institution','')} ({e.get('years','')})</div>"
    template = template.replace("{{education}}", edu_html)

    exp_html = ""
    for e in data.get("experience", []):
        exp_html += f"<div><strong>{e.get('role','')}</strong> at {e.get('company','')} ({e.get('duration','')})<p>{e.get('description','')}</p></div>"
    template = template.replace("{{experience}}", exp_html)

    proj_html = ""
    for p in data.get("projects", []):
        proj_html += f"<div><strong>{p.get('title','')}</strong><p>{p.get('description','')}</p><em>{p.get('technologies','')}</em></div>"
    template = template.replace("{{projects}}", proj_html)

    ach_html = "".join(f"<li>{a}</li>" for a in data.get("achievements", []))
    template = template.replace("{{achievements}}", ach_html)

    contact = data.get("contact", {})
    contact_html = f"""
    <p>Email: {contact.get('email','')}</p>
    <p>Phone: {contact.get('phone','')}</p>
    <p>LinkedIn: {contact.get('linkedin','')}</p>
    <p>GitHub: {contact.get('github','')}</p>
    """
    template = template.replace("{{contact}}", contact_html)

    with open("portfolio.html", "w", encoding="utf-8") as f:
        f.write(template)

    print("✅ portfolio.html generated successfully! Open it in your browser.")


# ---------- MAIN PROGRAM FLOW ----------
if __name__ == "__main__":
    print("📄 Reading resume.txt ...")
    resume_text = read_resume()

    print("🧠 Building prompt and calling Gemini ...")
    prompt = build_prompt(resume_text)
    raw_response = call_gemini(prompt)

    print("🔍 Parsing JSON response ...")
    data = parse_json_response(raw_response)

    print("🏗️  Generating portfolio.html ...")
    generate_html(data)