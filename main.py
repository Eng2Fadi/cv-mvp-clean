import requests

from flask import Flask, render_template, request
import os

app = Flask(__name__)


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

    generated_cv = f"""
Name: {data['name']}
Email: {data['email']}
Specialization: {data['specialization']}

Skills:
{data['skills']}

Courses:
{data['courses']}

Projects:
{data['projects']}

Languages:
{data['languages']}

Job Description:
{data['job_description']}
"""

    return render_template("result.html", generated_cv=generated_cv, **data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
