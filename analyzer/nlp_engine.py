"""
Advanced Local Semantic NLP & ATS Resume Analyzer Engine.
Uses spaCy, scikit-learn TF-IDF, and comprehensive skill taxonomy
to produce deep, deterministic, private analysis without external API dependencies.
"""
import re
import math
from typing import Dict, List, Any, Set, Tuple
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Comprehensive taxonomy of skills and keywords across tech, data, product, business, and soft skills
SKILL_TAXONOMY = {
    "languages": {
        "python", "javascript", "typescript", "java", "c++", "c#", "golang", "go", "rust",
        "ruby", "php", "swift", "kotlin", "scala", "r", "sql", "html", "html5", "css", "css3",
        "bash", "shell", "dart", "perl", "matlab", "vba"
    },
    "frontend": {
        "react", "react.js", "next.js", "nextjs", "vue", "vue.js", "angular", "svelte",
        "redux", "tailwind", "tailwind css", "bootstrap", "sass", "scss", "webpack", "vite",
        "web vitals", "responsive design", "graphql", "rest", "restful api", "storybook"
    },
    "backend": {
        "node.js", "nodejs", "express", "express.js", "nestjs", "django", "fastapi", "flask",
        "spring boot", "spring", "asp.net", ".net", "ruby on rails", "rails", "microservices",
        "grpc", "restful apis", "rest api", "websocket", "celery", "bullmq"
    },
    "databases_caching": {
        "postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch", "dynamodb",
        "cassandra", "sqlite", "prisma", "sqlalchemy", "hibernate", "snowflake", "bigquery",
        "oracle", "mariadb", "neo4j", "supabase", "firebase"
    },
    "cloud_devops": {
        "aws", "amazon web services", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "k8s", "terraform", "ci/cd", "ci cd", "github actions", "gitlab ci", "jenkins",
        "linux", "nginx", "apache", "helm", "ansible", "cloudformation", "ecs", "lambda",
        "serverless", "cloudwatch", "prometheus", "grafana", "s3", "cloudfront"
    },
    "ai_data_ml": {
        "machine learning", "deep learning", "nlp", "natural language processing", "computer vision",
        "pytorch", "tensorflow", "scikit-learn", "sklearn", "keras", "pandas", "numpy",
        "scipy", "xgboost", "lightgbm", "spark", "apache spark", "kafka", "hadoop", "mlops",
        "mlflow", "data modeling", "predictive analytics", "etl", "data pipelines", "tableau",
        "power bi", "matplotlib", "seaborn", "llm", "genai", "prompt engineering"
    },
    "testing_qa": {
        "jest", "cypress", "vitest", "mocha", "chai", "playwright", "selenium", "pytest",
        "unittest", "tdd", "bdd", "integration testing", "unit testing", "e2e testing"
    },
    "product_management": {
        "product roadmap", "roadmapping", "prd", "okrs", "kpis", "a/b testing", "ab testing",
        "user research", "wireframing", "figma", "jira", "linear", "scrum", "agile",
        "kanban", "sprint planning", "backlog grooming", "user stories", "gtm", "go-to-market",
        "cac", "ltv", "arr", "dau/mau", "retention", "amplitude", "mixpanel", "funnel analysis"
    },
    "architecture_practices": {
        "system design", "distributed systems", "event-driven", "domain-driven design", "ddd",
        "clean architecture", "design patterns", "oop", "functional programming", "code reviews",
        "scalability", "high availability", "security", "oauth", "jwt", "soc 2", "gdpr"
    },
    "soft_leadership": {
        "mentorship", "leadership", "cross-functional", "stakeholder management", "communication",
        "problem solving", "collaboration", "critical thinking", "client-facing", "team player",
        "conflict resolution", "project management", "time management", "ownership"
    }
}

# Strong action verbs signaling impact and leadership
ACTION_VERBS = {
    "architected", "spearheaded", "engineered", "optimized", "developed", "orchestrated",
    "implemented", "designed", "accelerated", "scaled", "automated", "mentored",
    "led", "reduced", "increased", "boosted", "delivered", "transformed", "streamlined",
    "championed", "negotiated", "established", "launched", "executed", "generated", "authored"
}

