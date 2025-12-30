import json
from flask import Flask, request, render_template_string
from agent import normalize_claim

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Claims Description Normalizer</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        textarea { width: 100%; height: 120px; }
        pre { background: #f4f4f4; padding: 15px; }
        button { padding: 10px 20px; }
    </style>
</head>
<body>
    <h2>Claims Description Normalizer</h2>

    <form method="POST">
        <textarea name="claim_text"
        placeholder="Enter claim description...">{{ claim_text }}</textarea><br><br>
        <button type="submit">Normalize</button>
    </form>

    {% if result %}
    <h3>Normalized Output</h3>
    <pre>{{ result }}</pre>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    claim_text = ""

    if request.method == "POST":
        claim_text = request.form["claim_text"]
        output = normalize_claim(claim_text)
        result = json.dumps(output, indent=2)

    return render_template_string(
        HTML_TEMPLATE,
        result=result,
        claim_text=claim_text
    )

if __name__ == "__main__":
    app.run(debug=True)
