from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__)


def generate_cv_with_ai(data):
    api_key = os.environ.get("DEEPSEEK_API_KEY")

    if not api_key:
        return f"""
Professional Summary
Entry-level {data['specialization']} candidate with foundational knowledge, practical project exposure, and strong motivation to contribute in a professional environment.

Skills
{data['skills'] or 'Not provided'}

Courses
{data['courses'] or 'Not provided'}

Projects
{data['projects'] or 'Not provided'}

Languages
{data['languages'] or 'Not provided'}

Target Job
{data['job_description'] or 'Not provided'}
"""

    prompt = f"""
You are a professional resume writer.

Create a clean, strong, ATS-friendly CV for an entry-level candidate.

Candidate data:
Name: {data['name']}
Email: {data['email']}
Specialization: {data['specialization']}
Skills: {data['skills']}
Courses: {data['courses']}
Projects: {data['projects']}
Languages: {data['languages']}
Target job description: {data['job_description']}

Instructions:
- Write a strong professional summary
- Turn projects and courses into professional value
- Make the candidate sound credible for a first job
- Keep it concise and professional
- Use clear sections
- Use bullet points where appropriate
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
            "temperature": 0.7,
            "max_tokens": 900
        },
        timeout=60
    )

    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate")
def generate():
    return render_template("generate.html")


@app.route("/result", methods=["POST"])
def result():
    data = {
        "name": request.form.get("name", "").strip(),
        "email": request.form.get("email", "").strip(),
        "specialization": request.form.get("specialization", "").strip(),
        "skills": request.form.get("skills", "").strip(),
        "courses": request.form.get("courses", "").strip(),
        "projects": request.form.get("projects", "").strip(),
        "languages": request.form.get("languages", "").strip(),
        "job_description": request.form.get("job_description", "").strip(),
    }

    try:
        generated_cv = generate_cv_with_ai(data)
    except Exception as e:
        generated_cv = f"Error while generating CV: {str(e)}"

    return render_template("result.html", generated_cv=generated_cv, **data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
