import json
import os

def load_role_config(role_name):
    """Load role configuration from JSON file."""
    try:
        # Map friendly names to filenames
        role_map = {
            "software engineer": "engineer.json",
            "product manager": "product.json",
            "sales": "sales.json"
        }
        
        filename = role_map.get(role_name.lower())
        if not filename:
            return None
            
        path = os.path.join("roles", filename)
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading role {role_name}: {e}")
        return None

def new_state():
    """
    Initialize a new interview state.
    """
    return {
        "stage": "setup",  # setup -> await_role -> interview -> finished
        "role": None,
        "context": None,  # Loaded role context from JSON
        "history": [],  # Full conversation history
        "answers": [],  # User answers for final summary
        "scores": [],  # Scoring results for each answer
        "current_question_index": 0,  # Track which base question we're on
        "max_questions": 5,  # Number of main questions to ask
        "followup_stage": False,  # Toggle between main question and follow-up
        "current_question": None  # The question the user is currently answering
    }

def update_state(state, user_msg, assistant_msg):
    """
    Update interview state with new conversation turn.
    
    Args:
        state (dict): Current interview state
        user_msg (str): User's message
        assistant_msg (str): Assistant's response
        
    Returns:
        dict: Updated state
    """
    # Append conversation turn
    state["history"].append({
        "user": user_msg,
        "assistant": assistant_msg
    })
    
    return state

