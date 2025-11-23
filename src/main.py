# Gradio UI entrypoint
from dotenv import load_dotenv
load_dotenv()

import gradio as gr
import os
from router import handle_message
from state_manager import new_state
from stt_whisper import transcribe_audio

# Initialize interview state once
interview_state = new_state()

def process_turn(user_text, user_audio, history):
    """
    Handle a single conversation turn.
    """
    global interview_state
    
    # 1. Handle Audio Input (STT)
    if user_audio is not None:
        try:
            transcription = transcribe_audio(user_audio)
            if transcription:
                user_text = transcription
        except Exception as e:
            print(f"STT Error: {e}")
            pass
    
    if not user_text:
        return history, None

    # 2. Route message
    response_data = handle_message(user_text, interview_state)
    
    # 3. Update History in messages format for Gradio 6.0
    # Gradio 6.0 Chatbot expects messages format: [{"role": "user", "content": "..."}, ...]
    if history is None:
        history = []
    
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": response_data["reply_text"]})
    
    # 4. Return updated history and audio path (if any)
    return history, response_data["reply_audio"]

def main():
    """
    Main entrypoint for the interview practice agent.
    """
    with gr.Blocks(title="AI Interview Practice Agent") as demo:
        gr.Markdown("# 🤖 AI Interview Practice Agent")
        gr.Markdown("Practice your soft skills, technical knowledge, and behavioral answers.")
        
        chatbot = gr.Chatbot(height=500)
        
        with gr.Row():
            with gr.Column(scale=8):
                msg_input = gr.Textbox(
                    show_label=False, 
                    placeholder="Type your answer here...",
                    container=False
                )
            with gr.Column(scale=1):
                audio_input = gr.Audio(
                    sources=["microphone"], 
                    type="filepath",
                    show_label=False,
                    container=False
                )
        
        with gr.Row():
            submit_btn = gr.Button("Send", variant="primary")
            clear_btn = gr.Button("Clear Session")
            
        # Hidden audio output for TTS
        audio_output = gr.Audio(
            label="Assistant Voice", 
            autoplay=True, 
            visible=False
        )
        
        # Event handlers
        def user_chat(user_text, user_audio, history):
            # Process the turn and return updated history in messages format
            updated_history, audio_path = process_turn(user_text, user_audio, history or [])
            return "", None, updated_history, audio_path

        submit_btn.click(
            user_chat,
            inputs=[msg_input, audio_input, chatbot],
            outputs=[msg_input, audio_input, chatbot, audio_output]
        )
        
        msg_input.submit(
            user_chat,
            inputs=[msg_input, audio_input, chatbot],
            outputs=[msg_input, audio_input, chatbot, audio_output]
        )
        
        def clear_session():
            global interview_state
            interview_state = new_state()
            return [], None
            
        clear_btn.click(clear_session, outputs=[chatbot, audio_output])

    # Launch the app
    demo.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()
