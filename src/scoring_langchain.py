# scoring_langchain.py
# Updated for LangChain 0.1+ and Groq LLM scoring with strict JSON output.

import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


def score_answer(question: str, answer: str, role: str = "engineer") -> dict:
    """
    Score a candidate's answer using the Groq LLM with strict JSON output.

    Returns dict:
    {
        "communication": int,
        "technical": int,
        "behavioral": int,
        "structure": int,
        "strengths": [...],
        "improvements": [...]
    }
    """

    # Ensure API key exists
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")

    # Define JSON schema for structured output
    json_schema = {
        "type": "object",
        "properties": {
            "communication": {"type": "integer"},
            "technical": {"type": "integer"},
            "behavioral": {"type": "integer"},
            "structure": {"type": "integer"},
            "strengths": {"type": "array", "items": {"type": "string"}},
            "improvements": {"type": "array", "items": {"type": "string"}}
        },
        "required": [
            "communication",
            "technical",
            "behavioral",
            "structure",
            "strengths",
            "improvements"
        ]
    }

    parser = JsonOutputParser(json_schema=json_schema)

    # Create evaluation prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert interview evaluator. "
                "Score the candidate's response using ONLY the provided JSON schema. "
                "Never include explanations outside JSON."
            ),
            (
                "user",
                (
                    "Role: {role}\n\n"
                    "Interview Question: {question}\n"
                    "Candidate Answer: {answer}\n\n"
                    "Evaluate the answer based on:\n"
                    "1. Communication clarity\n"
                    "2. Technical depth\n"
                    "3. Behavioral maturity\n"
                    "4. Structure (STAR method)\n\n"
                    "Return ONLY valid JSON using this schema:\n"
                    "{format_instructions}"
                )
            ),
        ]
    )

    chain = (
        prompt
        | ChatGroq(
            model="llama3-70b-8192",
            temperature=0,
            groq_api_key=api_key,
        )
        | parser
    )

    try:
        # Invoke chain with actual inputs
        return chain.invoke(
            {
                "role": role,
                "question": question,
                "answer": answer,
                "format_instructions": parser.get_format_instructions(),
            }
        )

    except ValueError as e:
        # JSON parsing errors and parser errors show up here
        return {"error": f"Failed to parse LLM output as JSON: {str(e)}"}

    except Exception as e:
        return {"error": f"LLM scoring failed: {str(e)}"}
