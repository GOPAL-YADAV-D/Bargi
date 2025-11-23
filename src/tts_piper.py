import subprocess
import os
import shutil

def synthesize_speech(text, output_path, voice_path):
    """
    Synthesize speech from text using Piper TTS via command line.

    Args:
        text (str): Text to synthesize.
        output_path (str): Path to save the output WAV file.
        voice_path (str): Path to the voice model (.onnx).

    Returns:
        str: Path to the generated audio file.

    Raises:
        RuntimeError: If Piper is not installed or synthesis fails.
        FileNotFoundError: If model or output file is missing.
    """

    # Resolve model path:
    # If the user passed a relative path, make it relative to the project root.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    resolved_voice_path = os.path.normpath(os.path.join(project_root, voice_path))

    if not os.path.exists(resolved_voice_path):
        raise FileNotFoundError(
            f"Voice model not found: {resolved_voice_path}"
        )

    # Check if python3 is available
    if not shutil.which("python3"):
        raise RuntimeError("python3 is not found in PATH.")

    # Build the Piper command:
    # python3 -m piper -m <voice> -f <output> -- <text>
    cmd = [
        "python3", "-m", "piper",
        "-m", resolved_voice_path,
        "-f", output_path,
        "--",
        text
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        if not os.path.exists(output_path):
            raise FileNotFoundError(
                f"Piper finished but output file not found at: {output_path}"
            )

        return output_path

    except subprocess.CalledProcessError as e:
        if "No module named piper" in e.stderr:
            raise RuntimeError(
                "Piper is not installed. Install it with: pip install piper-tts"
            )

        raise RuntimeError(
            f"Piper TTS failed with exit code {e.returncode}.\nStderr:\n{e.stderr}"
        )

    except Exception as e:
        raise RuntimeError(f"Unexpected TTS error: {str(e)}")
