# VoiceBot Application Flow - Complete Explanation

## 🎯 Overview
This is a **Voice-Enabled Banking Assistant** that converts speech to text, processes queries through a multi-tier response system, and converts responses back to speech.

---

## 📊 Complete Flow Diagram

```
USER SPEAKS → [Gradio UI] → Audio File (temp)
    ↓
[Speech-to-Text] → Text String
    ↓
[Bot Response Logic] → Response Text
    ├─→ FAQ Search (data/faq.json)
    ├─→ Recommendation Engine (logic.py)
    └─→ LLM Fallback (Groq API)
    ↓
[Text-to-Speech] → Audio File (temp_audio/output_audio.mp3)
    ↓
[Gradio UI] → Display Text + Play Audio
```

---

## 🔄 Step-by-Step Flow

### **STEP 1: User Input (gradio_app.py)**

**Location:** `src/gradio_app.py` - Line 22-25

**What Happens:**
- Gradio creates a web interface at `http://127.0.0.1:7860`
- User clicks the microphone button and speaks
- Gradio records audio and saves it to a **temporary file** (Windows temp directory)
- The file path is passed to the `main()` function

**File Saved:**
- **Location:** Windows temp directory (e.g., `C:\Users\LENOVO\AppData\Local\Temp\tmpXXXXX.wav`)
- **Format:** WAV or MP3 (depends on browser/system)
- **Lifecycle:** Temporary, deleted after processing

**Code:**
```python
inputs=gr.Audio(sources=["microphone"],type="filepath")
# Returns: "C:\Users\...\Temp\tmp1xssrgb5.wav"
```

---

### **STEP 2: Speech-to-Text Conversion (voice.py)**

**Location:** `src/voice.py` - `speech_to_text()` function (Lines 9-43)

**What Happens:**
1. **Audio Format Conversion:**
   - Uses `pydub.AudioSegment` to read the input audio file
   - Creates a temporary WAV file (required by SpeechRecognition library)
   - Converts any format (MP3, M4A, etc.) to WAV format
   - **Temp WAV file:** `C:\Users\...\Temp\tmpXXXXX.wav`

2. **Speech Recognition:**
   - Uses `speech_recognition` library with Google's free API
   - Reads the WAV file and extracts audio data
   - Sends audio to Google Speech Recognition service (no API key needed)
   - Returns transcribed text string

3. **Cleanup:**
   - Deletes the temporary WAV file after processing
   - Original Gradio temp file remains (Gradio manages it)

**Files Created/Deleted:**
- ✅ **Created:** Temporary WAV file in Windows temp directory
- ❌ **Deleted:** Temporary WAV file after transcription (in `finally` block)

**Output:**
- Returns: `"How can I open a savings account?"` (text string)

---

### **STEP 3: Bot Response Generation (app.py + logic.py)**

**Location:** `src/app.py` - `bot_response()` function (Lines 27-39)

**What Happens - Multi-Tier Response System:**

#### **Tier 1: FAQ Search** (Lines 29-31)
- **File:** `data/faq.json` (loaded at startup in `logic.py`)
- **Function:** `search_faq()` in `logic.py` (Lines 9-13)
- **Process:**
  - Splits user input into words
  - Searches FAQ questions for matching words (case-insensitive)
  - Returns matching answer if found
- **Example:**
  - Input: `"How can I open a savings account?"`
  - Matches: `"How can I open a savings account?"` in FAQ
  - Returns: `"To open a savings account, you typically need..."`

#### **Tier 2: Recommendation Engine** (Lines 34-36)
- **Function:** `get_recommendation()` in `logic.py` (Lines 15-22)
- **Process:**
  - Checks for keywords: "student", "business", "loan" + "salary"
  - Returns predefined recommendations
- **Examples:**
  - Input: `"I'm a student"`
  - Returns: `"A student savings account with low minimum balance is suitable."`

#### **Tier 3: LLM Fallback** (Lines 38-39)
- **API:** Groq API (using `llama-3.1-8b-instant` model)
- **Function:** `ask_llm()` in `app.py` (Lines 17-25)
- **Process:**
  - Sends system prompt + user message to Groq API
  - System prompt defines bot as "junior banking assistant"
  - Returns AI-generated response
- **API Key:** Stored in `.env` file as `GROQ_API_KEY`

**Files Read:**
- ✅ `data/faq.json` - FAQ database (loaded once at startup)

**Output:**
- Returns: Response text string (from FAQ, recommendation, or LLM)

---

### **STEP 4: Text-to-Speech Conversion (voice.py)**

**Location:** `src/voice.py` - `text_to_speech()` function (Lines 45-60)

