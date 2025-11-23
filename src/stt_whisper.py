# Whisper.cpp integration


class WhisperSTT:
    """
    Speech-to-text using Whisper.cpp.
    """
    
    def __init__(self, model_path=None):
        self.model_path = model_path
    
    def transcribe(self, audio_file):
        """
        Transcribe audio to text.
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            Transcribed text
        """
        pass
