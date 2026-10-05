import re
import math
from typing import List, Dict, Any, Tuple
from app.utils.skill_taxonomy import (
    SKILL_TAXONOMY,
    ACTION_VERBS,
    normalize_skill,
    get_all_hard_skills,
    get_all_soft_skills
)

class NLPEngine:
    """
    Local Natural Language Processing Engine for ATS Scoring, Skill Extraction,
    Action Verb Frequency, and Semantic Similarity (TF-IDF & Cosine Similarity).
    Works offline with zero external API dependencies.
    """

    @classmethod
    def extract_skills(cls, text: str) -> Dict[str, List[str]]:
        """
        Extract Hard Skills and Soft Skills from text using word boundary matching.
        """
        text_lower = f" {text.lower()} "
        found_hard = set()
        found_soft = set()
        
        # Hard skills extraction
        for category, skills in SKILL_TAXONOMY.items():
            if category == "soft_skills":
                continue
            for skill in skills:
                # Escape special regex characters (like c++, .net, c#)
                escaped = re.escape(skill)
                # Word boundary matching
                pattern = r'(?:\b|\s)' + escaped + r'(?:\b|\s|[,\.\;\:\)])'
                if re.search(pattern, text_lower):
                    found_hard.add(normalize_skill(skill))
                    
        # Soft skills extraction
        for soft_skill in SKILL_TAXONOMY["soft_skills"]:
            escaped = re.escape(soft_skill)
            pattern = r'(?:\b|\s)' + escaped + r'(?:\b|\s|[,\.\;\:\)])'
            if re.search(pattern, text_lower):
                found_soft.add(normalize_skill(soft_skill))

        all_skills = sorted(list(found_hard.union(found_soft)))
        return {
            "all_skills": all_skills,
            "hard_skills": sorted(list(found_hard)),
            "soft_skills": sorted(list(found_soft))
        }

    @classmethod
    def analyze_action_verbs_and_metrics(cls, text: str) -> Dict[str, Any]:
        """
        Analyze the strength of resume bullet points:
        - Quantifiable metrics (%, $, numbers, multipliers like 3x, 50k)
        - Action verbs (spearheaded, architected, delivered, etc.)
        """
        text_lower = text.lower()
        
        # Quantifiable metrics pattern
        metric_pattern = r'(\b\d+%\b|\$\d+[\d,]*|\b\d+x\b|\b\d+\s*(?:million|billion|k|percent|users|clients|requests|ms|seconds)\b|\bincreased\s+by\s+\d+|\breduced\s+by\s+\d+)'
        metrics_found = re.findall(metric_pattern, text_lower)
        
        # Action verbs count
        action_verb_hits = []
        for cat, verbs in ACTION_VERBS.items():
            for v in verbs:
                if re.search(r'\b' + v + r'\b', text_lower):
                    action_verb_hits.append(v)
                    
        return {
            "metrics_count": len(metrics_found),
            "metrics_samples": metrics_found[:5],
            "action_verbs_count": len(action_verb_hits),
            "action_verbs_found": list(set(action_verb_hits))
        }

    @classmethod
    def calculate_ats_score(cls, text: str, parsed_sections: Dict[str, str], extracted_skills: Dict[str, List[str]]) -> Tuple[float, Dict[str, float], List[str], List[str]]:
        """
        Calculate ATS compatibility score (0 - 100) based on 4 key dimensions:
        1. Keyword Density & Skill Breadth (35%)
        2. Section Completeness & Layout (25%)
        3. Impact & Quantifiable Metrics (25%)
        4. Contact Info & Readability (15%)
        """
        strengths = []
        weaknesses = []
        
        # 1. Keywords & Skills (0 - 100)
        hard_count = len(extracted_skills.get("hard_skills", []))
        soft_count = len(extracted_skills.get("soft_skills", []))
        
        if hard_count >= 12:
            kw_score = 100.0
            strengths.append(f"Strong technical skill footprint ({hard_count} hard skills recognized by ATS).")
        elif hard_count >= 7:
            kw_score = 80.0 + (hard_count - 7) * 4
            strengths.append(f"Good technical vocabulary ({hard_count} skills identified).")
        else:
            kw_score = max(35.0, hard_count * 10.0)
            weaknesses.append("Skill section is sparse. Add specific technologies, frameworks, and tools to beat ATS filters.")

        # 2. Section Completeness (0 - 100)
        sections_found = [k for k, v in parsed_sections.items() if len(v.strip()) > 30]
        completeness_score = min(100.0, (len(sections_found) / 5.0) * 100.0)
        
        if "experience" in sections_found:
            strengths.append("Clear work experience structure.")
        else:
            weaknesses.append("Missing or unparseable Work Experience section header.")
            
        if "education" not in sections_found:
            weaknesses.append("Missing standard Education section header.")

        # 3. Impact & Metrics (0 - 100)
        impact_analysis = cls.analyze_action_verbs_and_metrics(text)
        metrics_count = impact_analysis["metrics_count"]
        verbs_count = impact_analysis["action_verbs_count"]
        
        metric_score = min(100.0, (metrics_count / 5.0) * 50.0 + (verbs_count / 8.0) * 50.0)
        
        if metrics_count >= 4:
            strengths.append(f"Excellent quantifiable achievements found ({metrics_count} metrics detected).")
        else:
            weaknesses.append("Lacks quantifiable impact. Add metrics (e.g., 'boosted API speed by 40%', 'managed $100k budget').")

        # 4. Formatting & Length (0 - 100)
        word_count = len(text.split())
        if 350 <= word_count <= 1100:
            format_score = 95.0
            strengths.append(f"Optimal resume length ({word_count} words).")
        elif word_count < 250:
            format_score = 50.0
            weaknesses.append(f"Resume is very short ({word_count} words). Expand on responsibilities and achievements.")
        else:
            format_score = 75.0
            weaknesses.append("Resume is somewhat lengthy. Consider condensing to 1-2 pages.")

        # Overall Weighted Score
        overall = round(
            (kw_score * 0.35) +
            (completeness_score * 0.25) +
            (metric_score * 0.25) +
            (format_score * 0.15),
            1
        )
        
        breakdown = {
            "keywords": round(kw_score, 1),
            "formatting": round(format_score, 1),
            "impact_metrics": round(metric_score, 1),
            "section_completeness": round(completeness_score, 1),
            "overall": overall
        }
        
        return overall, breakdown, strengths, weaknesses

    @classmethod
    def calculate_cosine_similarity(cls, text1: str, text2: str) -> float:
        """
        Calculate semantic TF-IDF Cosine Similarity between Resume and Job Description.
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return round(float(sim) * 100.0, 1)
        except Exception:
            # Fallback word-overlap Jaccard similarity if scikit-learn is not ready
            words1 = set(re.findall(r'\w+', text1.lower()))
            words2 = set(re.findall(r'\w+', text2.lower()))
            if not words1 or not words2:
                return 0.0
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            return round((len(intersection) / len(union)) * 100.0 * 2.5, 1) # scaled for readability
