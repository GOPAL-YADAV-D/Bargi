# Routing logic (text/voice, scoring)


class InterviewRouter:
    """
    Routes user input to appropriate handlers based on mode (text/voice).
    Manages scoring triggers and interview flow.
    """
    
    def __init__(self):
        pass
    
    def route_input(self, input_data, mode="text"):
        """
        Route input to the appropriate handler.
        
        Args:
            input_data: User input (text or audio)
            mode: "text" or "voice"
        """
        pass
    
    def trigger_scoring(self, session_data):
        """
        Trigger scoring based on interview completion.
        
        Args:
            session_data: Complete interview session data
        """
        pass
