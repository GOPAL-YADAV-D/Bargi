import subprocess
import sounddevice as sd
import numpy as np
import os

# Resolve model path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
model_rel = "piper/en_US-lessac-medium.onnx"
model_path = os.path.normpath(os.path.join(project_root, model_rel))

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model not found: {model_path}")

DEFAULT_SR = 22050  # Piper raw output sample rate

print("Real-time Piper TTS (RAW PCM).")
print("Type text and hear speech immediately.")
print("Type 'exit' to quit.\n")

while True:
    text = input("You: ")
    if text.strip().lower() == "exit":
        break

    # Run Piper and request raw PCM output
    proc = subprocess.Popen(
        ["piper", "-m", model_path, "--output-raw", "--", text],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    raw = proc.stdout.read()

    if not raw:
        print("No audio returned. Error:")
        print(proc.stderr.read().decode())
        continue

    # Convert raw PCM (int16) to numpy array
    audio_np = np.frombuffer(raw, dtype=np.int16)

    # Play audio immediately
    sd.play(audio_np, DEFAULT_SR)
    sd.wait()
