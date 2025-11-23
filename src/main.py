# Gradio UI entrypoint
from dotenv import load_dotenv
load_dotenv()


import gradio as gr
from router import handle_message
from state_manager import new_state


# Initialize interview state once
interview_state = new_state()


def chat(message, history):
    """
    Handle chat messages from the user.
    
    Args:
        message: User's input message
        history: Chat history (list of message pairs)
        
    Returns:
        Response string
    """
    global interview_state
    
    # Route message through the router
    response = handle_message(message, interview_state)
    
    # Return text response (audio support to be added later)
    return response["reply_text"]


def main():
    """
    Main entrypoint for the interview practice agent.
    Launches the Gradio interface.
    """
    # Create chat interface with updated Gradio 5.x+ API
    interface = gr.ChatInterface(
        fn=chat,
        title="AI Interview Practice Agent",
        description="Practice your interview skills with an AI interviewer",
        # type="messages",  # Use structured message format
        examples=[
            "I'd like to practice for a software engineering interview",
            "Can we do a product manager interview?",
            "I want to practice sales interview"
        ]
    )
    
    # Launch the app on port 7860
    interface.launch(server_port=7860)


if __name__ == "__main__":
    main()
