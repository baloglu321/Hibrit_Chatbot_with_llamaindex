# 🤖 Hybrid Chatbot and Agent System

A sophisticated hybrid AI system that intelligently routes user queries between a lightweight conversational LLM and a powerful ReAct Agent equipped with specialized tools. Built with LlamaIndex and Gradio.

## 📊 Architecture

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {'primaryColor':'#1f2937','primaryTextColor':'#fff','primaryBorderColor':'#4b5563','lineColor':'#6b7280','secondaryColor':'#374151','tertiaryColor':'#1f2937','textColor':'#fff','fontSize':'14px'}}}%%
graph TB
    User["👤 User"]
    Gradio["🖥️ Gradio Interface"]
    Router["🧭 Query Router<br/>(LLM-based Classifier)"]
    BasicModule["💬 Basic Chat Module"]
    AgentModule["🤖 ReAct Agent Module"]
    Memory["🧠 Chat Memory Buffer<br/>(40k tokens)"]
    
    User -->|"Query"| Gradio
    Gradio -->|"Analyze Query"| Router
    Router -->|"BASIC<br/>(Simple Chat)"| BasicModule
    Router -->|"AGENT<br/>(Complex Task)"| AgentModule
    
    BasicModule -->|"Direct Response"| OllamaLLM["🦙 Ollama LLM<br/>(Gemma 3 27B)"]
    AgentModule --> Memory
    AgentModule --> OllamaLLM
    AgentModule --> ToolHub["🛠️ Tool Hub"]
    
    ToolHub --> WebTools["🌐 Web Search<br/>• DuckDuckGo<br/>• Wikipedia<br/>• Arxiv"]
    ToolHub --> DataTools["📊 Data Processing<br/>• Math Operations<br/>• File Downloads<br/>• Excel/JSON Parser"]
    ToolHub --> MediaTools["🎬 Media Processing<br/>• YouTube Downloader<br/>• Audio Transcriber<br/>• Image Captioner"]
    ToolHub --> APITools["🌤️ External APIs<br/>• Weather API<br/>(Weatherstack)"]
    
    OllamaLLM -->|"Response"| Gradio
    ToolHub -->|"Tool Results"| AgentModule
    AgentModule -->|"Final Answer"| Gradio
    Gradio -->|"Display"| User
    
    style User fill:#4f46e5,stroke:#6366f1,color:#fff
    style Gradio fill:#059669,stroke:#10b981,color:#fff
    style Router fill:#dc2626,stroke:#ef4444,color:#fff
    style BasicModule fill:#0891b2,stroke:#06b6d4,color:#fff
    style AgentModule fill:#7c3aed,stroke:#8b5cf6,color:#fff
    style Memory fill:#db2777,stroke:#ec4899,color:#fff
    style OllamaLLM fill:#ea580c,stroke:#f97316,color:#fff
    style ToolHub fill:#65a30d,stroke:#84cc16,color:#fff
    style WebTools fill:#0284c7,stroke:#0ea5e9,color:#fff
    style DataTools fill:#0d9488,stroke:#14b8a6,color:#fff
    style MediaTools fill:#6366f1,stroke:#818cf8,color:#fff
    style APITools fill:#c026d3,stroke:#d946ef,color:#fff
```

## ✨ Key Features

### 🎯 Intelligent Query Routing
- **Smart Classification**: LLM-powered router analyzes each query and classifies it as `BASIC` (simple conversation) or `AGENT` (complex task requiring tools)
- **Optimized Performance**: Simple queries get fast responses; complex queries leverage full agent capabilities

### 💬 Dual-Mode Processing

#### Basic Chat Mode
- Handles general conversation, greetings, and simple Q&A
- Direct connection to Ollama LLM for fast responses
- Maintains conversation history for context

#### Agent Mode
- **LlamaIndex ReAct Agent**: Advanced reasoning with multi-step tool orchestration
- **Asynchronous Execution**: Non-blocking tool calls for better performance
- **Persistent Memory**: 40,000 token context window for extended conversations

### 🛠️ Comprehensive Tool Suite

| Category | Tools | Description |
|----------|-------|-------------|
| **Web Search** | DuckDuckGo, Wikipedia, Arxiv | Real-time information retrieval from multiple sources |
| **Mathematics** | Add, Subtract, Multiply, Divide | Basic arithmetic operations with error handling |
| **Weather** | Weatherstack API | Current weather information for any location |
| **Media Processing** | YouTube Downloader, Whisper Transcriber, Image Captioner | Download and analyze video/audio/image content |
| **File Handling** | File Downloader, Excel/JSON Parser | Retrieve and process structured data files |

## 🛠️ Technologies Used

### Core Framework
- **LlamaIndex**: ReAct Agent framework for tool orchestration
- **Gradio**: Interactive web-based chat interface
- **Ollama**: Local LLM inference (Gemma 3 27B model)

### AI & ML
- **Whisper**: OpenAI's speech-to-text model for audio transcription
- **LLaMA Index Tools**: Pre-built integrations for Wikipedia, DuckDuckGo, Arxiv

### Python Libraries
- **asyncio & nest_asyncio**: Asynchronous execution
- **requests**: HTTP client for API calls
- **Pillow (PIL)**: Image processing
- **pandas**: Data manipulation and Excel handling
- **yt-dlp**: YouTube video/audio downloading

### External Services
- **Cloudflare Tunnel**: Secure access to Ollama server
- **Weatherstack API**: Weather data provider

## 📥 Installation

### Prerequisites

1. **Ollama Server**: Install and run Ollama with the Gemma 3 27B model
   ```bash
   ollama pull gemma3:27b
   ```

2. **Python 3.8+**: Ensure Python is installed

3. **yt-dlp**: Required for YouTube downloads
   ```bash
   pip install yt-dlp
   ```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
CLOUDFLARE_TUNNEL_URL=https://your-ollama-tunnel-url/
OLLAMA_MODEL_ID=gemma3:27b
WEATHER_API=your-weatherstack-api-key
```