# Standard expected resume sections
STANDARD_SECTIONS = [
    {"name": "Summary / Objective", "patterns": [r"summary", r"objective", r"profile", r"about me", r"executive summary"]},
    {"name": "Work Experience", "patterns": [r"experience", r"employment", r"work history", r"professional experience"]},
    {"name": "Skills", "patterns": [r"skills", r"technical skills", r"core competencies", r"expertise", r"technologies"]},
    {"name": "Education", "patterns": [r"education", r"academic background", r"degree", r"university", r"college"]},
    {"name": "Projects / Certifications", "patterns": [r"projects", r"certifications", r"credentials", r"personal projects", r"accomplishments"]}
]


def normalize_token(token: str) -> str:
    """Normalize text token for matching."""
    token = token.lower().strip()
    token = re.sub(r'[\(\)\[\]\{\},:;]', '', token)
    return token


def extract_skills_from_text(text: str) -> Dict[str, Dict[str, Any]]:
    """
    Scan text against our taxonomy and identify present skills,
    returning count, category, and matching token.
    """
    text_lower = text.lower()
    found_skills: Dict[str, Dict[str, Any]] = {}

    for category, skills in SKILL_TAXONOMY.items():
        for skill in skills:
            # Build regex word-boundary pattern to avoid partial false matches
            # e.g., 'c' should not match 'react'
            escaped = re.escape(skill)
            # Handle special symbols like c++, c#, .net
            if skill in {"c++", "c#", ".net"}:
                pattern = r'(?:^|\s|\W)' + escaped + r'(?:$|\s|\W)'
            else:
                pattern = r'\b' + escaped + r'\b'

            matches = list(re.finditer(pattern, text_lower))
            if matches:
                # Skill found!
                key = skill.replace(" ", "_")
                found_skills[key] = {
                    "name": skill.title() if len(skill) > 3 else skill.upper(),
                    "raw": skill,
                    "category": category,
                    "count": len(matches)
                }

    return found_skills


def analyze_contact_info(text: str) -> Dict[str, Any]:
    """Check for presence of professional contact channels."""
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', text, re.IGNORECASE)
    github_match = re.search(r'github\.com/[\w-]+', text, re.IGNORECASE)
    portfolio_match = re.search(r'(https?://)?[\w.-]+\.(com|dev|io|me|org)', text, re.IGNORECASE)

    return {
        "email": bool(email_match),
        "phone": bool(phone_match),
        "linkedin": bool(linkedin_match),
        "github": bool(github_match),
        "portfolio": bool(portfolio_match),
        "score": sum([
            1 if email_match else 0,
            1 if phone_match else 0,
            1 if linkedin_match else 0,
            0.5 if github_match else 0
        ])
    }


def analyze_sections_and_structure(text: str) -> Dict[str, Any]:
    """Detect whether standard resume sections exist."""
    lines = text.split("\n")
    found_sections = []
    missing_sections = []

    for sec in STANDARD_SECTIONS:
        matched = False
        for pattern in sec["patterns"]:
            # Check for header-like line
            regex = re.compile(r'^\s*(' + pattern + r')\s*$', re.IGNORECASE)
            for line in lines[:80]: # check reasonable top/middle portion
                if regex.search(line.strip()):
                    matched = True
                    break
            if matched:
                break
        if matched:
            found_sections.append(sec["name"])
        else:
            missing_sections.append(sec["name"])

    return {
        "found_sections": found_sections,
        "missing_sections": missing_sections,
        "section_coverage_pct": round((len(found_sections) / len(STANDARD_SECTIONS)) * 100)
    }


def analyze_metrics_and_action_verbs(text: str) -> Dict[str, Any]:
    """
    Detect quantifiable metrics (% improvements, $ amounts, numbers)
    and leadership action verbs.
    """
    text_lower = text.lower()

    # Detect metric indicators: percentages, dollars, large counts
    percentage_matches = re.findall(r'\b\d+(?:\.\d+)?%', text)
    dollar_matches = re.findall(r'\$\s?\d+(?:,\d+)*(?:\.\d+)?[kKmMbB]?', text)
    multiplier_matches = re.findall(r'\b\d+x\b', text, re.IGNORECASE)
    numerical_metrics = re.findall(r'\b(?:reduced|increased|scaled|saved|cut|boosted|grew|improved)\b[^\.\n]*?\b\d+', text_lower)

    total_metrics_found = len(percentage_matches) + len(dollar_matches) + len(multiplier_matches) + len(numerical_metrics)

    # Detect action verbs
    found_verbs = []
    words = set(re.findall(r'\b[a-zA-Z]+\b', text_lower))
    for verb in ACTION_VERBS:
        if verb in words:
            found_verbs.append(verb.capitalize())

    return {
        "metrics_count": total_metrics_found,
        "percentages": percentage_matches[:5],
        "dollar_amounts": dollar_matches[:5],
        "action_verbs": found_verbs,
        "action_verbs_count": len(found_verbs)
    }


