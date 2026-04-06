from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>App is working ✅</h1><a href='/generate'>Go</a>"

@app.route("/generate")
def generate():
    return """
    <form method="POST" action="/result">
    <input name="name"><br>
    <button type="submit">Send</button>
    </form>
    """

@app.route("/result", methods=["POST"])
def result():
    name = request.form.get("name")
    return f"<h1>Hello {name}</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
