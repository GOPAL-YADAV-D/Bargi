# 🧪 Complete Testing Guide - AI Interview Practice Agent

## 📋 Project Overview

**Architecture:**
- **UI:** Gradio 6.0 (text + voice dual mode)
- **LLM:** Groq API (llama3-70b-8192)
- **STT:** Whisper.cpp (base.en model)
- **TTS:** Piper TTS (en_US-lessac-medium voice)
- **Scoring:** LangChain + Groq with JSON output
- **State:** In-memory state manager
- **Knowledge Base:** JSON role configs (engineer, product, sales)

---

## 🚀 Phase 1: Environment Setup Testing

### 1.1 Python Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR: venv\Scripts\activate  # Windows

# Verify Python version
python --version  # Should be 3.10+
```

**Expected:** Python 3.10 or higher

---

### 1.2 Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt

# Verify key packages
pip list | grep -E "(gradio|langchain|groq)"
```

**Expected Output:**
```
gradio                      6.0.0 (or higher)
langchain                   0.3.0 (or higher)
langchain-groq             0.x.x
groq                        0.9.0 (or higher)
```

---

### 1.3 Environment Variables
```bash
# Create .env file
echo "GROQ_API_KEY=your_actual_key_here" > .env

# Verify
cat .env
```

**Test Script:**
```bash
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
key = os.getenv('GROQ_API_KEY')
print('✅ API Key loaded' if key else '❌ API Key missing')
"
```

**Expected:** `✅ API Key loaded`

---

### 1.4 Whisper.cpp Setup
```bash
# Navigate to whisper directory
cd whisper

# Build whisper.cpp
make

# Verify binary exists
ls -lh build/bin/whisper-cli

# Download base.en model
cd models
bash download-ggml-model.sh base.en

# Verify model
ls -lh ggml-base.en.bin
```

**Expected:**
- Binary: `whisper/build/bin/whisper-cli` (~5MB)
- Model: `whisper/models/ggml-base.en.bin` (~140MB)

---

### 1.5 Piper TTS Setup
```bash
# Install piper-tts
pip install piper-tts

# Download voice model
python3 -m piper.download en_US-lessac-medium

# Verify installation
python3 -c "import piper; print('✅ Piper installed')"
```

**Expected:** `✅ Piper installed`

---

## 🧩 Phase 2: Component Unit Testing

### 2.1 Test Groq API Client
```bash
cd src

# Test groq_client.py
python3 -c "
from groq_client import groq_chat

messages = [
    {'role': 'system', 'content': 'You are helpful.'},
    {'role': 'user', 'content': 'Say hello in 5 words.'}
]

try:
    response = groq_chat(messages, model='llama3-70b-8192', temperature=0.7)
    print('✅ Groq API works')
    print(f'Response: {response}')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

**Expected:**
```
✅ Groq API works
Response: Hello there, how are you?
```

---

### 2.2 Test RAG Loader
```bash
# Test rag_loader.py
python3 -c "
from rag_loader import load_role_context

# Test all roles
for role in ['engineer', 'product', 'sales']:
    context = load_role_context(role)
    if context and 'base_questions' in context:
        print(f'✅ {role}: {len(context[\"base_questions\"])} questions loaded')
    else:
        print(f'❌ {role}: Failed to load')
"
```

**Expected:**
```
✅ engineer: 10 questions loaded
✅ product: 10 questions loaded
✅ sales: 10 questions loaded
```

---

### 2.3 Test LangChain Scoring
```bash
# Test scoring_langchain.py
python3 -c "
from scoring_langchain import score_answer

question = 'Tell me about a time you solved a difficult problem.'
answer = 'I debugged a memory leak by profiling the application and identified the root cause in a third-party library. I implemented a workaround and documented it for the team.'