Update `agent.py` and `app.py` to load environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

CLOUDFLARE_TUNNEL_URL = os.getenv("CLOUDFLARE_TUNNEL_URL")
OLLAMA_MODEL_ID = os.getenv("OLLAMA_MODEL_ID", "gemma3:27b")
WEATHER_API = os.getenv("WEATHER_API")
```

### Configuration Variables

| Variable | Files | Example Value | Purpose |
|----------|-------|---------------|---------|
| `CLOUDFLARE_TUNNEL_URL` | `app.py`, `agent.py` | `"https://your-tunnel.com/"` | Public endpoint for Ollama service |
| `OLLAMA_MODEL_ID` | `app.py`, `agent.py` | `"gemma3:27b"` | LLM model identifier |
| `WEATHER_API` | `agent.py` | `"your-api-key"` | Weatherstack API key |

## 🚀 Usage

Start the application:

```bash
python app.py
```

The Gradio interface will launch at `http://127.0.0.1:7860`

### Example Queries

**Basic Mode (Fast Response):**
- "Hello, how are you?"
- "Tell me a joke"
- "What is Python?"

**Agent Mode (Tool-Powered):**
- "What's the current population of Turkey?" (Web Search)
- "What's the weather in Istanbul?" (Weather API)
- "Calculate 125 × 47" (Math Tool)
- "Download and transcribe this YouTube video: [URL]" (Media Tools)
- "Analyze this image: image.jpg - What objects are in it?" (Image Captioner)

## 🏗️ Project Structure

```
Hibrit_Chatbot_with_llamaindex/
├── app.py                 # Main Gradio application with routing logic
├── agent.py               # ReAct Agent setup and tool definitions
├── deneme.py              # Test/demo script
├── requirements.txt       # Python dependencies
├── system_prompt.txt      # Agent system instructions
└── README.md              # This file
```

## 🧰 Available Tools

### 1. Web Search Tools
- **DuckDuckGo Search**: General web search
- **Wikipedia**: Encyclopedia lookups
- **Arxiv**: Academic paper search

### 2. Mathematical Tools
- **add_tool**: Addition operations
- **subtract_tool**: Subtraction operations
- **multiply**: Multiplication operations
- **divide_tool**: Division with zero-check

### 3. Weather Tool
- **my_weather_tool**: Fetches current weather via Weatherstack API

### 4. Media Processing Tools
- **youtube_video_download**: Downloads YouTube videos
- **youtube_transcript**: Extracts audio and generates transcript
- **mp3_transcript**: Transcribes audio files using Whisper
- **image_captioner**: Analyzes images with multimodal LLM

### 5. File Tools
- **File_Download_Tool**: Downloads and parses Excel/JSON files

## 🛑 Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `ConnectionError` | Ollama unreachable | Verify Ollama is running and tunnel URL is correct |
| `ValueError: ReActAgent has no field "memory"` | Memory assignment error | Use `memory.reset()` and `memory.put()` methods |
| `AttributeError: ChatMessage has no attribute 'get'` | Wrong return type | Ensure agent returns `str(response)` |
| Agent loses context | Token limit too low | Increase `token_limit` in `ChatMemoryBuffer.from_defaults()` |
| Weather tool fails | Invalid API key | Verify Weatherstack API key in `.env` |
| YouTube download fails | yt-dlp not installed | Install: `pip install yt-dlp` |

## 🔒 Security Best Practices

⚠️ **Never commit API keys or secrets to version control!**

1. Store sensitive values in `.env` file
2. Add `.env` to `.gitignore`
3. Use environment variables in code
4. Share `.env.example` template instead

### Example `.gitignore`

```gitignore
# Environment
.env
.env.local

# Python
__pycache__/
*.pyc

# Media downloads
*.mp3
*.mp4
audio.mp3
video.mp4
```

## 📝 How It Works

1. **User Input**: Query submitted via Gradio interface
2. **Routing**: LLM router analyzes query complexity
3. **Processing**:
   - **Basic**: Direct LLM response for simple queries
   - **Agent**: ReAct loop with tool selection and execution
4. **Memory Management**: Conversation history maintained in buffer
5. **Response**: Final answer streamed back to user

### Agent Reasoning Flow

```
Query → Agent Thinks → Selects Tool → Executes Tool → 
Evaluates Result → [Loop if needed] → Final Answer
```

## 🎯 Use Cases

- **Research Assistant**: Search academic papers, Wikipedia, web
- **Data Analyst**: Download and analyze Excel/JSON files
- **Weather Reporter**: Real-time weather information
- **Content Analyzer**: Transcribe videos, caption images
- **Calculator**: Complex mathematical operations
- **Conversation Partner**: General chat and Q&A

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Add more specialized tools
- Implement streaming responses
- Add logging and monitoring
- Create unit tests
- Optimize token usage

## 📄 License

This project is open-source and available under the MIT License.

## 🙏 Acknowledgments

- **LlamaIndex**: For the excellent agent framework
- **Gradio**: For the intuitive UI library
- **Ollama**: For local LLM inference
- **OpenAI Whisper**: For speech recognition

---

**Built with ❤️ using LlamaIndex, Gradio, and Ollama**
