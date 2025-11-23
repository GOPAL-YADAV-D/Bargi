# Gradio UI entrypoint
import gradio as gr
from dotenv import load_dotenv
from router import handle_message
from state_manager import new_state

load_dotenv()

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
    # Create chat interface
    interface = gr.ChatInterface(
        fn=chat,
        title="AI Interview Practice Agent",
        description="Practice your interview skills with an AI interviewer"
    )
    
    # Launch the app
    interface.launch(server_port=7860)


if __name__ == "__main__":
    main()