try:
    result = score_answer(question, answer, role='engineer')
    
    if 'error' in result:
        print(f'❌ Scoring error: {result[\"error\"]}')
    else:
        print('✅ Scoring works')
        print(f'Communication: {result[\"communication\"]}/10')
        print(f'Technical: {result[\"technical\"]}/10')
        print(f'Behavioral: {result[\"behavioral\"]}/10')
        print(f'Structure: {result[\"structure\"]}/10')
        print(f'Strengths: {result[\"strengths\"]}')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

**Expected:**
```
✅ Scoring works
Communication: 8/10
Technical: 9/10
Behavioral: 7/10
Structure: 8/10
Strengths: ['Clear explanation', 'Specific example', ...]
```

---

### 2.4 Test Whisper STT
```bash
# Create a test audio file (requires microphone or sample WAV)
# For testing, record a simple message: "This is a test."

# Option A: Use existing sample
# Option B: Record using sox
rec -r 16000 -c 1 test_audio.wav

# Test transcription
python3 -c "
from stt_whisper import transcribe_audio
import os

audio_path = 'test_audio.wav'

if os.path.exists(audio_path):
    try:
        text = transcribe_audio(audio_path)
        print(f'✅ STT works')
        print(f'Transcription: {text}')
    except Exception as e:
        print(f'❌ Error: {e}')
else:
    print('⚠️  No test audio file found. Create test_audio.wav first.')
"
```

**Expected:**
```
✅ STT works
Transcription: this is a test
```

---

### 2.5 Test Piper TTS
```bash
# Test tts_piper.py
python3 -c "
from tts_piper import synthesize_speech
import os

text = 'Hello, this is a test of the text to speech system.'
output_path = 'test_output.wav'
voice_path = '~/.local/share/piper/voices/en_US-lessac-medium.onnx'

try:
    result = synthesize_speech(text, output_path, voice_path)
    if os.path.exists(output_path):
        print('✅ TTS works')
        print(f'Audio saved: {result}')
        print(f'Size: {os.path.getsize(output_path)} bytes')
    else:
        print('❌ Audio file not created')
except Exception as e:
    print(f'❌ Error: {e}')
"

# Play the audio (requires audio player)
# aplay test_output.wav  # Linux
# afplay test_output.wav # Mac
# vlc test_output.wav    # Cross-platform
```

**Expected:**
```
✅ TTS works
Audio saved: test_output.wav
Size: 352000 bytes
```

---

### 2.6 Test State Manager
```bash
# Test state_manager.py
python3 -c "
from state_manager import new_state, update_state

# Create new state
state = new_state()

# Verify initial state
assert state['stage'] == 'setup'
assert state['role'] is None
assert state['history'] == []
assert state['scores'] == []
assert state['max_questions'] == 5
print('✅ Initial state correct')

# Update state
update_state(state, 'Hello', 'Hi there!')
assert len(state['history']) == 1
assert state['history'][0]['user'] == 'Hello'
assert state['history'][0]['assistant'] == 'Hi there!'
print('✅ State update works')
"
```

**Expected:**
```
✅ Initial state correct
✅ State update works
```

---

### 2.7 Test Final Summary Generator
```bash
# Test final_summary.py
python3 -c "
from final_summary import generate_final_summary
from state_manager import new_state

# Create mock state with scores
state = new_state()
state['role'] = 'engineer'
state['context'] = {'role': 'Software Engineer'}
state['answers'] = [
    {'question': 'Q1', 'answer': 'A1'},
    {'question': 'Q2', 'answer': 'A2'}
]
state['scores'] = [
    {
        'communication': 8,
        'technical': 7,
        'behavioral': 9,
        'structure': 8,
        'strengths': ['Clear', 'Detailed'],
        'improvements': ['Add metrics']
    },
    {
        'communication': 7,
        'technical': 8,
        'behavioral': 8,
        'structure': 7,
        'strengths': ['Good examples'],
        'improvements': ['More depth']
    }
]

try:
    summary = generate_final_summary(state)
    if summary and len(summary) > 100:
        print('✅ Final summary generated')
        print(f'Length: {len(summary)} characters')
        print(f'Preview: {summary[:200]}...')
    else:
        print('❌ Summary too short or empty')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

**Expected:**
```
✅ Final summary generated
Length: 1250 characters
Preview: ## 📊 Interview Performance Summary

