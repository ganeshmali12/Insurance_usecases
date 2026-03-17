import os
from flask import Flask, render_template, request, jsonify
from classifier import classify_document

app = Flask(__name__)

UPLOAD_FOLDER = "data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/classify", methods=["POST"])
def classify():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"})

    from werkzeug.utils import secure_filename
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    try:
        result = classify_document(file_path)
    except Exception as e:
        print(f"[ERROR] classify_document failed: {e}")
        result = {
            "document_type": "Unknown",
            "confidence": 0.0,
            "reason": f"Classification error: {str(e)}"
        }
    return jsonify(result)


@app.route("/debug-ocr", methods=["POST"])
def debug_ocr():
    """Debug endpoint: returns raw OCR text so you can see what Tesseract extracted."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"})

    from werkzeug.utils import secure_filename
    from utils.ocr_utils import extract_text
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    try:
        text = extract_text(file_path)
        return jsonify({
            "char_count": len(text.strip()),
            "extracted_text": text
        })
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)

