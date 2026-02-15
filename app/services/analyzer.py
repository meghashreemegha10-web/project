import re
from typing import List, Dict
from pydantic import BaseModel



# Mock database of market needs - In a real app this would come from an API or DB
MARKET_NEEDS = {
    "python": 10, "java": 8, "react": 9, "aws": 9, "docker": 8,
    "kubernetes": 9, "communication": 7, "leadership": 8, "sql": 8,
    "fastapi": 9, "machine learning": 10, "nlp": 10, "ai": 10,
    "project management": 7, "agile": 7, "scrum": 6
}

class AnalysisResult(BaseModel):
    score: int
    found_skills: List[str]
    missing_critical_skills: List[str]
    summary: str

class ResumeAnalyzer:
    def __init__(self):
        pass

    def analyze(self, text: str) -> AnalysisResult:
        text_lower = text.lower()
        found_skills = []
        matched_weights = 0
        
        # Robust keyword matching (works with or without spacy)
        for skill, weight in MARKET_NEEDS.items():
            # Use regex for word boundary matching to avoid partial matches (e.g. "java" in "javascript")
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.append(skill)
                matched_weights += weight
        
        # Calculate Score
        # Heuristic: 50 points base + points from skills. Max 100.
        # If matched weights > 50, we consider it a very strong profile.
        score = min(100, int(matched_weights * 1.5)) 
        if MatchScore := int(matched_weights * 1.5): # duplicate logic fix
             score = min(100, MatchScore)

        if len(found_skills) == 0:
            score = 10 # Participation award
        
        # Identify missing high-value skills
        missing_skills = [
            s for s, w in sorted(MARKET_NEEDS.items(), key=lambda x: x[1], reverse=True)
            if s not in found_skills
        ][:5]
        
        # Generate Summary
        summary = f"Detected {len(found_skills)} relevant market skills. "
        if score >= 80:
            summary += "Excellent candidate with strong alignment to current market needs."
        elif score >= 50:
            summary += "Good candidate matches. Consider checking for specific domain expertise."
        else:
            summary += "Low match with current high-demand market skills."

        return AnalysisResult(
            score=score,
            found_skills=found_skills,
            missing_critical_skills=missing_skills,
            summary=summary
        )