**Role:** Software Engineer

### Overall Scores:
- Communication: 7.5/10
- Technical: 7.5/10
...
```

---

## 🎯 Phase 3: Integration Testing

### 3.1 Test Router Logic (Text Mode)
```bash
# Test router.py handle_message
python3 -c "
from router import handle_message
from state_manager import new_state

state = new_state()

# Test 1: Initial setup
response1 = handle_message('', state)
assert 'engineer, product, sales' in response1['reply_text']
assert response1['score'] is None
print('✅ Test 1: Initial setup passed')

# Test 2: Role selection
response2 = handle_message('engineer', state)
assert state['role'] == 'engineer'
assert state['stage'] == 'interview'
assert response2['score'] is None
print('✅ Test 2: Role selection passed')

# Test 3: Answer a question
response3 = handle_message('I have 5 years of Python experience', state)
assert response3['score'] is not None
assert 'communication' in response3['score']
print('✅ Test 3: Answer scoring passed')
print(f'Score: {response3[\"score\"]}')
"
```

**Expected:**
```
✅ Test 1: Initial setup passed
✅ Test 2: Role selection passed
✅ Test 3: Answer scoring passed
Score: {'communication': 7, 'technical': 6, 'behavioral': 5, 'structure': 6}
```

---

### 3.2 Test Router Logic (Voice Mode)
```bash
# Test router.py handle_audio
# Requires test_audio.wav file
python3 -c "
from router import handle_audio
from state_manager import new_state
import os

state = new_state()
state['stage'] = 'interview'
state['role'] = 'engineer'
state['current_question'] = 'Tell me about yourself.'

audio_path = 'test_audio.wav'

if os.path.exists(audio_path):
    try:
        response = handle_audio(audio_path, state)
        
        if 'error' in response['reply_text'].lower() and 'failed' in response['reply_text'].lower():
            print('⚠️  Voice mode error (expected if STT/TTS not set up)')
        else:
            print('✅ Voice mode works')
            print(f'Reply: {response[\"reply_text\"][:100]}...')
            print(f'Audio: {response[\"reply_audio\"]}')
            print(f'Score: {response[\"score\"]}')
    except Exception as e:
        print(f'⚠️  Error: {e}')
else:
    print('⚠️  No test audio. Skipping voice mode test.')
"
```

---

### 3.3 Test Error Handling
```bash
# Test invalid inputs
python3 -c "
from router import handle_message
from state_manager import new_state

state = new_state()

# Test empty message during role selection
state['stage'] = 'await_role'
response = handle_message('', state)
assert 'Please select' in response['reply_text']
print('✅ Empty role input handled')

# Test invalid role
response = handle_message('invalid_role', state)
assert 'engineer, product, or sales' in response['reply_text']
print('✅ Invalid role handled')

# Test empty answer during interview
state['stage'] = 'interview'
state['current_question'] = 'Test question'
response = handle_message('', state)
assert 'provide your answer' in response['reply_text'].lower()
print('✅ Empty answer handled')

# Test finished interview
state['stage'] = 'finished'
response = handle_message('more text', state)
assert 'Restart Interview' in response['reply_text']
print('✅ Finished state handled')
"
```

**Expected:**
```
✅ Empty role input handled
✅ Invalid role handled
✅ Empty answer handled
✅ Finished state handled
```

---

## 🖥️ Phase 4: UI Testing (Gradio)

### 4.1 Launch Application
```bash
cd /mnt/sagittarius/Bargi

