# Multi-stage interview logic


def new_state():
    """
    Initialize a new interview state.
    
    Returns:
        Dictionary representing initial interview state
        {
            "stage": Current stage (setup, intro, technical, behavioral, etc.)
            "role": Selected role (engineer, product, sales, or None)
            "history": List of conversation turns
            "answers": List of user answers for scoring
        }
    """
    return {
        "stage": "setup",
        "role": None,
        "history": [],
        "answers": []
    }


def update_state(state, user_msg, assistant_msg):
    """
    Update interview state with new conversation turn.
    
    Args:
        state: Current state dictionary
        user_msg: User's message
        assistant_msg: Assistant's response
        
    Returns:
        Updated state dictionary
    
    TODO:
    - Add stage transition logic
    - Track question-answer pairs for scoring
    - Detect completion conditions
    - Handle role-specific state updates
    """
    # Append conversation turn to history
    state["history"].append({
        "user": user_msg,
        "assistant": assistant_msg
    })
    
    # TODO: Add logic to transition between stages
    # TODO: Extract and store answers for final scoring
    # TODO: Check if interview should move to next stage
    
    return state
