import json
from typing import Dict, Any, List
from app.services.llm_engine import LLMEngine

class CoverLetterService:
    """
    Generates tailored cover letters tailored to specific jobs, company culture, and candidate background.
    """

    @classmethod
    async def generate_cover_letter(
        cls,
        candidate_name: str,
        resume_text: str,
        job_title: str,
        company_name: str,
        job_description: str = "",
        tone: str = "professional",
        custom_notes: str = "",
        provider: str = "auto"
    ) -> Dict[str, Any]:
        
        system_prompt = (
            "You are an executive career strategist and top tech recruiter. "
            "Write an engaging, persuasive, and tailored cover letter matching the candidate's actual accomplishments "
            "to the specified job requirements. Output valid JSON only with keys: 'cover_letter' (string) and 'key_selling_points' (list of strings)."
        )
        
        user_prompt = f"""
Candidate Name: {candidate_name or 'Candidate'}
Target Role: {job_title}
Target Company: {company_name}
Tone: {tone}
Special Notes/Focus: {custom_notes or 'Focus on technical depth and measurable project outcomes'}

Candidate Resume Highlights:
{resume_text[:2000]}

Target Job Description:
{job_description[:1500] if job_description else f"A high-growth role for a {job_title} at {company_name}"}

Instructions:
1. Write 3-4 structured paragraphs: Strong opening hook, relevant technical achievements with metrics, why {company_name}, and professional call to action.
2. Incorporate a {tone} tone.
3. Return JSON format:
{{"cover_letter": "...", "key_selling_points": ["point 1", "point 2", "point 3"]}}
"""
        response_text = await LLMEngine.generate_response(system_prompt, user_prompt, provider=provider)
        
        # Parse JSON response
        try:
            # Clean markdown codeblocks if returned
            clean = response_text.strip()
            if clean.startswith("```"):
                clean = clean.split("```", 2)[1]
                if clean.startswith("json"):
                    clean = clean[4:].strip()
            data = json.loads(clean)
            return {
                "job_title": job_title,
                "company_name": company_name,
                "tone": tone,
                "cover_letter": data.get("cover_letter", ""),
                "key_selling_points": data.get("key_selling_points", [])
            }
        except Exception:
            # Fallback format
            return {
                "job_title": job_title,
                "company_name": company_name,
                "tone": tone,
                "cover_letter": response_text,
                "key_selling_points": [
                    f"Strong alignment with {job_title} core responsibilities",
                    "Demonstrated record of delivering performant software solutions",
                    "Clear communication and enthusiasm for " + company_name
                ]
            }
