import json
from typing import Dict, Any, List
from app.services.llm_engine import LLMEngine

class InterviewPrepService:
    """
    Generates intelligent behavioral and technical interview questions,
    strategic STAR answers, and resume-linked talking points.
    """

    @classmethod
    async def generate_interview_prep(
        cls,
        resume_text: str,
        job_title: str,
        job_description: str = "",
        question_count: int = 5,
        provider: str = "auto"
    ) -> Dict[str, Any]:
        
        system_prompt = (
            "You are a principal technical interviewer and executive talent coach at top tech companies. "
            "Generate rigorous, highly realistic interview questions combining Technical, System Design, "
            "and Behavioral (STAR method) scenarios tailored to the candidate's resume and target job. "
            "Output valid JSON only with key 'questions' containing a list of objects with: "
            "'category', 'question', 'why_asked', 'recommended_star_answer', 'resume_talking_point'."
        )
        
        user_prompt = f"""
Target Job Title: {job_title}
Target Job Description: {job_description[:1200] if job_description else 'A role requiring strong software architecture, problem solving, and leadership.'}
Candidate Resume Snippet: {resume_text[:1500]}

Generate {question_count} interview questions across Technical, System Design, Behavioral, and Leadership categories.
Return JSON format:
{{
  "questions": [
    {{
      "category": "Technical Architecture",
      "question": "...",
      "why_asked": "...",
      "recommended_star_answer": "...",
      "resume_talking_point": "..."
    }}
  ]
}}
"""
        response_text = await LLMEngine.generate_response(system_prompt, user_prompt, provider=provider)
        
        try:
            clean = response_text.strip()
            if clean.startswith("```"):
                clean = clean.split("```", 2)[1]
                if clean.startswith("json"):
                    clean = clean[4:].strip()
            data = json.loads(clean)
            return {
                "job_title": job_title,
                "questions": data.get("questions", [])
            }
        except Exception:
            # High-quality fallback interview questions
            return {
                "job_title": job_title,
                "questions": [
                    {
                        "category": "Technical Depth",
                        "question": f"How do you design a scalable system for {job_title} that handles spikes in traffic?",
                        "why_asked": "Tests architectural acumen, understanding of caching, asynchronous processing, and horizontal scaling.",
                        "recommended_star_answer": "Situation: Past high-volume project. Task: Scale throughput. Action: Deployed Redis cache, partitioned database tables, implemented async workers. Result: Handled 5x peak traffic with zero downtime.",
                        "resume_talking_point": "Discuss your past backend or full-stack projects and latency benchmarks."
                    },
                    {
                        "category": "Behavioral (STAR)",
                        "question": "Tell me about a time you had to make a difficult technical trade-off under a tight deadline.",
                        "why_asked": "Evaluates pragmatic engineering judgment, technical debt management, and stakeholder communication.",
                        "recommended_star_answer": "Focus on balancing speed to market with maintainability, documenting debt, and scheduling refactoring in subsequent sprints.",
                        "resume_talking_point": "Reference a project where you shipped a feature quickly while preserving test coverage."
                    },
                    {
                        "category": "Problem Solving",
                        "question": "Walk me through how you diagnose an intermittent production issue with high latency.",
                        "why_asked": "Assesses observational debugging, telemetry inspection, log aggregation, and APM tracing.",
                        "recommended_star_answer": "Check APM flame graphs, database slow query logs, network IO latency, and CPU/memory exhaustion.",
                        "resume_talking_point": "Highlight your experience with debugging tools, metrics, and CI/CD pipelines."
                    }
                ]
            }
