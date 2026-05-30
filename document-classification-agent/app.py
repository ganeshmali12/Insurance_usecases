import os
import hmac
from datetime import timedelta
from functools import wraps
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from classifier import classify_document

# Load .env explicitly before any os.getenv() calls
load_dotenv(find_dotenv())

app = Flask(__name__)

UPLOAD_FOLDER = "data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# SECRET_KEY must be set in .env — used to sign session cookies
app.secret_key = os.getenv("SECRET_KEY", "change-this-before-deploying")
# Sessions expire after 30 minutes of inactivity
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)


# --------------------------------------------------
# Auth helpers
# --------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        # hmac.compare_digest prevents timing-based attacks
        valid_user = hmac.compare_digest(username, os.getenv("APP_USERNAME", "").strip())
        valid_pass = hmac.compare_digest(password, os.getenv("APP_PASSWORD", "").strip())
        if valid_user and valid_pass:
            session.permanent = True
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("index"))
        error = "Invalid username or password."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    return render_template("index.html", username=session.get("username"))


@app.route("/classify", methods=["POST"])
@login_required
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
@login_required
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
    app.run(debug=True, threaded=True)

