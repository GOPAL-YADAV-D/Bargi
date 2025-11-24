# Production-ready Dockerfile for AI Interview Agent
# Base: Python 3.10 slim for minimal size
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# =============================================
# SYSTEM DEPENDENCIES
# =============================================
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libsndfile1 \
    curl \
    wget \
    git \
    sox \
    && rm -rf /var/lib/apt/lists/*

# =============================================
# WHISPER.CPP SETUP
# =============================================
# Clone and build whisper.cpp
RUN git clone https://github.com/ggerganov/whisper.cpp.git /app/whisper.cpp && \
    cd /app/whisper.cpp && \
    make

# Download base.en model for Whisper
RUN cd /app/whisper.cpp/models && \
    curl -LO https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin

# =============================================
# PYTHON DEPENDENCIES
# =============================================
# Copy requirements file first (for layer caching)
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# =============================================
# PIPER TTS SETUP
# =============================================
# Install piper-tts
RUN pip install --no-cache-dir piper-tts

# Download Piper voice model
RUN python3 -m piper.download en_US-lessac-medium

# =============================================
# COPY PROJECT FILES
# =============================================
# Copy source code
COPY src/ /app/src/

# Copy role configuration files
COPY roles/ /app/roles/

# =============================================
# ENVIRONMENT VARIABLES
# =============================================
# Set default environment variable for Groq API key
# Override this with: docker run -e GROQ_API_KEY=your_key_here
ENV GROQ_API_KEY=""

# Set Python to unbuffered mode for better logging
ENV PYTHONUNBUFFERED=1

# =============================================
# EXPOSE PORT
# =============================================
# Gradio default port
EXPOSE 7860

# =============================================
# HEALTH CHECK
# =============================================
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# =============================================
# ENTRYPOINT
# =============================================
ENTRYPOINT ["python", "src/main.py"]
