import subprocess
import os

def transcribe_audio(audio_path, model_path="whisper/models/ggml-base.en.bin"):
    """
    Transcribe audio file to text using Whisper.cpp.

    This module is used by the router for STT.
    Whisper.cpp must be installed manually (or via Docker).
    UI integration will come later (Stage 6).

    Args:
        audio_path (str): Path to the WAV audio file.
        model_path (str): Path to the Whisper model binary.

    Returns:
        str: Transcribed text.

    Raises:
        FileNotFoundError: If audio file or whisper binary is missing.
        RuntimeError: If transcription fails.
    """
    # Check if audio file exists
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # Determine path to whisper binary
    # Assuming running from project root, binary is at whisper/main
    # If running from src/, we might need to adjust, but we'll stick to the prompt's implication
    # or try to find it.
    
    # The prompt explicitly asked to use: whisper/main
    whisper_binary = "whisper/build/bin/whisper-cli"
    
    # Check if binary exists (relative to current working directory)
    if not os.path.exists(whisper_binary):
        # Try looking in absolute path if we are in src/
        # But for now, let's stick to the prompt's requested command structure
        # and just raise error if not found.
        if os.path.exists(os.path.join("..", whisper_binary)):
             whisper_binary = os.path.join("..", whisper_binary)
        else:
             raise FileNotFoundError(f"Whisper binary not found at: {whisper_binary}. Please build whisper.cpp.")

    # Check if model exists
    if not os.path.exists(model_path):
         # Try adjusting for src/ execution context
         if os.path.exists(os.path.join("..", model_path)):
             model_path = os.path.join("..", model_path)
         else:
             raise FileNotFoundError(f"Whisper model not found at: {model_path}")

    # Construct command
    # whisper/main -m <model_path> -f <audio_path> --print-special --no-timestamps
    cmd = [
        whisper_binary,
        "-m", model_path,
        "-f", audio_path,
        "--print-special",
        "--no-timestamps"
    ]

    try:
        # Run subprocess
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=True
        )
        
        # Return stdout as the transcription
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        error_msg = f"Transcription failed with exit code {e.returncode}. Stderr: {e.stderr}"
        raise RuntimeError(error_msg)
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during transcription: {str(e)}")