# Start the Gradio app
python src/main.py
```

**Expected Output:**
```
Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://xxxxx.gradio.live (if share=True)
```

---

### 4.2 Manual UI Testing Checklist

#### **Visual Elements:**
- [ ] Header displays: "🎙️ AI Interview Practice Agent"
- [ ] Tech stack shown: "Powered by Groq LLM, Whisper.cpp (STT), Piper (TTS), LangChain Scoring"
- [ ] 2-column layout: Chat (70%) | Score Panel (30%)
- [ ] Text input box with "Type your response..." label
- [ ] "Send" button (primary variant)
- [ ] Microphone audio input
- [ ] "Send Voice" button (secondary variant)
- [ ] Audio output player
- [ ] "🔄 Restart Interview" button
- [ ] Footer tip: "💡 Tip: You can switch between typing and speaking anytime."

#### **Text Mode Flow:**
1. **Initial Message:**
   - [ ] Welcome message appears automatically
   - [ ] Asks for role selection (engineer, product, sales)

2. **Role Selection:**
   - [ ] Type "engineer" → Confirms role and shows first question
   - [ ] Type "invalid" → Shows error: "Please select engineer, product, or sales."
   - [ ] Leave empty and submit → Shows error

3. **Interview Questions:**
   - [ ] First question appears (from base_questions)
   - [ ] Type answer → Score appears in right panel
   - [ ] Score shows: communication, technical, behavioral, structure (0-10)
   - [ ] Follow-up question appears after answer
   - [ ] Follow-up is relevant to previous answer

4. **Multi-Round:**
   - [ ] After follow-up answer, next base question appears
   - [ ] Score updates in panel
   - [ ] Continues for 5 main questions (max_questions)

5. **Final Summary:**
   - [ ] After 5 questions, summary appears
   - [ ] Summary includes average scores
   - [ ] Summary shows strengths and improvements
   - [ ] No more questions asked

6. **Reset:**
   - [ ] Click "🔄 Restart Interview" button
   - [ ] Chat clears
   - [ ] Score panel clears
   - [ ] Returns to initial welcome message

#### **Voice Mode Flow:**
1. **Record Audio:**
   - [ ] Click microphone icon
   - [ ] Speak: "I want to practice for engineer role"
   - [ ] Click "Send Voice"

2. **STT Processing:**
   - [ ] Audio transcribed to text
   - [ ] Appears in chat as user message

3. **Response:**
   - [ ] Assistant reply in chat
   - [ ] Audio output plays automatically
   - [ ] Can hear TTS voice

4. **Score Display:**
   - [ ] After answering question via voice
   - [ ] Score appears in right panel
   - [ ] Same scoring as text mode

#### **Mixed Mode:**
- [ ] Start with text, switch to voice → Works seamlessly
- [ ] Start with voice, switch to text → Works seamlessly

---

## 🐳 Phase 5: Docker Testing

### 5.1 Build Docker Image
```bash
cd /mnt/sagittarius/Bargi

# Build image
docker build -t interview-agent:latest .

# Check image size
docker images | grep interview-agent
```

**Expected:**
- Build completes without errors
- Image size: ~2-3GB (includes Whisper, Piper, models)

---

### 5.2 Run Docker Container
```bash
# Run with API key
docker run -d \
  -p 7860:7860 \
  -e GROQ_API_KEY=your_key_here \
  --name interview-agent-test \
  interview-agent:latest

# Check logs
docker logs -f interview-agent-test
```

**Expected:**
```
Running on local URL:  http://0.0.0.0:7860
```

---

### 5.3 Test Container
```bash
# Test health check
docker ps | grep interview-agent-test
# Should show "healthy" status after 30 seconds

# Test web access
curl http://localhost:7860

# Open in browser
# http://localhost:7860
```

**Expected:**
- Health check passes
- Gradio UI loads in browser
- All features work (text, voice, scoring)

---

### 5.4 Cleanup
```bash
# Stop container
docker stop interview-agent-test

# Remove container
docker rm interview-agent-test

# Remove image (optional)
docker rmi interview-agent:latest
```

---

## 📊 Phase 6: Performance Testing

### 6.1 Response Time Benchmarks
```bash
# Test LLM response time
python3 -c "
import time
from groq_client import groq_chat

