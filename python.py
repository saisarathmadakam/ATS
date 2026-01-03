from flask import Flask, request, jsonify, render_template
from google import genai
import PyPDF2
import os
from dotenv import load_dotenv

# -------------------- Flask app --------------------
app = Flask(__name__)

# Load .env file
load_dotenv()

# Gemini API client using env variable
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# -------------------- PDF Text Extractor --------------------
def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# -------------------- Resume Parser --------------------
def parse_resume(resume_text):
    prompt = f"""
Extract key information from resume.

Return format:
SKILLS:
EXPERIENCE:
EDUCATION:

Resume:
{resume_text}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

# -------------------- Job Description Parser --------------------
def parse_job_description(jd_text):
    prompt = f"""
Extract required skills and qualifications.

Return format:
REQUIRED_SKILLS:
REQUIREMENTS:

Job Description:
{jd_text}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

# -------------------- ATS Analysis --------------------
def ats_analysis(resume_text, jd_text=None):
    parsed_resume = parse_resume(resume_text)

    if jd_text and jd_text.strip():
        parsed_jd = parse_job_description(jd_text)
        prompt = f"""
You are a strict ATS system.

Compare Resume with Job Description.

Return ONLY in this format:

SCORE: <number>/100

PROS:
- strength

CONS:
- weakness

MATCHED_SKILLS:
- skill

MISSING_SKILLS:
- skill

RECOMMENDATIONS:
- suggestion

RESUME:
{parsed_resume}

JOB DESCRIPTION:
{parsed_jd}
"""
    else:
        prompt = f"""
You are a strict ATS (Applicant Tracking System).

Analyze resume ONLY.

Return ONLY in this format:

SCORE: <number>/100

PROS:
- strength

CONS:
- weakness

CRITICAL_ISSUES:
- issue

MISSING_KEYWORDS:
- keyword

RECOMMENDATIONS:
- suggestion

RESUME:
{parsed_resume}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

# -------------------- Routes --------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        jd_text = request.form.get("job_description", "")

        resume_text = extract_text_from_pdf(file)
        result = ats_analysis(resume_text, jd_text)

        return jsonify({"result": result})

    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to analyze resume"}), 500

# -------------------- Run --------------------
if __name__ == "__main__":
    print("API KEY:", os.getenv("GEMINI_API_KEY"))  # test key read
    app.run(debug=True, port=5000)
