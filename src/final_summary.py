"""
Final interview summary generation module.
Uses LangChain and Groq to create comprehensive feedback reports.
"""

from groq_client import groq_chat
from rag_loader import load_role_context


def generate_final_summary(state: dict) -> str:
    """
    Generate a comprehensive final summary for the completed interview.
    
    This function:
    1. Aggregates all scores from the interview
    2. Collects strengths and improvement areas
    3. Uses Groq LLM to generate a detailed, personalized summary
    4. Returns formatted feedback text
    
    Args:
        state (dict): Interview state containing scores, answers, role, and context
        
    Returns:
        str: Formatted final summary text with scores, strengths, and recommendations
    """
    
    # =========================================
    # 1. AGGREGATE SCORES
    # =========================================
    
    scores = state.get("scores", [])
    
    if not scores:
        return "Interview completed, but no scores were recorded. Please try again."
    
    # Filter out error scores
    valid_scores = [s for s in scores if "error" not in s]
    
    if not valid_scores:
        return "Interview completed, but scoring encountered errors. Please try again."
    
    # Compute averages
    avg_communication = sum(s.get("communication", 0) for s in valid_scores) / len(valid_scores)
    avg_technical = sum(s.get("technical", 0) for s in valid_scores) / len(valid_scores)
    avg_behavioral = sum(s.get("behavioral", 0) for s in valid_scores) / len(valid_scores)
    avg_structure = sum(s.get("structure", 0) for s in valid_scores) / len(valid_scores)
    
    # Round to nearest integer
    avg_communication = round(avg_communication)
    avg_technical = round(avg_technical)
    avg_behavioral = round(avg_behavioral)
    avg_structure = round(avg_structure)
    
    # =========================================
    # 2. COLLECT STRENGTHS AND IMPROVEMENTS
    # =========================================
    
    all_strengths = []
    all_improvements = []
    
    for score in valid_scores:
        all_strengths.extend(score.get("strengths", []))
        all_improvements.extend(score.get("improvements", []))
    
    # Deduplicate while preserving order
    strengths_unique = list(dict.fromkeys(all_strengths))
    improvements_unique = list(dict.fromkeys(all_improvements))
    
    # =========================================
    # 3. LOAD ROLE CONTEXT
    # =========================================
    
    role = state.get("role", "general")
    context = load_role_context(role) if role else {}
    
    role_name = context.get("role", role.title())
    competencies = context.get("competencies", [])
    competencies_str = ", ".join(competencies) if competencies else "general interview skills"
    
    # =========================================
    # 4. BUILD PROMPTS FOR GROQ
    # =========================================
    
    system_prompt = (
        "You are an expert interview evaluator and career coach. "
        "Your task is to generate a final structured summary for a completed practice interview. "
        "Be encouraging but honest. Provide specific, actionable feedback. "
        "Format your response in a clear, professional manner with sections and bullet points."
    )
    
    user_prompt = f"""
Generate a comprehensive interview evaluation summary based on the following data:

**Role:** {role_name}

**Overall Scores (0-10 scale):**
- Communication: {avg_communication}/10
- Technical: {avg_technical}/10
- Behavioral: {avg_behavioral}/10
- Structure: {avg_structure}/10

**Key Strengths Identified:**
{chr(10).join(f"- {s}" for s in strengths_unique[:8])}

**Areas for Improvement:**
{chr(10).join(f"- {i}" for i in improvements_unique[:8])}

**Interview Statistics:**
- Total Questions Answered: {len(state.get("answers", []))}
- Role Competencies Evaluated: {competencies_str}

Please generate a final summary that includes:
1. An opening statement about overall performance
2. A breakdown of the scores with brief explanations
3. Top 3-5 strengths to celebrate
4. Top 3-5 improvement areas with specific action items
5. A motivating closing statement

Keep the tone professional yet encouraging.
"""
    
    # =========================================
    # 5. CALL GROQ LLM
    # =========================================
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        summary = groq_chat(messages, temperature=0.7)  # Slightly higher temp for creativity
        return summary
    except Exception as e:
        # Fallback to basic summary if LLM fails
        fallback_summary = f"""
🎉 **Interview Complete!**

**Overall Performance for {role_name} Role:**

**Scores:**
- Communication: {avg_communication}/10
- Technical: {avg_technical}/10
- Behavioral: {avg_behavioral}/10
- Structure: {avg_structure}/10

**Key Strengths:**
{chr(10).join(f"✓ {s}" for s in strengths_unique[:5])}

**Areas for Improvement:**
{chr(10).join(f"→ {i}" for i in improvements_unique[:5])}

**Next Steps:**
Focus on the improvement areas above and keep practicing. Great work!

_(Note: Detailed AI summary failed: {str(e)})_
"""
        return fallback_summary
