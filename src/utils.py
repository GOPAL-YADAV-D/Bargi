# Shared helpers
import json
import os


def load_role_config(role_name):
    """
    Load role configuration from JSON file.
    
    Args:
        role_name: Name of the role (e.g., "engineer", "product", "sales")
        
    Returns:
        Role configuration dictionary
    """
    role_path = os.path.join("roles", f"{role_name}.json")
    with open(role_path, "r") as f:
        return json.load(f)


def save_session(session_data, session_id):
    """
    Save interview session data.
    
    Args:
        session_data: Session data to save
        session_id: Unique session identifier
    """
    pass


def format_timestamp(timestamp):
    """
    Format timestamp for display.
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        Formatted timestamp string
    """
    pass
