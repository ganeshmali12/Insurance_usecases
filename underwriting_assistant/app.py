from flask import Flask, render_template, request
from agent import underwriting_agent

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        applicant_data = request.form.get("applicant_data")
        claims_history = request.form.get("claims_history")
        external_report = request.form.get("external_report")

        result = underwriting_agent(
            applicant_data,
            claims_history,
            external_report
        )

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
