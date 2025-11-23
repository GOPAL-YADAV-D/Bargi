# Base image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    ffmpeg \
    curl \
    wget \
    libasound2-dev \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# --- Whisper.cpp Setup ---
# Clone and build Whisper.cpp
RUN git clone https://github.com/ggerganov/whisper.cpp.git && \
    cd whisper.cpp && \
    make

# Download a base model for Whisper (ggml-base.en.bin)
RUN cd whisper.cpp/models && \
    ./download-ggml-model.sh base.en

# --- Piper TTS Setup ---
# Download Piper binary (Linux x86_64)
RUN wget -O piper.tar.gz https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_x86_64.tar.gz && \
    tar -xvf piper.tar.gz && \
    rm piper.tar.gz

# Download a voice model for Piper (en_US-lessac-medium)
RUN mkdir -p piper_voices && \
    wget -O piper_voices/en_US-lessac-medium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx && \
    wget -O piper_voices/en_US-lessac-medium.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json

# --- Python Setup ---
# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose Gradio port
EXPOSE 7860

# Run the application
CMD ["python", "src/main.py"]
