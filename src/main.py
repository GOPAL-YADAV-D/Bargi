# Gradio UI entrypoint
from dotenv import load_dotenv
load_dotenv()

import gradio as gr
import os
from router import handle_message, handle_audio
from state_manager import new_state

# Initialize interview state once
interview_state = new_state()

def text_mode(user_text, history):
    """
    Handle text-based conversation turn.
    
    Args:
        user_text (str): User's typed message
        history (list): Chat history in messages format
        
    Returns:
        tuple: (updated_history, audio_output, score)
    """
    global interview_state
    
    if not user_text:
        return history, None, None
    
    # Route message through the router
    response_data = handle_message(user_text, interview_state)
    
    # Update history in messages format for Gradio 6.0
    if history is None:
        history = []
    
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": response_data["reply_text"]})
    
    # Return score for UI panel
    return history, response_data.get("reply_audio"), response_data.get("score")


def voice_mode(user_audio, history):
    """
    Handle voice-based conversation turn.
    
    Args:
        user_audio (str): Path to user's audio file
        history (list): Chat history in messages format
        
    Returns:
        tuple: (updated_history, audio_output_path, score)
    """
    global interview_state
    
    if not user_audio:
        return history, None, None
    
    # Route audio through the voice handler (STT + Router + TTS)
    response_data = handle_audio(user_audio, interview_state)
    
    # The response_data contains both transcribed user text (implicitly handled)
    # and the assistant's reply. We need to add both to history.
    
    # Note: handle_audio internally calls handle_message, which updates state.history
    # We can extract the last user message from the state
    if interview_state.get("history"):
        last_turn = interview_state["history"][-1]
        user_text = last_turn.get("user", "")
    else:
        user_text = "[Voice input]"
    
    # Update Gradio history
    if history is None:
        history = []
    
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": response_data["reply_text"]})
    
    # Return audio output and score for UI panel
    return history, response_data.get("reply_audio"), response_data.get("score")

def main():
    """
    Main entrypoint for the interview practice agent.
    """
    with gr.Blocks(title="AI Interview Practice Agent") as demo:
        # ============================================
        # HEADER SECTION
        # ============================================
        gr.Markdown("# 🎙️ AI Interview Practice Agent")
        gr.Markdown("**Powered by Groq LLM, Whisper.cpp (STT), Piper (TTS), LangChain Scoring**")
        
        # ============================================
        # MAIN CHAT INTERFACE (2-COLUMN LAYOUT)
        # ============================================
        with gr.Row():
            with gr.Column(scale=7):
                chatbot = gr.Chatbot(height=450, label="Interview Conversation")
            with gr.Column(scale=3):
                score_panel = gr.JSON(label="Latest Score", value=None)
        
        # ============================================
        # INPUT AREAS
        # ============================================
        
        # A) Text input row
        with gr.Row():
            text_input = gr.Textbox(
                label="Type your response...",
                placeholder="Enter your answer here and press Send",
                scale=4
            )
            text_button = gr.Button("Send", variant="primary", scale=1)
        
        # B) Voice input row
        with gr.Row():
            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="Speak your answer",
                scale=4
            )
            voice_button = gr.Button("Send Voice", variant="secondary", scale=1)
        
        # ============================================
        # OUTPUT
        # ============================================
        audio_output = gr.Audio(label="Assistant Voice Reply", autoplay=True)
        
        # ============================================
        # RESET BUTTON
        # ============================================
        reset_btn = gr.Button("🔄 Restart Interview", variant="stop", size="sm")
        
        # ============================================
        # FOOTER
        # ============================================
        gr.Markdown("### 💡 Tip: You can switch between typing and speaking anytime.")
        
        # ============================================
        # BACKEND HANDLERS
        # ============================================
        
        # Text mode handler
        def handle_text_submit(user_text, history):
            updated_history, audio_out, score = text_mode(user_text, history)
            return "", updated_history, audio_out, score
        
        text_button.click(
            handle_text_submit,
            inputs=[text_input, chatbot],
            outputs=[text_input, chatbot, audio_output, score_panel]
        )
        
        text_input.submit(
            handle_text_submit,
            inputs=[text_input, chatbot],
            outputs=[text_input, chatbot, audio_output, score_panel]
        )
        
        # Voice mode handler
        def handle_voice_submit(user_audio, history):
            updated_history, audio_out, score = voice_mode(user_audio, history)
            return None, updated_history, audio_out, score
        
        voice_button.click(
            handle_voice_submit,
            inputs=[audio_input, chatbot],
            outputs=[audio_input, chatbot, audio_output, score_panel]
        )
        
        # Reset session handler
        def reset_session():
            global interview_state
            interview_state = new_state()
            return [], None, None  # chatbot history, audio, scores
        
        reset_btn.click(
            fn=reset_session,
            outputs=[chatbot, audio_output, score_panel]
        )

    # Launch the app
    demo.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()
