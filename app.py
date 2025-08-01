from flask import Flask, render_template, request, jsonify
import fitz  # PyMuPDF
from groq import Groq

client = Groq(api_key="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")  # Replace this with your actual Groq API key

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['resume']
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = " ".join([page.get_text() for page in doc])
        return jsonify({"text": text[:1500]})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    data = request.get_json()
    role = data.get("role")
    resume_text = data.get("resume_text")

    prompt = f"""
You're an expert interviewer. Generate 5 interview questions for a {role}, based on this resume:\n\n{resume_text[:1500]}
    """

    res = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    questions = [line.strip() for line in res.choices[0].message.content.strip().split("\n") if line.strip() and line.strip()[0].isdigit()]
    return jsonify({"questions": questions})
