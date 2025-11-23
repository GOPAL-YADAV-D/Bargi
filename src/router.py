# Routing logic (text/voice, scoring)
from groq_client import groq_chat
from state_manager import update_state


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
    - Add STT integration for voice input (Whisper.cpp)
    - Add TTS integration for voice output (Piper TTS)
    - Add scoring integration when interview is complete (LangChain)
    - Implement multi-stage interview logic (setup -> intro -> technical -> behavioral -> scoring)
    - Add persona adaptation based on user behavior
    - Implement role-specific system prompts from roles/*.json
    """
    
    # Build messages list in OpenAI/Groq format
    # TODO: Load system prompt from role configuration based on state["role"] and state["stage"]
    # TODO: Include conversation history from state["history"] for context
    messages = [
        {
            "role": "system",
            "content": "You are an AI interview assistant. Keep responses short for now."
        },
        {
            "role": "user",
            "content": message
        }
    ]
    
    try:
        # Call Groq API to get assistant reply
        assistant_reply = groq_chat(messages)
        
        # Update state with this conversation turn
        # TODO: Check if this answer should be stored for scoring
        # TODO: Detect stage transitions and update state["stage"]
        update_state(state, message, assistant_reply)
        
        # Return response
        # TODO: If voice mode enabled, generate audio via Piper TTS
        # TODO: Check if interview is complete and trigger scoring
        return {
            "reply_text": assistant_reply,
            "reply_audio": None  # Will be populated when TTS is integrated
        }
        
    except Exception as e:
        # Handle errors gracefully
        error_message = f"Sorry, I encountered an error: {str(e)}"
        return {
            "reply_text": error_message,
            "reply_audio": None
        }
