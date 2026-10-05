from typing import Dict, Any, List
from app.services.nlp_engine import NLPEngine
from app.utils.skill_taxonomy import normalize_skill

class JobMatcherService:
    """
    Evaluates compatibility between a candidate resume and a job vacancy
    using multidimensional scoring (Skills, Semantic Similarity, Experience).
    """

    @classmethod
    def match_resume_to_job(cls, resume_text: str, resume_skills: List[str], job_title: str, job_description: str, job_required_skills: List[str] = None) -> Dict[str, Any]:
        # 1. Extract job skills if not provided
        if not job_required_skills:
            job_skill_data = NLPEngine.extract_skills(f"{job_title} {job_description}")
            job_required_skills = job_skill_data.get("hard_skills", [])

        # Normalize skill sets
        cand_skills_set = set([s.lower() for s in resume_skills])
        job_skills_lower = [s.lower() for s in job_required_skills]
        
        # Identify matched and missing skills
        matched = []
        missing = []
        for s in job_required_skills:
            if s.lower() in cand_skills_set:
                matched.append(s)
            else:
                missing.append(s)

        # 2. Calculate Skill Match Score (0 - 100)
        if job_required_skills:
            skill_score = round((len(matched) / len(job_required_skills)) * 100.0, 1)
        else:
            skill_score = 75.0

        # 3. Calculate Semantic Cosine Similarity (0 - 100)
        semantic_score = NLPEngine.calculate_cosine_similarity(resume_text, f"{job_title} {job_description}")
        # Normalize semantic score to reasonable recruiter baseline
        adjusted_semantic = min(100.0, round(semantic_score * 1.6 + 25.0, 1)) if semantic_score > 0 else 50.0

        # 4. Experience & Keyword Density Heuristics
        exp_score = 80.0
        if any(word in resume_text.lower() for word in ["lead", "senior", "principal", "architect", "5+ years", "10+ years"]):
            exp_score = 95.0
        elif any(word in resume_text.lower() for word in ["intern", "junior", "student"]):
            exp_score = 65.0

        # 5. Composite Match Score
        # 50% Skills + 30% Semantic + 20% Experience
        overall_match = round((skill_score * 0.50) + (adjusted_semantic * 0.30) + (exp_score * 0.20), 1)
        overall_match = min(99.0, max(25.0, overall_match)) # Keep in realistic 25%-99% range

        # 6. Generate Tailored Advice & Strengths
        strengths = []
        if matched:
            strengths.append(f"Strong overlap in core technologies: {', '.join(matched[:5])}.")
        if len(matched) >= 4:
            strengths.append("High keyword relevance for recruiter screening software.")
            
        recommendations = []
        if missing:
            recommendations.append(f"Incorporate missing core keywords into your experience bullets: {', '.join(missing[:4])}.")
        recommendations.append(f"Highlight projects or practical experience solving problems specific to {job_title}.")
        recommendations.append("Ensure your summary section opens with target title and key accomplishments.")

        fit_summary = (
            f"Candidate is a {overall_match:.0f}% match for {job_title}. "
            f"Possesses {len(matched)} of {len(job_required_skills)} required technical competencies."
        )

        return {
            "match_score": overall_match,
            "skills_match_score": skill_score,
            "experience_match_score": exp_score,
            "semantic_similarity_score": adjusted_semantic,
            "matched_skills": matched,
            "missing_critical_skills": missing[:8],
            "missing_nice_to_have": missing[8:15] if len(missing) > 8 else [],
            "fit_summary": fit_summary,
            "strengths_for_job": strengths,
            "tailored_recommendations": recommendations,
            "interview_focus_areas": [
                f"Deep dive into your experience working with {matched[0]}" if matched else "System design and architecture",
                "How you bridge the gap with technologies like " + (missing[0] if missing else "new frameworks"),
                "Measurable business impact and ownership from past projects"
            ]
        }