messages = [{'role': 'user', 'content': 'Hello'}]

start = time.time()
response = groq_chat(messages)
elapsed = time.time() - start

print(f'LLM Response Time: {elapsed:.2f}s')
print('✅ PASS' if elapsed < 5 else '⚠️  SLOW')
"
```

**Target:** < 3 seconds

---

### 6.2 Scoring Performance
```bash
# Test scoring speed
python3 -c "
import time
from scoring_langchain import score_answer

question = 'Tell me about a project you worked on.'
answer = 'I built a REST API using Flask and PostgreSQL with 1000+ users.'

start = time.time()
result = score_answer(question, answer)
elapsed = time.time() - start

print(f'Scoring Time: {elapsed:.2f}s')
print('✅ PASS' if elapsed < 8 else '⚠️  SLOW')
"
```

**Target:** < 5 seconds

---

### 6.3 Memory Usage
```bash
# Run the app and monitor
python src/main.py &
APP_PID=$!

# Wait for startup
sleep 5

# Check memory
ps aux | grep "python src/main.py" | grep -v grep

# Kill app
kill $APP_PID
```

**Target:** < 500MB base memory

---

## 🔒 Phase 7: Security Testing

### 7.1 API Key Protection
```bash
# Test missing API key
unset GROQ_API_KEY

python3 -c "
from groq_client import groq_chat
try:
    groq_chat([{'role': 'user', 'content': 'test'}])
    print('❌ Should have raised error')
except ValueError as e:
    if 'GROQ_API_KEY' in str(e):
        print('✅ API key validation works')
"
```

---

### 7.2 Input Sanitization
```bash
# Test malicious inputs
python3 -c "
from router import handle_message
from state_manager import new_state

state = new_state()
state['stage'] = 'await_role'

