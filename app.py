
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from PIL import Image
import pytesseract
import pdfplumber
import tempfile
import os
from analyze_utils import analyze_clauses

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.route("/")
def index():
    return render_template("index.html")

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

    result = analyze_clauses(extracted_text)
    result["extracted_text"] = extracted_text
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
