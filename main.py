import os
import json
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate():
    return render_template('generate.html')

def generate_cv_with_ai(data):
    api_key = os.environ.get("DEEPSEEK_API_KEY")

    prompt = f"""
YouYou are an expert ATS resume optimizer.

Your job is to:
1. Analyze the target job description
2. Score the candidate CV for ATS compatibility
3. Identify matched keywords and missing keywords
4. Suggest improvements
5. Generate an improved ATS-friendly CV tailored to the target job

Candidate data:
Name: {data.get("name")}
Email: {data.get("email")}
Specialization: {data.get("specialization")}
Skills: {data.get("skills")}
Courses: {data.get("courses")}
Projects: {data.get("projects")}
Languages: {data.get("languages")}
Job Description: {data.get("job_description")}

Rules:
- Be strict and realistic
- ATS score must be between 0 and 100
- Use executive-quality writing
- Keep the CV ATS-friendly
- Use one-column professional structure
- No tables, no icons, no fancy formatting
- Return ONLY valid JSON
- Do not add markdown
- Do not explain outside JSON

Required JSON structure:

{{
  "ats_score": 0,
  "job_title_detected": "",
  "matched_keywords": [],
  "missing_keywords": [],
  "improvement_suggestions": [],
  "cv": {{
    "full_name": "",
    "location": "",
    "phone": "",
    "email": "",
    "linkedin": "",
    "headline": "",
    "branding_line": "",
    "career_summary": "",
    "hard_skills": [],
    "soft_skills": [],
    "experience": [
      {{
        "company": "",
        "location": "",
        "title": "",
        "date": "",
        "bullets": []
      }}
    ],
    "education": [],
    "certificates": [],
    "publications": [],
    "languages": []
  }}
}}
"""

    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1800
        },
        timeout=60
    )

    response.raise_for_status()
    result = response.json()
    content = result["choices"][0]["message"]["content"]

    return json.loads(content)

@app.route('/result', methods=['POST'])
def result():
    data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'specialization': request.form['specialization'],
        'skills': request.form['skills'],
        'courses': request.form['courses'],
        'projects': request.form['projects'],
        'languages': request.form['languages'],
        'job_description': request.form['job_description']
    }

    analysis = generate_cv_with_ai(data)
    cv = analysis["cv"]
    ats_score = analysis["ats_score"]
    matched_keywords = analysis["matched_keywords"]
    missing_keywords = analysis["missing_keywords"]
    improvement_suggestions = analysis["improvement_suggestions"]

    return render_template(
        "result.html",
        cv=cv,
        ats_score=ats_score,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        improvement_suggestions=improvement_suggestions,
        is_paid=False
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
