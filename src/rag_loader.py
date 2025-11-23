import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_role_context(role_name: str) -> dict:
    """
    Load the role-specific context from the JSON knowledge base.

    This function loads the complete role configuration including
    base questions, competencies, sample answers, and evaluation criteria.

    Args:
        role_name (str): The name of the role (e.g., "engineer", "product", "sales",
                        "Software Engineer", "Product Manager", "Sales Representative").

    Returns:
        dict: A dictionary containing the role context with keys:
              - role: Role name
              - base_questions: List of core interview questions
              - competencies: List of key competencies
              - sample_good_answers: List of strong example answers
              - sample_bad_answers: List of weak example answers
              - evaluation_criteria: List of evaluation criteria
              - stages: Interview stages (if available)
              Returns an empty dict if the role file is not found or invalid.

    Raises:
        No exceptions are raised. Errors are logged and an empty dict is returned.

    Example:
        >>> context = load_role_context("engineer")
        >>> print(context["base_questions"][0])
        'Can you explain the difference between a process and a thread?'
    """
    if not role_name:
        logger.error("Role name is empty.")
        return {}

    # Normalize role name to filename
    # Support both short names and full role titles
    role_map = {
        "software engineer": "engineer",
        "engineer": "engineer",
        "product manager": "product",
        "product": "product",
        "sales representative": "sales",
        "sales": "sales"
    }

    normalized_name = role_map.get(role_name.lower())
    if not normalized_name:
        logger.warning(f"Unknown role name: {role_name}. Available roles: {list(set(role_map.values()))}")
        return {}

    # Construct file path relative to project root
    # This function may be called from src/ or project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    file_path = os.path.join(project_root, "roles", f"{normalized_name}.json")

    # Fallback to relative path if absolute doesn't work
    if not os.path.exists(file_path):
        file_path = os.path.join("roles", f"{normalized_name}.json")

    if not os.path.exists(file_path):
        logger.error(f"Role file not found: {file_path}")
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Validate required fields
        required_fields = ["role", "base_questions", "competencies"]
        for field in required_fields:
            if field not in data:
                logger.warning(f"Role file {file_path} missing required field: {field}")

        # Log successful load
        logger.info(f"Successfully loaded role context for: {data.get('role', normalized_name)}")

        return data

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON for role {role_name}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error loading role {role_name}: {e}")
        return {}
