# AI Interview Practice Agent

A comprehensive AI-powered interview preparation system that helps candidates practice and improve their interview skills through interactive conversations with real-time scoring and feedback.

## Overview

This application provides an intelligent interview practice platform that simulates realistic interview scenarios for three key roles: Software Engineer, Product Manager, and Sales Representative. The system conducts multi-round interviews with adaptive follow-up questions, provides detailed scoring on each response, and generates comprehensive performance summaries.

## Key Features

### Multi-Modal Interaction
- **Text Mode**: Type responses directly into the chat interface
- **Voice Mode**: Speak your answers using the microphone for a more realistic interview experience
- **Seamless Switching**: Move between text and voice modes at any point during the interview

### Intelligent Interview Flow
- **Role-Based Questions**: Tailored questions for Software Engineer, Product Manager, and Sales roles
- **Adaptive Follow-ups**: AI-generated follow-up questions based on your responses
- **Multi-Round Structure**: 5 main questions with follow-ups to thoroughly evaluate competencies

### Real-Time Scoring
- **Four Evaluation Dimensions**: Communication, Technical Knowledge, Behavioral Competence, and Response Structure
- **Live Feedback**: Scores displayed immediately after each answer (0-10 scale)
- **Detailed Analysis**: Strengths and areas for improvement identified for each response

### Comprehensive Feedback
- **Final Summary**: Complete performance report at the end of the interview
- **Aggregated Scores**: Average scores across all evaluation dimensions
- **Actionable Insights**: Specific recommendations for improvement

## Technology Stack

### Core Components
- **UI Framework**: Gradio 6.0 - Modern web interface with real-time updates
- **LLM Backend**: Groq API (llama3-70b-8192) - Fast, high-quality language model
- **Scoring Engine**: LangChain + Groq - Structured JSON output for consistent evaluation
- **Speech-to-Text**: Whisper.cpp (base.en model) - Accurate, local STT processing
- **Text-to-Speech**: Piper TTS (en_US-lessac-medium) - Natural-sounding voice synthesis

### Architecture
- **State Management**: In-memory session state with full conversation history
- **Knowledge Base**: JSON-based role configurations with questions and competencies
- **Processing Pipeline**: STT → Router → Scoring → TTS for voice mode

## Installation