def compute_semantic_similarity(resume_text: str, jd_text: str) -> float:
    """
    Compute TF-IDF Cosine Similarity between resume and job description.
    Yields value between 0.0 and 1.0.
    """
    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000, ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(sim)
    except Exception:
        # Fallback to token overlap Jaccard
        r_words = set(re.findall(r'\b\w{3,}\b', resume_text.lower()))
        j_words = set(re.findall(r'\b\w{3,}\b', jd_text.lower()))
        if not j_words:
            return 0.5
        intersection = len(r_words.intersection(j_words))
        return intersection / len(j_words)


def generate_tailored_suggestions(
    missing_skills: List[Dict[str, Any]],
    matched_skills: List[Dict[str, Any]],
    structure_info: Dict[str, Any],
    metrics_info: Dict[str, Any],
    contact_info: Dict[str, Any],
    word_count: int
) -> List[Dict[str, str]]:
    """
    Create specific, realistic, actionable recommendations categorized by type.
    """
    suggestions = []

    # 1. High Priority Keyword Injection
    if missing_skills:
        top_missing = [s["name"] for s in missing_skills[:4]]
        suggestions.append({
            "category": "Keywords & Skills",
            "priority": "High",
            "title": f"Integrate High-Demand Keywords: {', '.join(top_missing)}",
            "action": (
                f"The job description explicitly highlights {', '.join(top_missing)}. "
                f"Weave these terms directly into your Skills section and substantiate them with bullet points under relevant previous roles."
            ),
            "example": f"Example: 'Leveraged {top_missing[0]} to automate build workflows, reducing deployment cycle times by 35%.'"
        })

    # 2. Measurable Impact & Quantifiable Results
    if metrics_info["metrics_count"] < 3:
        suggestions.append({
            "category": "Experience & Impact",
            "priority": "High",
            "title": "Quantify Achievements with the Google XYZ Formula",
            "action": (
                "Your resume has few quantifiable metrics. Recruiters and ATS screeners favor measurable impact: "
                "'Accomplished [X] as measured by [Y], by doing [Z]'."
            ),
            "example": "Before: 'Worked on database queries to make them faster.'\nAfter: 'Optimized PostgreSQL indexing and query execution plans, reducing p99 latency by 42% across 1.2M daily transactions.'"
        })
    else:
        suggestions.append({
            "category": "Experience & Impact",
            "priority": "Medium",
            "title": "Amplify Scope and Business Metrics",
            "action": (
                f"You have {metrics_info['metrics_count']} metrics. Push further by tying technical efforts to bottom-line results like cost savings ($), customer retention (%), or velocity (x)."
            ),
            "example": "Highlight dollar impact, e.g. 'Saved $120k in annual cloud infrastructure costs through automated autoscaling policies.'"
        })

    # 3. Action Verbs & Leadership
    if metrics_info["action_verbs_count"] < 4:
        suggestions.append({
            "category": "Action Verbs",
            "priority": "Medium",
            "title": "Replace Passive Language with High-Power Action Verbs",
            "action": (
                "Avoid starting bullet points with passive phrases like 'Responsible for', 'Assisted with', or 'Helped'. "
                "Use high-ownership verbs: 'Architected', 'Spearheaded', 'Engineered', 'Optimized', or 'Orchestrated'."
            ),
            "example": "Replace 'Responsible for bug fixes' with 'Spearheaded triage of production incidents, decreasing mean time to resolution (MTTR) by 50%.'"
        })

    # 4. Resume Structure / Sections
    if structure_info["missing_sections"]:
        missing_sec_str = ", ".join(structure_info["missing_sections"])
        suggestions.append({
            "category": "ATS Structure",
            "priority": "High" if "Skills" in structure_info["missing_sections"] or "Summary / Objective" in structure_info["missing_sections"] else "Medium",
            "title": f"Add Missing Standard Headers: {missing_sec_str}",
            "action": (
                f"ATS parsers look for standard naming conventions. Add explicit headers for: {missing_sec_str} to ensure automated parsers categorize your sections correctly."
            ),
            "example": "Use standard titles: 'PROFESSIONAL EXPERIENCE', 'CORE TECHNICAL SKILLS', 'EDUCATION', 'SUMMARY'."
        })

    # 5. Length & Readability
    if word_count < 300:
        suggestions.append({
            "category": "Formatting & Length",
            "priority": "High",
            "title": "Expand Resume Depth (Currently Under 300 words)",
            "action": "Your resume text is very brief. Standard 1-page resumes typically range between 400 and 700 words with 3-5 bullets per major role.",
            "example": "Add technical details about your projects, tools used, and challenges solved."
        })
    elif word_count > 1000:
        suggestions.append({
            "category": "Formatting & Length",
            "priority": "Medium",
            "title": "Condense Resume Content for Rapid Scanning",
            "action": f"At {word_count} words, your resume may exceed 2 pages. Recruiters spend ~7 seconds on initial scan. Condense older roles to 2-3 high-impact bullets.",
            "example": "Focus on the most recent 5-7 years and trim obsolete tools."
        })

    # 6. Contact & Links
    if not contact_info["linkedin"]:
        suggestions.append({
            "category": "Contact & Links",
            "priority": "Low",
            "title": "Include Clean LinkedIn Profile URL",
            "action": "Ensure your custom LinkedIn URL (e.g., linkedin.com/in/yourname) is placed in the header for easy recruiter verification.",
            "example": "Include: linkedin.com/in/alexchen"
        })

    return suggestions


