# Routing logic (text/voice, scoring)
from groq_client import groq_chat
from rag_loader import load_role_context
from scoring_langchain import score_answer
from state_manager import update_state
from final_summary import generate_final_summary
from stt_whisper import transcribe_audio
from tts_piper import synthesize_speech


def handle_message(message: str, state: dict) -> dict:
    """
    Handle incoming message and route to appropriate components.
    
    Args:
        message (str): User's text input
        state (dict): Current interview state
        
    Returns:
        dict: Response with reply_text and reply_audio
              {
                  "reply_text": str,
                  "reply_audio": None or str (path to audio file)
              }
    """
    
    # =========================================
    # A) ROLE SETUP PHASE
    # =========================================
    
    if state["stage"] == "setup":
        # Ask user to select a role
        state["stage"] = "await_role"
        return {
            "reply_text": "Welcome! Which role would you like to practice for? (engineer, product, sales)",
            "reply_audio": None,
            "score": None  # STAGE 15: Returning score for UI panel
        }
    
    if state["stage"] == "await_role":
        # Validate non-empty input
        if not message or not message.strip():
            return {
                "reply_text": "Please select a role: engineer, product, or sales.",
                "reply_audio": None,
                "score": None  # STAGE 15: Returning score for UI panel
            }
        
        # Extract role from user's message
        role_input = message.lower().strip()
        
        # Map user input to valid role names
        role_map = {
            "engineer": "engineer",
            "software engineer": "engineer",
            "product": "product",
            "product manager": "product",
            "sales": "sales",
            "sales representative": "sales"
        }
        
        role = role_map.get(role_input)
        
        if not role:
            # Invalid role selection - provide clear guidance
            return {
                "reply_text": "Please select engineer, product, or sales.",
                "reply_audio": None,
                "score": None  # STAGE 15: Returning score for UI panel
            }
        
        # Save role to state
        state["role"] = role
        
        # Load role context from knowledge base
        context = load_role_context(role)
        
        if not context:
            return {
                "reply_text": f"Sorry, I couldn't load the knowledge base for {role}. Please try again.",
                "reply_audio": None,
                "score": None  # STAGE 15: Returning score for UI panel
            }
        
        state["context"] = context
        state["scores"] = []  # Initialize scoring history
        state["question_index"] = 0  # Track which question we're on
        
        # Ask the first base question
        first_question = context.get("base_questions", ["Tell me about yourself."])[0]
        state["current_question"] = first_question
        state["stage"] = "interview"
        
        # Store this as the first interaction
        update_state(state, message, first_question)
        
        return {
            "reply_text": f"Great! Let's begin the {context.get('role', role)} interview.\n\n{first_question}",
            "reply_audio": None,
            "score": None  # STAGE 15: Returning score for UI panel
        }
    
    # =========================================
    # B) INTERVIEW PHASE
    # =========================================
    
    if state["stage"] == "interview":
        # Validate non-empty input
        if not message or not message.strip():
            return {
                "reply_text": "I didn't catch that. Please provide your answer.",
                "reply_audio": None,
                "score": None  # STAGE 15: Returning score for UI panel
            }
        
        # Check if this is a user answer (not the first turn)
        if state["current_question"]:
            # Score the user's answer to the previous question
            score_result = score_answer(
                question=state["current_question"],
                answer=message,
                role=state.get("role", "general")
            )
            
            # Store the answer and score
            state["answers"].append({
                "question": state["current_question"],
                "answer": message
            })
            state["scores"].append(score_result)
            
            # Update conversation history
            update_state(state, message, "")  # We'll fill assistant response below
        
        # Decide what to ask next based on followup_stage
        if state["followup_stage"]:
            # Generate a follow-up question using Groq
            role_name = state.get("context", {}).get("role", state.get("role", "general"))
            competencies = state.get("context", {}).get("competencies", [])
            competencies_str = ", ".join(competencies[:3])  # First 3 competencies
            
            system_prompt = (
                f"You are an expert AI interviewer for a {role_name} position. "
                f"Focus on these competencies: {competencies_str}. "
                "Based on the candidate's previous answer, ask ONE short, specific follow-up question "
                "to dig deeper. Keep it under 2 sentences."
            )
            
            # Build messages with recent context
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add the last answer for context
            if state["answers"]:
                last_qa = state["answers"][-1]
                messages.append({"role": "assistant", "content": last_qa["question"]})
                messages.append({"role": "user", "content": last_qa["answer"]})
            
            try:
                followup_question = groq_chat(messages)
            except Exception as e:
                followup_question = "Can you elaborate more on that?"
            
            # Update state
            state["current_question"] = followup_question
            state["followup_stage"] = False  # Next turn will be main question
            
            # Update history with the follow-up
            if state["history"]:
                state["history"][-1]["assistant"] = followup_question
            else:
                update_state(state, "", followup_question)
            
            # STAGE 15: Returning score for UI panel
            # Return the score from the answer we just evaluated
            score_to_return = None
            if state["scores"]:
                latest_score = state["scores"][-1]
                score_to_return = {
                    "communication": latest_score.get("communication", 0),
                    "technical": latest_score.get("technical", 0),
                    "behavioral": latest_score.get("behavioral", 0),
                    "structure": latest_score.get("structure", 0)
                }
            
            return {
                "reply_text": followup_question,
                "reply_audio": None,
                "score": score_to_return
            }
        
        else:
            # Ask next main question from base_questions
            idx = state["current_question_index"]
            base_questions = state.get("context", {}).get("base_questions", [])
            
            # Check if we've finished all questions
            if idx >= state["max_questions"] or idx >= len(base_questions):
                state["stage"] = "finished"
                
                # Generate comprehensive final summary using final_summary module
                # This aggregates scores, collects feedback, and uses Groq LLM
                # to create a detailed, personalized evaluation report
                summary = generate_final_summary(state)
                
                return {
                    "reply_text": summary,
                    "reply_audio": None,  # TODO (Stage 12): Add TTS for summary
                    "score": None  # STAGE 15: Returning score for UI panel
                }
            
            # Get the next main question
            next_main_question = base_questions[idx]
            
            # Update state
            state["current_question"] = next_main_question
            state["current_question_index"] += 1
            state["followup_stage"] = True  # Next turn will be follow-up
            
            # Update history
            if state["history"] and not state["history"][-1]["assistant"]:
                state["history"][-1]["assistant"] = next_main_question
            else:
                update_state(state, "", next_main_question)
            
            return {
                "reply_text": next_main_question,
                "reply_audio": None,
                "score": None  # STAGE 15: Returning score for UI panel (no scoring for questions)
            }
    
    # =========================================
    # C) INTERVIEW FINISHED
    # =========================================
    
    if state["stage"] == "finished":
        # Interview has already ended and summary was shown
        # User is still sending messages - remind them to restart
        return {
            "reply_text": "The interview has ended. Please click the '🔄 Restart Interview' button to begin a new session.",
            "reply_audio": None,
            "score": None  # STAGE 15: Returning score for UI panel
        }
    
    # =========================================
    # FALLBACK
    # =========================================
    
    return {
        "reply_text": "I'm not sure how to respond. Please restart the interview.",
        "reply_audio": None,
        "score": None  # STAGE 15: Returning score for UI panel
    }


