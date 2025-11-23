# Routing logic (text/voice, scoring)
from groq_client import groq_chat
from rag_loader import load_role_context
from scoring_langchain import score_answer
from state_manager import update_state


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
            "reply_audio": None
        }
    
    if state["stage"] == "await_role":
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
            # Invalid role selection
            return {
                "reply_text": "I didn't recognize that role. Please choose: engineer, product, or sales.",
                "reply_audio": None
            }
        
        # Save role to state
        state["role"] = role
        
        # Load role context from knowledge base
        context = load_role_context(role)
        
        if not context:
            return {
                "reply_text": f"Sorry, I couldn't load the knowledge base for {role}. Please try again.",
                "reply_audio": None
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
            "reply_audio": None
        }
    
    # =========================================
    # B) INTERVIEW PHASE
    # =========================================
    
    if state["stage"] == "interview":
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
            
            return {
                "reply_text": followup_question,
                "reply_audio": None
            }
        
        else:
            # Ask next main question from base_questions
            idx = state["current_question_index"]
            base_questions = state.get("context", {}).get("base_questions", [])
            
            # Check if we've finished all questions
            if idx >= state["max_questions"] or idx >= len(base_questions):
                state["stage"] = "finished"
                
                # TODO (Stage 11): Generate comprehensive final summary using LangChain
                # - Aggregate all scores from state["scores"]
                # - Compare answers against sample_good_answers and sample_bad_answers
                # - Provide detailed feedback and action items
                
                # Placeholder summary for now
                if state["scores"]:
                    avg_comm = sum(s.get("communication", 0) for s in state["scores"] if "error" not in s) / max(len(state["scores"]), 1)
                    avg_tech = sum(s.get("technical", 0) for s in state["scores"] if "error" not in s) / max(len(state["scores"]), 1)
                    avg_behav = sum(s.get("behavioral", 0) for s in state["scores"] if "error" not in s) / max(len(state["scores"]), 1)
                    avg_struct = sum(s.get("structure", 0) for s in state["scores"] if "error" not in s) / max(len(state["scores"]), 1)
                    
                    summary = (
                        f"🎉 Interview Complete!\n\n"
                        f"**Overall Scores:**\n"
                        f"- Communication: {avg_comm:.1f}/10\n"
                        f"- Technical: {avg_tech:.1f}/10\n"
                        f"- Behavioral: {avg_behav:.1f}/10\n"
                        f"- Structure: {avg_struct:.1f}/10\n\n"
                        f"Thank you for practicing with me! "
                        f"Detailed feedback will be available in Stage 11."
                    )
                else:
                    summary = "Interview complete! Thank you for your time."
                
                return {
                    "reply_text": summary,
                    "reply_audio": None
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
                "reply_audio": None
            }
    
    # =========================================
    # C) INTERVIEW FINISHED
    # =========================================
    
    if state["stage"] == "finished":
        return {
            "reply_text": "The interview has ended. Refresh the page to start a new session.",
            "reply_audio": None
        }
    
    # =========================================
    # FALLBACK
    # =========================================
    
    return {
        "reply_text": "I'm not sure how to respond. Please restart the interview.",
        "reply_audio": None
    }


# TODO: Add voice mode integration
# - Integrate Whisper.cpp for STT (transcribe_audio)
# - Integrate Piper for TTS (synthesize_speech)
# - Add audio_input parameter to handle_message
# - Return audio_path in reply_audio field

# TODO: Multi-round interview flow improvements
# - Add persona handling (confused, efficient, chatty candidates)
# - Add adaptive difficulty based on performance
# - Add time tracking per question

# TODO: Final summary enhancements
# - Use LangChain to generate detailed narrative feedback
# - Compare against sample_good_answers and sample_bad_answers
# - Provide specific action items for improvement
