from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import pytesseract
from PIL import Image
import pdfplumber
import os
import tempfile

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

pytesseract.pytesseract.tesseract_cmd = r"D:\\Fake Catcher\\Tesseract-OCR\\tesseract.exe"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route("/ping")
def ping():
    return "pong"

@app.route("/analyze", methods=["POST"])
def analyze():
    extracted_text = ""

    if "file" in request.files:
        file = request.files["file"]
        ext = file.filename.split(".")[-1].lower()

        with tempfile.NamedTemporaryFile(delete=False, suffix="." + ext) as temp:
            file.save(temp.name)

            if ext == "pdf":
                with pdfplumber.open(temp.name) as pdf:
                    for page in pdf.pages:
                        extracted_text += (page.extract_text() or "") + "\n"
            else:
                image = Image.open(temp.name)
                extracted_text = pytesseract.image_to_string(image)

    elif "text" in request.form:
        extracted_text = request.form["text"]

    else:
        return jsonify({"error": "No input provided"}), 400

    risky_keywords = {
        "terminate": "high",
        "arbitration": "high",
        "liability": "high",
        "renew": "medium",
        "change": "medium",
        "update": "medium",
        "waive": "high",
        "discretion": "medium",
        "binding": "high",
        "without notice": "high",
    }

    analysis = []
    for line in extracted_text.split("\n"):
        if not line.strip():
            continue

        risk_level = "low"
        for keyword, level in risky_keywords.items():
            if keyword in line.lower():
                risk_level = level
                break

        analysis.append({
            "title": line.strip()[:60] + "...",  
            "summary": "This means: " + line.strip(),
            "risk_level": risk_level
        })

    summary = "Contract contains clauses with various risk levels. Review recommended."

    return jsonify({
        "summary": summary,
        "analysis": analysis,
        "extracted_text": extracted_text
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