# =========================================
# STAGE 12: VOICE MODE INTEGRATION
# =========================================

def handle_audio(audio_path: str, state: dict) -> dict:
    """
    Handle audio input from the user (full voice mode).
    
    This function:
    1. Transcribes audio to text using Whisper.cpp
    2. Routes the text through handle_message()
    3. Converts the reply text to speech using Piper TTS
    4. Returns both text and audio responses
    
    Args:
        audio_path (str): Path to the user's audio file
        state (dict): Current interview state
        
    Returns:
        dict: Response with reply_text and reply_audio
              {
                  "reply_text": str,
                  "reply_audio": str or None (path to audio file)
              }
    """
    
    # Step 1: Transcribe audio to text using Whisper STT
    try:
        user_text = transcribe_audio(audio_path)
        
        # Safe handling: check for empty or whitespace-only transcription
        if not user_text or not user_text.strip():
            return {
                "reply_text": "I couldn't hear you clearly. Please try speaking again or use text input.",
                "reply_audio": None,
                "score": None  # STAGE 15: Returning score for UI panel
            }
    except Exception as e:
        # Whisper STT failure - ask user to repeat or use text mode
        print(f"Whisper STT Error: {e}")
        return {
            "reply_text": "Speech recognition failed. Please try again or use text input instead.",
            "reply_audio": None,
            "score": None  # STAGE 15: Returning score for UI panel
        }
    
    # Step 2: Route the transcribed text through the normal message handler
    response = handle_message(user_text, state)
    reply_text = response["reply_text"]
    
    # Step 3: Convert the reply text to speech using Piper TTS
    try:
        audio_output_path = synthesize_speech(reply_text)
        
        # STAGE 15: Returning score for UI panel
        return {
            "reply_text": reply_text,
            "reply_audio": audio_output_path,
            "score": response.get("score")  # Pass through score from handle_message
        }
    except Exception as e:
        # Piper TTS failure - still return text reply without audio
        print(f"Piper TTS Error: {e}")
        print("Continuing with text-only response...")
        # STAGE 15: Returning score for UI panel
        return {
            "reply_text": reply_text,
            "reply_audio": None,  # Graceful degradation: text works, audio fails
            "score": response.get("score")  # Pass through score from handle_message
        }


# TODO: Add voice configuration options
# - Allow users to select different Piper voices
# - Add voice speed/pitch controls
# - Support multiple languages via Whisper models

# TODO: Optimize audio processing
# - Add background processing for TTS to reduce latency
# - Cache common responses to avoid re-synthesis
# - Compress audio files for faster delivery