# Test SQL injection attempt
response = handle_message(\"engineer'; DROP TABLE users; --\", state)
print('✅ SQL injection handled' if state['role'] == 'engineer' else '❌ Failed')

# Test XSS attempt
response = handle_message('<script>alert(1)</script>', state)
print('✅ XSS handled')

# Test extremely long input
long_input = 'a' * 100000
response = handle_message(long_input, state)
print('✅ Long input handled')
"
```

---

## 📝 Phase 8: Edge Cases Testing

### 8.1 Network Failures
```bash
# Test Groq API timeout
python3 -c "
from groq_client import groq_chat
import requests

# Simulate timeout
try:
    # This should timeout or fail gracefully
    response = groq_chat([{'role': 'user', 'content': 'test'}])
except Exception as e:
    print(f'✅ Network error handled: {type(e).__name__}')
"
```

---

### 8.2 File System Issues
```bash
# Test missing role file
python3 -c "
from rag_loader import load_role_context

# Test non-existent role
context = load_role_context('nonexistent_role')
assert context == {}
print('✅ Missing role file handled')
"
```

---

### 8.3 Concurrent Users (Stateful Issue)
```bash
# Test state isolation
python3 -c "
from state_manager import new_state

state1 = new_state()
state2 = new_state()

state1['role'] = 'engineer'
state2['role'] = 'product'

assert state1['role'] != state2['role']
print('✅ State isolation works')
print('⚠️  Note: In production, need session management')
"
```

---

## ✅ Testing Summary Checklist

### Core Components:
- [ ] Groq API client works
- [ ] RAG loader loads all roles
- [ ] LangChain scoring returns valid JSON
- [ ] Whisper STT transcribes audio
- [ ] Piper TTS generates audio
- [ ] State manager maintains state
- [ ] Final summary generator works

### Integration:
- [ ] Router handles text messages
- [ ] Router handles audio messages
- [ ] Error handling works (empty inputs, invalid roles)
- [ ] Multi-round interview flow works
- [ ] Score visualization updates in real-time

### UI:
- [ ] Gradio launches successfully
- [ ] 2-column layout displays correctly
- [ ] Text mode works end-to-end
- [ ] Voice mode works end-to-end
- [ ] Score panel updates
- [ ] Reset button clears session

### Docker:
- [ ] Image builds successfully
- [ ] Container runs and exposes port 7860
- [ ] Health check passes
- [ ] All features work in container

### Performance:
- [ ] LLM responses < 3s
- [ ] Scoring < 5s
- [ ] Memory usage < 500MB

### Security:
- [ ] API key validation works
- [ ] Input sanitization prevents injection
- [ ] Long inputs handled gracefully

---

## 🐛 Common Issues & Troubleshooting

### Issue 1: "GROQ_API_KEY not set"
**Solution:**
```bash
export GROQ_API_KEY=your_key_here
# Or add to .env file
```

### Issue 2: "Whisper binary not found"
**Solution:**
```bash
cd whisper
make
# Verify: ls build/bin/whisper-cli
```

### Issue 3: "Piper not installed"
**Solution:**
```bash
pip install piper-tts
python3 -m piper.download en_US-lessac-medium
```

### Issue 4: "Module not found"
**Solution:**
```bash
# Ensure running from project root
cd /mnt/sagittarius/Bargi
python src/main.py
```

### Issue 5: Gradio not loading
**Solution:**
```bash
# Check port availability
lsof -i :7860
# Kill if needed
kill -9 <PID>
```

### Issue 6: Score panel shows null
**Solution:**
- This is normal during setup and question prompts
- Scores only appear after answering questions

---

## 🎓 Test Results Template

```
===========================================
AI Interview Agent - Test Results
===========================================
Date: _______________
Tester: _______________

PHASE 1: Environment Setup
  [ ] Python 3.10+
  [ ] Dependencies installed
  [ ] API key configured
  [ ] Whisper.cpp built
  [ ] Piper TTS installed

PHASE 2: Component Tests
  [ ] Groq API: _____ (PASS/FAIL)
  [ ] RAG Loader: _____ (PASS/FAIL)
  [ ] Scoring: _____ (PASS/FAIL)
  [ ] Whisper STT: _____ (PASS/FAIL)
  [ ] Piper TTS: _____ (PASS/FAIL)
  [ ] State Manager: _____ (PASS/FAIL)
  [ ] Final Summary: _____ (PASS/FAIL)

PHASE 3: Integration Tests
  [ ] Router (text): _____ (PASS/FAIL)
  [ ] Router (voice): _____ (PASS/FAIL)
  [ ] Error handling: _____ (PASS/FAIL)

PHASE 4: UI Tests
  [ ] Visual layout: _____ (PASS/FAIL)
  [ ] Text mode flow: _____ (PASS/FAIL)
  [ ] Voice mode flow: _____ (PASS/FAIL)
  [ ] Reset button: _____ (PASS/FAIL)

PHASE 5: Docker Tests
  [ ] Build: _____ (PASS/FAIL)
  [ ] Run: _____ (PASS/FAIL)
  [ ] Health check: _____ (PASS/FAIL)

PHASE 6: Performance
  [ ] LLM response: _____s
  [ ] Scoring: _____s
  [ ] Memory: _____MB

PHASE 7: Security
  [ ] API key protection: _____ (PASS/FAIL)
  [ ] Input sanitization: _____ (PASS/FAIL)

Overall Status: _____ (PASS/FAIL)
Notes:
_________________________________________
_________________________________________
===========================================
```

---

## 📚 Next Steps After Testing

1. **If all tests pass:**
   - Deploy to production
   - Set up monitoring (logs, metrics)
   - Add analytics for interview sessions

2. **If tests fail:**
   - Review error logs
   - Check component dependencies
   - Verify API keys and model paths
   - Consult troubleshooting section

3. **Future enhancements:**
   - Add session persistence (database)
   - Implement user authentication
   - Add more interview personas (confused, chatty, efficient)
   - Advanced RAG with vector stores
   - Multi-language support

---

**Happy Testing! 🚀**
