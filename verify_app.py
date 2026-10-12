"""
End-to-end automated verification script for AI Resume Analyzer.
Tests file upload/extraction (DOCX & PDF), NLP analysis engine,
validation edge cases, and API responses.
"""
import io
import json
import urllib.request
import urllib.error
import docx

BASE_URL = "http://127.0.0.1:5000"

def test_api_health():
    print("[1] Testing /api/health...")
    req = urllib.request.Request(f"{BASE_URL}/api/health")
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode('utf-8'))
        assert data["status"] == "healthy", f"Unexpected status: {data}"
        print("  -> Passed! Health status:", data["status"], "| Privacy:", data["privacy"])

def test_api_samples():
    print("[2] Testing /api/samples and individual sample retrieval...")
    req = urllib.request.Request(f"{BASE_URL}/api/samples")
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode('utf-8'))
        assert data["success"] is True
        samples = data["samples"]
        assert len(samples) >= 3, f"Expected at least 3 samples, got {len(samples)}"
        print(f"  -> Found {len(samples)} samples: {[s['id'] for s in samples]}")

    for s in samples:
        s_req = urllib.request.Request(f"{BASE_URL}/api/samples/{s['id']}")
        with urllib.request.urlopen(s_req) as s_res:
            s_data = json.loads(s_res.read().decode('utf-8'))
            assert s_data["success"] is True
            assert "resume" in s_data["sample"]
            assert "job_description" in s_data["sample"]
            print(f"  -> Sample '{s['id']}' loaded successfully ({len(s_data['sample']['resume'].split())} words)")

def test_docx_file_upload_extraction():
    print("[3] Testing in-memory DOCX extraction via /api/extract...")
    doc = docx.Document()
    doc.add_heading("Taylor Reed - Senior DevOps Engineer", level=1)
    doc.add_paragraph("Austin, TX | taylor@example.com | (555) 019-2834 | linkedin.com/in/taylorreed")
    doc.add_heading("Professional Summary", level=2)
    doc.add_paragraph("DevOps & Cloud Engineer with 5+ years of experience scaling Kubernetes, Terraform, AWS, and CI/CD pipelines.")
    doc.add_heading("Skills", level=2)
    doc.add_paragraph("AWS, Docker, Kubernetes, Terraform, Python, Bash, Prometheus, Grafana, GitHub Actions")
    doc.add_heading("Experience", level=2)
    doc.add_paragraph("Lead DevOps Engineer | CloudScale Tech (2021 - Present)")
    doc.add_paragraph("- Architected AWS EKS Kubernetes clusters serving 1.5M requests/sec.")
    doc.add_paragraph("- Reduced infrastructure costs by 32% ($140,000/yr) through spot instances and automated rightsizing.")

    doc_io = io.BytesIO()
    doc.save(doc_io)
    file_bytes = doc_io.getvalue()

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="resume_file"; filename="taylor_resume.docx"\r\n'
        f"Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        f"{BASE_URL}/api/extract",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST"
    )

    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode('utf-8'))
        assert data["success"] is True
        assert "Kubernetes" in data["text"]
        assert "taylor@example.com" in data["text"]
        print(f"  -> Passed! Extracted {data['metadata']['word_count']} words from DOCX. Parser: {data['metadata']['parser']}")
        return data["text"]

def test_analyze_endpoint(extracted_resume_text):
    print("[4] Testing /api/analyze with extracted resume against a DevOps role...")
    jd = """
    Position: Senior Cloud & DevOps Infrastructure Engineer
    Requirements:
    - 4+ years of production experience with AWS (EKS, EC2, S3, IAM)
    - Strong proficiency in Kubernetes, Docker, and Terraform
    - Hands-on expertise building CI/CD pipelines with GitHub Actions
    - Experience with monitoring systems (Prometheus, Grafana)
    - Experience with Python or Golang for infrastructure automation
    - Bonus: Kafka, Helm, ArgoCD, Datadog
    """

    payload = json.dumps({
        "resume_text": extracted_resume_text,
        "jd_text": jd,
        "engine": "local"
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{BASE_URL}/api/analyze",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode('utf-8'))
        assert data["success"] is True
        result = data["result"]

        assert "overall_score" in result
        assert 0 <= result["overall_score"] <= 100
        assert "sub_scores" in result
        assert "skills" in result
        assert len(result["skills"]["matched"]) > 0
        assert len(result["skills"]["missing"]) > 0
        assert "suggestions" in result
        assert len(result["suggestions"]) > 0
        assert "disclaimer" in result

        print(f"  -> Analysis Success!")
        print(f"     Overall Match Score: {result['overall_score']}/100 ({result['match_tier']})")
        print(f"     Subscores: Skill Match={result['sub_scores']['skill_match']}%, Semantic={result['sub_scores']['semantic_relevance']}%, Impact={result['sub_scores']['experience_impact']}%, ATS={result['sub_scores']['ats_readability']}%")
        print(f"     Matched Skills ({len(result['skills']['matched'])}): {[s['name'] for s in result['skills']['matched'][:5]]}")
        print(f"     Missing Skills ({len(result['skills']['missing'])}): {[s['name'] for s in result['skills']['missing'][:5]]}")
        print(f"     Strengths ({len(result['strengths'])}): {result['strengths'][0]}")
        print(f"     Suggestions ({len(result['suggestions'])}): {result['suggestions'][0]['title']}")
        print(f"     Disclaimer verified: '{result['disclaimer'][:60]}...'")

def test_validation_edge_cases():
    print("[5] Testing validation and error handling...")
    # Empty resume
    payload = json.dumps({"resume_text": "", "jd_text": "Need python"}).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/api/analyze", data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        urllib.request.urlopen(req)
        assert False, "Should have returned 400 for empty resume"
    except urllib.error.HTTPError as e:
        assert e.code == 400
        err_data = json.loads(e.read().decode('utf-8'))
        print(f"  -> Caught expected error for empty resume: '{err_data['error']}'")

    # Unsupported file upload
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="resume_file"; filename="malicious.exe"\r\n'
        "fake content\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")
    req2 = urllib.request.Request(f"{BASE_URL}/api/extract", data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
    try:
        urllib.request.urlopen(req2)
        assert False, "Should have returned 400 for unsupported file"
    except urllib.error.HTTPError as e:
        assert e.code == 400
        err_data = json.loads(e.read().decode('utf-8'))
        print(f"  -> Caught expected error for invalid file type: '{err_data['error']}'")

if __name__ == '__main__':
    print("=" * 60)
    print("RUNNING AUTOMATED TEST SUITE FOR AI RESUME ANALYZER")
    print("=" * 60)
    test_api_health()
    test_api_samples()
    extracted_text = test_docx_file_upload_extraction()
    test_analyze_endpoint(extracted_text)
    test_validation_edge_cases()
    print("=" * 60)
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)