**What Happens:**
1. **Directory Creation:**
   - Creates `temp_audio/` directory in project root (if doesn't exist)
   - **Path:** `E:\Z_Personal\Solvio\VoiceBot\temp_audio\`

2. **Audio Generation:**
   - Uses `gTTS` (Google Text-to-Speech) - free, no API key needed
   - Converts text to speech audio
   - Saves as MP3 file

3. **File Saving:**
   - **File:** `temp_audio/output_audio.mp3`
   - **Location:** Project root directory
   - **Format:** MP3
   - **Lifecycle:** Overwritten on each new request (same filename)

**Files Created:**
- ✅ `temp_audio/output_audio.mp3` - Generated speech audio (persists until next request)

**Output:**
- Returns: File path string `"E:\Z_Personal\Solvio\VoiceBot\temp_audio\output_audio.mp3"`

---

### **STEP 5: Display Output (gradio_app.py)**

**Location:** `src/gradio_app.py` - `main()` function return (Line 16)

**What Happens:**
- Returns tuple: `(reply_text, audio_file_path)`
- Gradio displays:
  - **Textbox:** Shows the bot's text response
  - **Audio Player:** Plays the generated MP3 file

**Outputs:**
- ✅ **Text:** Displayed in Gradio textbox
- ✅ **Audio:** Played in Gradio audio player (from `temp_audio/output_audio.mp3`)

---

## 📁 File Storage Locations

### **Persistent Files (Saved):**
1. **`data/faq.json`**
   - Location: `E:\Z_Personal\Solvio\VoiceBot\data\faq.json`
   - Purpose: FAQ database
   - Lifecycle: Permanent, manually edited

2. **`temp_audio/output_audio.mp3`**
   - Location: `E:\Z_Personal\Solvio\VoiceBot\temp_audio\output_audio.mp3`
   - Purpose: Latest generated speech audio
   - Lifecycle: Overwritten on each request

3. **`.env`**
   - Location: Project root (not in repo - gitignored)
   - Purpose: Stores `GROQ_API_KEY`
   - Lifecycle: Permanent, manually created

### **Temporary Files (Auto-deleted):**
1. **Gradio Audio Input**
   - Location: `C:\Users\LENOVO\AppData\Local\Temp\tmpXXXXX.wav`
   - Purpose: User's recorded audio
   - Lifecycle: Managed by Gradio, deleted automatically

2. **Speech-to-Text WAV Conversion**
   - Location: `C:\Users\LENOVO\AppData\Local\Temp\tmpXXXXX.wav`
   - Purpose: Converted audio for speech recognition
   - Lifecycle: Deleted in `finally` block after processing

---

## 🔑 API Keys & External Services

### **Groq API** (LLM)
- **Usage:** Chat completions (fallback response)
- **Model:** `llama-3.1-8b-instant`
- **Key Location:** `.env` file → `GROQ_API_KEY`
- **Cost:** Free tier available

### **Google Speech Recognition** (STT)
- **Usage:** Speech-to-text conversion
- **Key Required:** No (free for basic usage)
- **Service:** Google's public API

### **Google Text-to-Speech** (TTS)
- **Usage:** Text-to-speech conversion
- **Key Required:** No (free)
- **Library:** `gTTS` (gtts)

---

## 🎯 Data Flow Summary

```
INPUT:
  User Voice → Gradio Temp File → Speech-to-Text → Text String

PROCESSING:
  Text → FAQ Search → (Match? → Return) OR
  Text → Recommendation → (Match? → Return) OR
  Text → Groq LLM → AI Response

OUTPUT:
  Response Text → Text-to-Speech → MP3 File → Gradio Display
```

---

## 🛠️ Key Technologies

1. **Gradio:** Web UI framework (handles audio I/O)
2. **pydub:** Audio format conversion
3. **SpeechRecognition:** Google STT wrapper
4. **gTTS:** Google TTS library
5. **Groq:** Fast LLM inference API
6. **JSON:** FAQ data storage

---

## ⚠️ Important Notes

1. **File Overwriting:** `output_audio.mp3` is overwritten on each request
2. **Temp File Cleanup:** WAV conversion files are auto-deleted
3. **FAQ Loading:** FAQ is loaded once at module import (not per request)
4. **Error Handling:** All functions have try-except blocks with user-friendly messages
5. **API Fallback:** If Groq fails, error is returned to user (no silent failures)

---

## 🔍 Debugging Output

The code includes print statements that show:
- Audio file path being processed
- Transcribed text
- Bot reply text
- Generated audio file path
- Any errors encountered

Check console/terminal for these debug messages.

