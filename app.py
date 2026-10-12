"""
Flask Application for AI Resume Analyzer.
Provides RESTful APIs for in-memory resume parsing, ATS & Semantic NLP analysis,
optional Google Gemini live integration, and pre-built sample roles.
"""
import os
import sys
from flask import Flask, request, jsonify, render_template, send_from_directory
from analyzer import extract_resume_text, analyze_resume_nlp, SAMPLES, analyze_with_gemini

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload limit


@app.after_request
def add_security_and_privacy_headers(response):
    """Ensure no caching of sensitive resume data in browser/proxies."""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.route('/')
def index():
    """Render main application page."""
    return render_template('index.html')


@app.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "AI Resume Analyzer",
        "privacy": "In-memory processing only. Zero persistent storage."
    })


@app.route('/api/samples', methods=['GET'])
def list_samples():
    """List available sample profiles."""
    summary_list = []
    for sid, sdata in SAMPLES.items():
        summary_list.append({
            "id": sid,
            "title": sdata["title"],
            "role_category": sdata["role_category"],
            "short_desc": sdata["short_desc"]
        })
    return jsonify({"success": True, "samples": summary_list})


@app.route('/api/samples/<sample_id>', methods=['GET'])
def get_sample(sample_id):
    """Retrieve full resume and JD for a sample profile."""
    if sample_id not in SAMPLES:
        return jsonify({"success": False, "error": f"Sample '{sample_id}' not found."}), 404
    return jsonify({"success": True, "sample": SAMPLES[sample_id]})


@app.route('/api/extract', methods=['POST'])
def extract_file():
    """
    Extract text in-memory from an uploaded PDF, DOCX, or TXT file.
    No files are ever written to the disk.
    """
    if 'resume_file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded. Please choose a PDF or DOCX file."}), 400

    uploaded_file = request.files['resume_file']
    filename = uploaded_file.filename

    if not filename or filename.strip() == '':
        return jsonify({"success": False, "error": "No file selected."}), 400

    allowed_extensions = {'.pdf', '.docx', '.txt'}
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext not in allowed_extensions:
        return jsonify({
            "success": False,
            "error": f"Unsupported file type '{file_ext}'. Please upload a .pdf, .docx, or .txt file."
        }), 400

    try:
        file_bytes = uploaded_file.read()
        if len(file_bytes) == 0:
            return jsonify({"success": False, "error": "The uploaded file is empty (0 bytes)."}), 400

        text, metadata = extract_resume_text(filename, file_bytes)
        return jsonify({
            "success": True,
            "filename": filename,
            "text": text,
            "metadata": metadata
        })

    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Unexpected error while reading {filename}: {str(e)}"
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Analyze resume text against job description text.
    Supports either Local Semantic NLP engine or optional Gemini AI live key.
    """
    data = request.get_json(silent=True) or {}
    resume_text = data.get("resume_text", "").strip()
    jd_text = data.get("jd_text", "").strip()
    api_key = data.get("api_key", "").strip()
    engine = data.get("engine", "local").strip().lower()

    # Input validation
    if not resume_text:
        return jsonify({"success": False, "error": "Please provide your resume text or upload a document."}), 400

    if not jd_text:
        return jsonify({"success": False, "error": "Please provide the job description text."}), 400

    if len(resume_text) < 80:
        return jsonify({
            "success": False,
            "error": "The resume text is too short to analyze. Please provide a more complete resume (at least 80 characters)."
        }), 400

    if len(jd_text) < 40:
        return jsonify({
            "success": False,
            "error": "The job description is too short. Please paste the full job posting (at least 40 characters)."
        }), 400

    # Decision logic: Gemini vs Local Engine
    if engine == "gemini" and api_key:
        try:
            results = analyze_with_gemini(resume_text, jd_text, api_key)
            return jsonify({"success": True, "result": results})
        except Exception as e:
            # If user explicitly requested Gemini, return error so they know their key failed,
            # but provide option to fall back
            return jsonify({
                "success": False,
                "error": str(e),
                "can_fallback_to_local": True
            }), 400

    # Default to Local Semantic NLP & ATS Engine
    try:
        results = analyze_resume_nlp(resume_text, jd_text)
        return jsonify({"success": True, "result": results})
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Analysis failed: {str(e)}"
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[INFO] AI Resume Analyzer server running on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=False)
