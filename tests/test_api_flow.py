import sys
import httpx
from pathlib import Path

# Add backend directory to sys.path so app imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

# Ensure UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def get_test_client():
    # Attempt connecting to live server first, otherwise fall back to TestClient
    try:
        live_client = httpx.Client(base_url="http://127.0.0.1:8000/api/v1", timeout=5.0)
        res = live_client.get("/jobs/")
        if res.status_code == 200:
            print("[INFO] Testing against LIVE server on http://127.0.0.1:8000/api/v1")
            return live_client
    except Exception:
        pass
    
    from fastapi.testclient import TestClient
    from app.main import app
    print("[INFO] Testing using in-process FastAPI TestClient")
    return TestClient(app, base_url="http://testserver/api/v1")

def test_full_pipeline():
    client = get_test_client()

    # 1. Analyze Sample Resume
    sample_text = """ALEX RIVERA
San Francisco, CA | alex.rivera@airesume.io | (555) 234-5678 | linkedin.com/in/alexrivera

SUMMARY
Senior Full Stack Engineer with 6+ years experience architecting scalable distributed systems and REST microservices in Python, FastAPI, React, and PostgreSQL.

SKILLS
Python, FastAPI, Django, React, TypeScript, Docker, Kubernetes, PostgreSQL, Redis, AWS, CI/CD, Git

EXPERIENCE
Senior Software Engineer | TechCorp Inc. | 2021 - Present
- Architected and deployed 15+ microservices in FastAPI reducing p99 API latency by 45%.
- Implemented Redis caching and PostgreSQL query optimization supporting 200k DAU.
- Engineered CI/CD release pipelines with Docker and GitHub Actions.

EDUCATION
B.S. in Computer Science | UC Berkeley | 2015 - 2019"""

    res = client.post("/resumes/analyze-text", json={
        "raw_text": sample_text,
        "target_job_title": "Senior Full Stack Engineer"
    })
    assert res.status_code == 200, f"Failed resume analysis: {res.text}"
    resume_data = res.json()
    print(f"[PASS] 1. Resume Analyzed: ATS Score = {resume_data.get('ats_score')}, Skills = {len(resume_data.get('extracted_skills', []))}")

    # 2. Fetch Jobs
    jobs_res = client.get("/jobs/")
    assert jobs_res.status_code == 200
    jobs = jobs_res.json()
    assert len(jobs) > 0, "No jobs returned"
    print(f"[PASS] 2. Active Jobs Found: {len(jobs)} jobs in database")

    # 3. Match Single Job
    target_job = jobs[0]
    match_res = client.post("/match/match-single", json={
        "resume_id": resume_data["id"],
        "job_id": target_job["id"]
    })
    assert match_res.status_code == 200
    match_data = match_res.json()
    print(f"[PASS] 3. Match Result against '{target_job['title']}': {match_data.get('match_score')}% Match")

    # 4. Batch Match
    batch_res = client.post(f"/match/batch-match/{resume_data['id']}")
    assert batch_res.status_code == 200
    batch_data = batch_res.json()
    print(f"[PASS] 4. Batch Match: Evaluated {batch_data.get('total_jobs_evaluated')} jobs")

    # 5. AI Cover Letter
    cl_res = client.post("/ai-tools/cover-letter", json={
        "resume_id": resume_data["id"],
        "job_title": target_job["title"],
        "company_name": target_job["company"],
        "tone": "professional"
    })
    assert cl_res.status_code == 200
    cl_data = cl_res.json()
    print(f"[PASS] 5. Cover Letter Generated: {len(cl_data.get('cover_letter', ''))} characters")

    # 6. Bullet Optimizer
    bo_res = client.post("/ai-tools/optimize-bullets", json={
        "bullet_points": ["Built backend APIs and resolved issues", "Helped with frontend components"],
        "target_role": "Senior Full Stack Engineer"
    })
    assert bo_res.status_code == 200
    bo_data = bo_res.json()
    print(f"[PASS] 6. Bullet Points Optimized: {len(bo_data.get('optimized_bullets', []))} bullets transformed")

    # 7. Interview Prep
    ip_res = client.post("/ai-tools/interview-prep", json={
        "job_title": target_job["title"],
        "question_count": 3
    })
    assert ip_res.status_code == 200
    ip_data = ip_res.json()
    print(f"[PASS] 7. Interview Prep Q&A: {len(ip_data.get('questions', []))} questions generated")

    # 8. Career Roadmap
    cr_res = client.post("/ai-tools/career-roadmap", json={
        "target_role": "Staff Cloud Architect",
        "current_skills": ["Python", "Docker", "FastAPI"]
    })
    assert cr_res.status_code == 200
    cr_data = cr_res.json()
    print(f"[PASS] 8. Career Roadmap: {len(cr_data.get('milestones', []))} phases planned")

    # 9. Application Tracker
    app_res = client.post("/tracker/", json={
        "company_name": target_job["company"],
        "job_title": target_job["title"],
        "status": "APPLIED",
        "match_score": match_data.get("match_score", 90),
        "job_id": target_job["id"],
        "resume_id": resume_data["id"]
    })
    assert app_res.status_code == 201
    app_data = app_res.json()
    print(f"[PASS] 9. Tracked Application Created: ID = {app_data.get('id')}")

    # 10. PDF Export
    pdf_res = client.get(f"/resumes/{resume_data['id']}/export-pdf")
    assert pdf_res.status_code == 200
    assert len(pdf_res.content) > 1000
    print(f"[PASS] 10. PDF ATS Scorecard Download: {len(pdf_res.content)} bytes generated successfully")

    print("\nALL 10 END-TO-END PIPELINE TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    test_full_pipeline()