def analyze_resume_nlp(resume_text: str, jd_text: str) -> Dict[str, Any]:
    """
    Main analysis pipeline:
    Extracts skills, computes similarity, checks ATS format,
    and returns a structured report.
    """
    # 1. Clean & tokenize
    r_words = resume_text.split()
    word_count = len(r_words)

    # 2. Extract skills from both documents
    resume_skills_dict = extract_skills_from_text(resume_text)
    jd_skills_dict = extract_skills_from_text(jd_text)

    # 3. Classify matched and missing skills
    matched_skills = []
    missing_skills = []

    for key, jd_skill in jd_skills_dict.items():
        if key in resume_skills_dict:
            matched_skills.append({
                "name": jd_skill["name"],
                "raw": jd_skill["raw"],
                "category": jd_skill["category"],
                "jd_count": jd_skill["count"],
                "resume_count": resume_skills_dict[key]["count"]
            })
        else:
            # Importance ranking: mentioned multiple times in JD = high priority
            is_critical = jd_skill["count"] >= 2
            missing_skills.append({
                "name": jd_skill["name"],
                "raw": jd_skill["raw"],
                "category": jd_skill["category"],
                "jd_count": jd_skill["count"],
                "importance": "High Priority" if is_critical else "Recommended"
            })

    # Additional skills on resume not explicitly in JD (bonus value)
    additional_resume_skills = []
    for key, r_skill in resume_skills_dict.items():
        if key not in jd_skills_dict:
            additional_resume_skills.append({
                "name": r_skill["name"],
                "category": r_skill["category"],
                "resume_count": r_skill["count"]
            })

    # Sort skills by occurrence and priority
    matched_skills.sort(key=lambda s: s["jd_count"], reverse=True)
    missing_skills.sort(key=lambda s: (0 if s["importance"] == "High Priority" else 1, -s["jd_count"]))

    # 4. Structural & ATS checks
    contact_info = analyze_contact_info(resume_text)
    structure_info = analyze_sections_and_structure(resume_text)
    metrics_info = analyze_metrics_and_action_verbs(resume_text)

    # 5. Semantic similarity via TF-IDF
    cosine_sim = compute_semantic_similarity(resume_text, jd_text)
    semantic_score = round(min(100.0, max(20.0, cosine_sim * 140.0))) # Scaled to sensible 20-100 curve

    # 6. Skill match ratio
    total_jd_skills = len(jd_skills_dict)
    if total_jd_skills > 0:
        skill_ratio = len(matched_skills) / total_jd_skills
        skill_score = round(skill_ratio * 100)
    else:
        skill_ratio = 0.7
        skill_score = 70

    # 7. ATS readability & formatting score
    ats_score = 0
    if contact_info["email"]: ats_score += 15
    if contact_info["phone"]: ats_score += 15
    if contact_info["linkedin"]: ats_score += 10
    ats_score += round((len(structure_info["found_sections"]) / len(STANDARD_SECTIONS)) * 40)
    if 350 <= word_count <= 950:
        ats_score += 20
    elif 250 <= word_count <= 1200:
        ats_score += 10
    ats_score = min(100, max(30, ats_score))

    # 8. Experience & Impact score
    exp_score = 30
    exp_score += min(35, metrics_info["metrics_count"] * 8)
    exp_score += min(35, metrics_info["action_verbs_count"] * 6)
    exp_score = min(100, max(25, exp_score))

    # 9. Overall Match Score weighted calculation
    # 40% skills, 25% semantic relevance, 20% experience & impact, 15% ATS structure
    raw_overall = (
        (skill_score * 0.40) +
        (semantic_score * 0.25) +
        (exp_score * 0.20) +
        (ats_score * 0.15)
    )
    overall_score = round(min(98, max(25, raw_overall)))

    # Score grade & badge
    if overall_score >= 82:
        match_tier = "Strong Match"
        tier_color = "emerald"
        tier_summary = "Your profile demonstrates strong alignment with core role requirements and modern ATS standards."
    elif overall_score >= 65:
        match_tier = "Competitive Match"
        tier_color = "amber"
        tier_summary = "Your background shows solid foundational experience, but addressing key missing skills will significantly elevate your candidacy."
    else:
        match_tier = "Needs Optimization"
        tier_color = "rose"
        tier_summary = "There are notable keyword and experience gaps between this resume and the target role requirements."

    # 10. Synthesize Strengths
    strengths = []
    if matched_skills:
        top_matches = [m["name"] for m in matched_skills[:5]]
        strengths.append(f"Strong overlap in core technical competencies: {', '.join(top_matches)}.")
    if metrics_info["metrics_count"] >= 3:
        strengths.append(f"Effective use of quantifiable metrics ({metrics_info['metrics_count']} detected) demonstrating tangible business impact.")
    if metrics_info["action_verbs_count"] >= 4:
        strengths.append(f"Clear leadership language with strong action verbs ({', '.join(metrics_info['action_verbs'][:5])}).")
    if contact_info["email"] and contact_info["linkedin"]:
        strengths.append("Complete professional contact details including verified LinkedIn profile.")
    if structure_info["section_coverage_pct"] >= 80:
        strengths.append("Well-structured document architecture following standard ATS section headings.")

    # 11. Synthesize Gaps / Concerns
    gaps = []
    high_priority_missing = [s["name"] for s in missing_skills if s["importance"] == "High Priority"]
    if high_priority_missing:
        gaps.append(f"Missing high-frequency job keywords: {', '.join(high_priority_missing[:6])}.")
    if len(missing_skills) > len(matched_skills):
        gaps.append(f"Job demands {len(missing_skills)} skills not explicitly verified in your resume text.")
    if metrics_info["metrics_count"] < 3:
        gaps.append("Few quantifiable metrics: experience bullets focus more on responsibilities than measurable outcomes.")
    if structure_info["missing_sections"]:
        gaps.append(f"Missing expected standard sections: {', '.join(structure_info['missing_sections'])}.")
    if word_count < 350:
        gaps.append(f"Brief resume length ({word_count} words) may fail keyword depth checks on automated ATS screens.")

    # 12. Tailored Suggestions
    suggestions = generate_tailored_suggestions(
        missing_skills=missing_skills,
        matched_skills=matched_skills,
        structure_info=structure_info,
        metrics_info=metrics_info,
        contact_info=contact_info,
        word_count=word_count
    )

    return {
        "analysis_mode": "Local Semantic NLP & ATS Engine",
        "is_ai_live": False,
        "overall_score": overall_score,
        "match_tier": match_tier,
        "tier_color": tier_color,
        "tier_summary": tier_summary,
        "sub_scores": {
            "skill_match": skill_score,
            "semantic_relevance": semantic_score,
            "experience_impact": exp_score,
            "ats_readability": ats_score
        },
        "stats": {
            "resume_word_count": word_count,
            "matched_skills_count": len(matched_skills),
            "missing_skills_count": len(missing_skills),
            "metrics_detected": metrics_info["metrics_count"],
            "action_verbs_detected": metrics_info["action_verbs_count"]
        },
        "skills": {
            "matched": matched_skills,
            "missing": missing_skills,
            "additional": additional_resume_skills[:8]
        },
        "strengths": strengths,
        "gaps": gaps,
        "suggestions": suggestions,
        "ats_checklist": {
            "email_present": contact_info["email"],
            "phone_present": contact_info["phone"],
            "linkedin_present": contact_info["linkedin"],
            "sections_found": structure_info["found_sections"],
            "sections_missing": structure_info["missing_sections"]
        },
        "disclaimer": "This score and breakdown is an automated heuristic and semantic estimate for resume optimization purposes. It does not reflect a hiring decision or human evaluation."
    }