### Prerequisites
- Python 3.10 or higher
- Groq API key (free tier available at https://console.groq.com)
- Git
- Build tools (gcc, make) for Whisper.cpp compilation

### Step 1: Clone the Repository
```bash
git clone https://github.com/GOPAL-YADAV-D/Bargi.git
cd Bargi
```

### Step 2: Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows

# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
```bash
# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

### Step 4: Build Whisper.cpp
```bash
# Navigate to whisper directory
cd whisper

# Build the project
make

# Download the base.en model
cd models
bash download-ggml-model.sh base.en

# Return to project root
cd ../..
```

### Step 5: Install Piper TTS
```bash
# Install Piper
pip install piper-tts

# Download voice model
python3 -m piper.download en_US-lessac-medium
```

## Usage

### Running the Application

#### Local Development
```bash
# Ensure you're in the project root
cd /path/to/Bargi

# Activate virtual environment
source .venv/bin/activate

# Run the application
python src/main.py
```

The application will start and display:
```
Running on local URL:  http://127.0.0.1:7860
```

Open your browser and navigate to the URL to access the interview agent.

#### Docker Deployment
```bash
# Build the Docker image
docker build -t interview-agent:latest .

# Run the container
docker run -d \
  -p 7860:7860 \
  -e GROQ_API_KEY=your_groq_api_key_here \
  --name interview-agent \
  interview-agent:latest

# View logs
docker logs -f interview-agent

# Stop the container
docker stop interview-agent

# Remove the container
docker rm interview-agent
```

### Interview Workflow

1. **Start Interview**: Launch the application and open the web interface
2. **Select Role**: Choose from Engineer, Product Manager, or Sales Representative
3. **Answer Questions**: Respond to interview questions via text or voice
4. **Review Scores**: View real-time scoring in the side panel after each answer
5. **Receive Feedback**: Get detailed follow-up questions based on your responses
6. **Complete Interview**: After 5 main questions, receive a comprehensive summary
7. **Restart**: Click the "Restart Interview" button to practice again with a fresh session

### Using Text Mode
1. Type your response in the text input field
2. Click "Send" or press Enter
3. View the assistant's response and your score in the UI

### Using Voice Mode
1. Click the microphone icon to start recording
2. Speak your answer clearly
3. Click "Send Voice" to submit
4. The system will transcribe your speech, process it, and respond with both text and audio

## Project Structure

```
Bargi/
├── src/
│   ├── main.py                 # Gradio UI and application entry point
│   ├── router.py               # Core routing logic for interview flow
│   ├── groq_client.py          # Groq API wrapper for LLM interactions
│   ├── rag_loader.py           # Load role-based knowledge from JSON files
│   ├── scoring_langchain.py    # LangChain-based scoring engine
│   ├── state_manager.py        # Session state management
│   ├── stt_whisper.py          # Speech-to-text using Whisper.cpp
│   ├── tts_piper.py            # Text-to-speech using Piper
│   ├── final_summary.py        # Generate comprehensive interview summaries
│   └── utils.py                # Utility functions
├── roles/
│   ├── engineer.json           # Software Engineer interview configuration
│   ├── product.json            # Product Manager interview configuration
│   └── sales.json              # Sales Representative interview configuration
├── whisper/                    # Whisper.cpp submodule (cloned during setup)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker containerization configuration
├── .env                        # Environment variables (create this file)
├── .dockerignore              # Docker build exclusions
├── TESTING_GUIDE.md           # Comprehensive testing documentation
└── README.md                  # This file
```

## Configuration

### Role Configuration Files

Each role (engineer.json, product.json, sales.json) contains:
- **base_questions**: Core interview questions for the role
- **competencies**: Key skills and attributes evaluated
- **sample_good_answers**: Examples of strong responses
- **sample_bad_answers**: Examples of weak responses

You can customize these files to add new questions or modify evaluation criteria.

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)
- `PYTHONUNBUFFERED`: Set to 1 for real-time logging in Docker

## API Keys

### Groq API
1. Visit https://console.groq.com
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to your `.env` file

## Performance

### Expected Response Times
- **LLM Response**: 1-3 seconds
- **Scoring**: 2-5 seconds
- **STT (Whisper)**: 1-2 seconds per 10 seconds of audio
- **TTS (Piper)**: < 1 second for typical responses

### Resource Requirements
- **Memory**: ~500MB base, ~1GB during active use
- **CPU**: 2+ cores recommended
- **Disk**: ~3GB (includes models and dependencies)
- **Network**: Stable internet connection for Groq API

## Troubleshooting

### Application Won't Start
- Verify Python version: `python --version` (should be 3.10+)
- Check all dependencies are installed: `pip list`
- Ensure `.env` file exists with valid GROQ_API_KEY
- Check if port 7860 is available: `lsof -i :7860`

### Whisper.cpp Errors
- Ensure Whisper is built: `ls whisper/build/bin/whisper-cli`
- Verify model exists: `ls whisper/models/ggml-base.en.bin`
- Rebuild if necessary: `cd whisper && make clean && make`

### Piper TTS Not Working
- Check Piper installation: `python3 -c "import piper; print('OK')"`
- Verify voice model: `ls ~/.local/share/piper/voices/`
- Reinstall if needed: `pip install --force-reinstall piper-tts`

### Groq API Errors
- Verify API key is set: `echo $GROQ_API_KEY`
- Check API key validity at https://console.groq.com
- Review API rate limits and quotas

### Score Panel Shows Null
- This is normal during setup and when asking questions
- Scores only appear after answering interview questions
- Ensure the interview has progressed past role selection

## Development

### Running Tests
Refer to `TESTING_GUIDE.md` for comprehensive testing instructions covering:
- Component unit tests
- Integration tests
- UI testing procedures
- Docker validation
- Performance benchmarks

### Adding New Roles
1. Create a new JSON file in `roles/` directory
2. Follow the structure of existing role files
3. Update `rag_loader.py` role_map with the new role
4. Update `router.py` role selection prompt

### Extending Functionality
- **Custom Scoring Criteria**: Modify `scoring_langchain.py` JSON schema
- **Additional Questions**: Edit role JSON files
- **Different Models**: Change model parameters in `groq_client.py`
- **UI Customization**: Modify `main.py` Gradio components

## Security Considerations

- API keys are never logged or exposed in the UI
- User inputs are sanitized before processing
- No persistent storage of interview data (privacy by design)
- Docker containers run with minimal privileges
- Rate limiting recommended for production deployments

## Limitations

- **Stateful Architecture**: Current implementation uses in-memory state (single-user sessions)
- **Voice Quality**: STT accuracy depends on microphone quality and background noise
- **API Dependency**: Requires active internet connection for Groq API
- **Language Support**: Currently English-only (Whisper base.en model)

## Future Enhancements

- Session persistence with database integration
- User authentication and progress tracking
- Multi-language support
- Advanced RAG with vector embeddings (FAISS/ChromaDB)
- Interview persona variations (confused, chatty, efficient)
- Performance analytics dashboard
- Mobile-responsive UI improvements

## License

This project is open-source and available under the MIT License.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your fork
5. Submit a pull request

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Review the TESTING_GUIDE.md for troubleshooting
- Check existing issues for similar problems

## Acknowledgments

- Groq for providing fast, high-quality LLM inference
- Whisper.cpp team for efficient STT implementation
- Piper TTS for natural voice synthesis
- LangChain for structured LLM output
- Gradio for the intuitive UI framework

## Version History

- **v1.0.0** (November 2025)
  - Initial release
  - Multi-modal interview system (text + voice)
  - Real-time scoring and feedback
  - Three role configurations
  - Docker support
  - Comprehensive testing suite
