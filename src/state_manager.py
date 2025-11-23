# Multi-stage interview logic


class InterviewStateManager:
    """
    Manages multi-stage interview flow and state transitions.
    Tracks current stage, questions asked, and user responses.
    """
    
    def __init__(self, role_config):
        self.role_config = role_config
        self.current_stage = 0
        self.history = []
    
    def next_stage(self):
        """Move to the next interview stage."""
        pass
    
    def add_interaction(self, question, answer):
        """
        Record an interview interaction.
        
        Args:
            question: Question asked
            answer: User's answer
        """
        pass
    
    def is_complete(self):
        """Check if the interview is complete."""
        pass
    
    def get_session_data(self):
        """Get complete session data for scoring."""
        pass
