# Groq API wrapper
import os
from openai import OpenAI


class GroqClient:
    """
    Wrapper for Groq API using OpenAI-compatible interface.
    """
    
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
    
    def generate_response(self, messages, model="llama-3.1-70b-versatile"):
        """
        Generate a response using Groq API.
        
        Args:
            messages: List of message dictionaries
            model: Model identifier
            
        Returns:
            Generated response text
        """
        pass
