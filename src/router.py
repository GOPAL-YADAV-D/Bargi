# Routing logic (text/voice, scoring)


def handle_message(message, state):
    """
    Handle incoming message and route to appropriate components.
    
    Args:
        message: User's text input from the UI
        state: Current interview state dictionary
        
    Returns:
        Dictionary with reply_text and reply_audio
        {
            "reply_text": str,
            "reply_audio": str or None
        }
    
    TODO:
    - Add Groq API call for conversation generation
    - Check if voice mode is enabled (route to TTS)
    - Detect interview completion and trigger scoring
    - Handle persona adaptation logic
    - Manage stage transitions
    """
    # Placeholder response
    # Future: Call Groq API here based on state and message
    # Future: If voice mode, generate audio via Piper TTS
    # Future: Update state via state_manager
    
    return {
        "reply_text": "Router placeholder response",
        "reply_audio": None
    }
