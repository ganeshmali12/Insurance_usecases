from flask import Flask, request, render_template_string
from agent import normalize_claim
from Demo_data import DEMO_CLAIMS

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Claims Description Normalizer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet"/>
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
            color: #e2e8f0;
            display: flex;
            flex-direction: column;
        }

        /* ── Header ── */
        header {
            background: rgba(255,255,255,0.04);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(255,255,255,0.08);
            padding: 18px 40px;
            display: flex;
            align-items: center;
            gap: 14px;
        }
        header .logo-icon {
            width: 42px; height: 42px;
            background: linear-gradient(135deg, #3b82f6, #06b6d4);
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 20px;
            box-shadow: 0 4px 15px rgba(59,130,246,0.4);
        }
        header h1 {
            font-size: 1.25rem;
            font-weight: 700;
            background: linear-gradient(90deg, #60a5fa, #22d3ee);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.3px;
        }
        header span.subtitle {
            font-size: 0.75rem;
            color: #64748b;
            font-weight: 400;
            margin-left: 4px;
        }

        /* ── Main layout ── */
        main {
            flex: 1;
            max-width: 900px;
            width: 100%;
            margin: 0 auto;
            padding: 40px 20px;
            display: flex;
            flex-direction: column;
            gap: 28px;
        }

        /* ── Hero text ── */
        .hero {
            text-align: center;
        }
        .hero h2 {
            font-size: 2rem;
            font-weight: 700;
            color: #f1f5f9;
            margin-bottom: 8px;
        }
        .hero p {
            color: #94a3b8;
            font-size: 0.95rem;
        }

        /* ── Card ── */
        .card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 28px;
            backdrop-filter: blur(10px);
            transition: box-shadow 0.3s;
        }
        .card:hover { box-shadow: 0 8px 32px rgba(0,0,0,0.3); }

        /* ── Form ── */
        .form-label {
            display: block;
            font-size: 0.82rem;
            font-weight: 600;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 10px;
        }
        textarea {
            width: 100%;
            height: 140px;
            background: rgba(0,0,0,0.3);
            border: 1.5px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            color: #e2e8f0;
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            padding: 14px 16px;
            resize: vertical;
            outline: none;
            transition: border-color 0.25s, box-shadow 0.25s;
        }
        textarea:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59,130,246,0.2);
        }
        textarea::placeholder { color: #475569; }

        /* ── Button ── */
        .btn-row { display: flex; justify-content: flex-end; margin-top: 18px; }
        button[type="submit"] {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 12px 30px;
            background: linear-gradient(135deg, #3b82f6, #06b6d4);
            border: none;
            border-radius: 10px;
            color: #fff;
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s, opacity 0.2s;
            box-shadow: 0 4px 18px rgba(59,130,246,0.4);
        }
        button[type="submit"]:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(59,130,246,0.5); }
        button[type="submit"]:active { transform: translateY(0); }
        button[type="submit"].loading { opacity: 0.75; pointer-events: none; }

        /* ── Spinner ── */
        .spinner {
            display: none;
            width: 16px; height: 16px;
            border: 2px solid rgba(255,255,255,0.3);
            border-top-color: #fff;
            border-radius: 50%;
            animation: spin 0.7s linear infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        /* ── Results section ── */
        .results-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
        }
        .results-header i { color: #22d3ee; font-size: 1.1rem; }
        .results-header h3 { font-size: 1.05rem; font-weight: 600; color: #e2e8f0; }

        .results-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }
        @media (max-width: 600px) { .results-grid { grid-template-columns: 1fr; } }

        /* ── Result item ── */
        .result-item {
            background: rgba(0,0,0,0.25);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 18px 20px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            animation: fadeSlideIn 0.4s ease both;
        }
        @keyframes fadeSlideIn {
            from { opacity: 0; transform: translateY(12px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .result-item:nth-child(1) { animation-delay: 0.05s; }
        .result-item:nth-child(2) { animation-delay: 0.10s; }
        .result-item:nth-child(3) { animation-delay: 0.15s; }
        .result-item:nth-child(4) { animation-delay: 0.20s; grid-column: 1 / -1; }

        .result-label {
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.9px;
            color: #64748b;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .result-label i { font-size: 0.85rem; }

        .result-value {
            font-size: 1rem;
            font-weight: 600;
            color: #f1f5f9;
        }

        /* ── Severity badge ── */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 14px;
            border-radius: 50px;
            font-size: 0.88rem;
            font-weight: 700;
            width: fit-content;
        }
        .badge-low    { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
        .badge-medium { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
        .badge-high   { background: rgba(239,68,68,0.15);  color: #f87171; border: 1px solid rgba(248,113,113,0.3); }

        /* ── Loss type chip ── */
        .loss-chip {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            background: rgba(59,130,246,0.15);
            border: 1px solid rgba(59,130,246,0.3);
            border-radius: 50px;
            color: #93c5fd;
            font-size: 0.92rem;
            font-weight: 600;
            width: fit-content;
        }

        /* ── Asset tags ── */
        .asset-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px; }
        .asset-tag {
            padding: 4px 12px;
            background: rgba(99,102,241,0.15);
            border: 1px solid rgba(99,102,241,0.3);
            border-radius: 6px;
            color: #a5b4fc;
            font-size: 0.82rem;
            font-weight: 500;
        }

        /* ── Summary ── */
        .summary-text {
            font-size: 0.95rem;
            font-weight: 400;
            color: #cbd5e1;
            line-height: 1.6;
        }

        /* ── Demo sample chips ── */
        .samples-row {
            display: flex;
            flex-wrap: wrap;
            gap: 7px;
            margin-top: 14px;
            padding-top: 14px;
            border-top: 1px solid rgba(255,255,255,0.07);
        }
        .samples-row-label {
            width: 100%;
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #475569;
            margin-bottom: 2px;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .sample-chip {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            background: rgba(0,0,0,0.25);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 6px;
            color: #64748b;
            font-family: 'Inter', sans-serif;
            font-size: 0.78rem;
            padding: 5px 11px;
            cursor: pointer;
            transition: background 0.2s, border-color 0.2s, color 0.2s;
            white-space: nowrap;
        }
        .sample-chip:hover {
            background: rgba(59,130,246,0.12);
            border-color: rgba(59,130,246,0.35);
            color: #93c5fd;
        }

        /* ── Error card ── */
        .error-card {
            background: rgba(239,68,68,0.08);
            border: 1px solid rgba(239,68,68,0.3);
            border-radius: 12px;
            padding: 18px 22px;
            display: flex;
            align-items: flex-start;
            gap: 14px;
            animation: fadeSlideIn 0.3s ease both;
        }
        .error-card i { color: #f87171; font-size: 1.2rem; margin-top: 2px; flex-shrink: 0; }
        .error-card .error-title { font-weight: 600; color: #fca5a5; margin-bottom: 4px; }
        .error-card .error-msg { font-size: 0.88rem; color: #f87171; }

        /* ── Footer ── */
        footer {
            text-align: center;
            padding: 20px;
            font-size: 0.78rem;
            color: #475569;
            border-top: 1px solid rgba(255,255,255,0.05);
        }
    </style>
</head>
<body>

    <header>
        <div class="logo-icon"><i class="fa-solid fa-shield-halved"></i></div>
        <div>
            <h1>Claims Normalizer <span class="subtitle">AI-Powered</span></h1>
        </div>
    </header>

    <main>
        <div class="hero">
            <h2>Insurance Claims Analyzer</h2>
            <p>Paste a raw claim description and get a structured, normalized summary instantly.</p>
        </div>

        <div style="display:flex;flex-direction:column;gap:24px;">

                <!-- Input Card -->
                <div class="card">
                    <label class="form-label"><i class="fa-solid fa-file-lines" style="margin-right:6px;color:#3b82f6;"></i>Claim Description</label>
                    <form method="POST" id="claimForm" onsubmit="return validateForm()">
                        <textarea name="claim_text" id="claimText"
                            placeholder="e.g. — My car was hit from behind at the traffic signal yesterday. The rear bumper and trunk are badly damaged...">{{ claim_text }}</textarea>
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px;">
                            <span id="charCount" style="font-size:0.75rem;color:#475569;">0 characters</span>
                            <div class="btn-row" style="margin-top:0;">
                                <button type="submit" id="submitBtn">
                                    <span class="spinner" id="spinner"></span>
                                    <i class="fa-solid fa-wand-magic-sparkles" id="btnIcon"></i>
                                    <span id="btnText">Normalize Claim</span>
                                </button>
                            </div>
                        </div>

                        <!-- Sample chips inside the card -->
                        <div class="samples-row">
                            <div class="samples-row-label"><i class="fa-solid fa-flask-vial"></i> Try a sample</div>
                            {% set icons = ['fa-droplet','fa-fire','fa-mask','fa-car-burst','fa-heart-pulse'] %}
                            {% for sample in demo_claims %}
                            <button class="sample-chip" onclick="loadSample({{ loop.index0 }})" type="button">
                                <i class="fa-solid {{ icons[loop.index0] }}"></i>
                                {{ sample.split('.')[0][:40] }}
                            </button>
                            {% endfor %}
                        </div>
                    </form>
                </div>

                {% if error %}
                <!-- Error Card -->
                <div class="error-card">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    <div>
                        <div class="error-title">Analysis Failed</div>
                        <div class="error-msg">{{ error }}</div>
                    </div>
                </div>
                {% endif %}

                {% if result %}
                <!-- Results Card -->
                <div class="card">
                    <div class="results-header">
                        <i class="fa-solid fa-circle-check"></i>
                        <h3>Normalized Output</h3>
                    </div>

                    <div class="results-grid">

                        <!-- Loss Type -->
                        <div class="result-item">
                            <div class="result-label"><i class="fa-solid fa-tag"></i> Loss Type</div>
                            <div>
                                <span class="loss-chip">
                                    {% if result.loss_type == 'Fire' %}<i class="fa-solid fa-fire"></i>
                                    {% elif result.loss_type == 'Theft' %}<i class="fa-solid fa-mask"></i>
                                    {% elif result.loss_type == 'Water Damage' %}<i class="fa-solid fa-droplet"></i>
                                    {% elif result.loss_type == 'Accident' %}<i class="fa-solid fa-car-burst"></i>
                                    {% elif result.loss_type == 'Medical' %}<i class="fa-solid fa-heart-pulse"></i>
                                    {% else %}<i class="fa-solid fa-circle-question"></i>{% endif %}
                                    {{ result.loss_type }}
                                </span>
                            </div>
                        </div>

                        <!-- Severity -->
                        <div class="result-item">
                            <div class="result-label"><i class="fa-solid fa-gauge-high"></i> Severity</div>
                            <div>
                                {% if result.severity == 'Low' %}
                                    <span class="badge badge-low"><i class="fa-solid fa-circle-dot"></i> Low</span>
                                {% elif result.severity == 'Medium' %}
                                    <span class="badge badge-medium"><i class="fa-solid fa-circle-dot"></i> Medium</span>
                                {% else %}
                                    <span class="badge badge-high"><i class="fa-solid fa-circle-dot"></i> High</span>
                                {% endif %}
                            </div>
                        </div>

                        <!-- Affected Assets -->
                        <div class="result-item">
                            <div class="result-label"><i class="fa-solid fa-boxes-stacked"></i> Affected Assets</div>
                            <div class="asset-tags">
                                {% for asset in result.affected_asset %}
                                    <span class="asset-tag"><i class="fa-solid fa-cube" style="font-size:0.7rem;"></i> {{ asset }}</span>
                                {% endfor %}
                            </div>
                        </div>

                        <!-- Incident Summary (full width) -->
                        <div class="result-item">
                            <div class="result-label"><i class="fa-solid fa-memo"></i> Incident Summary</div>
                            <div class="summary-text">{{ result.incident_summary }}</div>
                        </div>

                    </div>
                </div>
                {% endif %}

        </div>
    </main>

    <footer>
        &copy; 2026 Insurance Claims Normalizer &nbsp;&bull;&nbsp; Powered by Azure OpenAI
    </footer>

    <script>
        // Character counter
        const ta = document.getElementById('claimText');
        const cc = document.getElementById('charCount');
        function updateCount() {
            const n = ta.value.trim().length;
            cc.textContent = n + ' character' + (n !== 1 ? 's' : '');
            cc.style.color = n === 0 ? '#ef4444' : '#475569';
        }
        ta.addEventListener('input', updateCount);
        updateCount();

        // Validate before submit
        function validateForm() {
            if (ta.value.trim().length === 0) {
                ta.style.borderColor = '#ef4444';
                ta.style.boxShadow = '0 0 0 3px rgba(239,68,68,0.2)';
                ta.focus();
                return false;
            }
            const btn = document.getElementById('submitBtn');
            const spinner = document.getElementById('spinner');
            const icon = document.getElementById('btnIcon');
            const text = document.getElementById('btnText');
            btn.classList.add('loading');
            spinner.style.display = 'block';
            icon.style.display = 'none';
            text.textContent = 'Analyzing\u2026';
            return true;
        }
        ta.addEventListener('input', function () {
            ta.style.borderColor = '';
            ta.style.boxShadow = '';
        });

        // Load sample into textarea by index
        const samples = {{ demo_claims | tojson }};
        function loadSample(idx) {
            ta.value = samples[idx];
            ta.style.borderColor = '';
            ta.style.boxShadow = '';
            ta.focus();
            updateCount();
        }
    </script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    claim_text = ""
    error = None

    if request.method == "POST":
        claim_text = request.form.get("claim_text", "").strip()
        if claim_text:
            try:
                result = normalize_claim(claim_text)
            except Exception as e:
                error = str(e)

    return render_template_string(
        HTML_TEMPLATE,
        result=result,
        claim_text=claim_text,
        error=error,
        demo_claims=DEMO_CLAIMS
    )

if __name__ == "__main__":
    app.run(debug=True)
