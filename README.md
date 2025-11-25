🤖 Hybrid Chatbot and Agent System
This project implements a flexible hybrid artificial intelligence system designed to analyze user queries and intelligently route them to the appropriate processing module. Simple conversational questions are handled by a standard Large Language Model (LLM), while complex, information-intensive tasks requiring external capabilities are delegated to a powerful ReAct Agent equipped with specialized tools.

✨ Features
Query Routing: Classifies every incoming message as either BASIC (simple chat) or AGENT (complex, tool-requiring task) using an internal LLM router.

Basic Module: Utilizes an external Ollama LLM service for general conversation and simple Q&A.

Agent Module: Built on the LlamaIndex ReAct Agent framework, capable of sophisticated reasoning and access to various external tools (Web Search, File Handling, Calculation, etc.).

Asynchronous Operation: The Agent module runs all its heavy lifting, including external tool calls, asynchronously using asyncio.

Context/Memory Management: The Gradio chat history is injected into the Agent's memory buffer on every call, ensuring conversation context is preserved for follow-up questions.

User Interface: A fast and interactive chat interface provided by Gradio.

🛠️ Setup
Prerequisites
You need Python and its dependencies, plus an accessible Ollama server to host the large language model.

Ollama Installation: Ensure you have Ollama running and accessible.

Ollama Model: The gemma3:27b model must be pulled and available on your Ollama server.

Project Dependencies
Install the required Python libraries using the provided environment file:

Bash

pip install -r requirements.txt
Configuration
The system requires specific URLs and API keys. You must update these variables in the relevant files:
Variable,File,Example Value,Purpose
CLOUDFLARE_TUNNEL_URL,"app.py, agent.py","""https://your-ollama-tunnel-url/""",The public endpoint to reach your Ollama service.
OLLAMA_MODEL_ID,"app.py, agent.py","""gemma3:27b""",The name of the model to use.
WEATHER_API,agent.py,"""your-weather-api-key""","API key for the weather tool (e.g., Weatherstack)."

📜 Agent Tools (Available Capabilities)
The ReAct Agent has access to the following specialized tools via llama_index.core.tools.FunctionTool:

DuckDuckGoSearchToolSpec (Web Search)

WikipediaToolSpec (General Knowledge)

ArxivToolSpec (Scientific Papers)

my_weather_tool (Current Weather Info)

image_captioner (Multimodal Image Analysis)

File_Download_Tool (Download/Preview various files: Excel, JSON, MP3, Images)

youtube_transcript (Extracts audio transcript from a YouTube URL)

mp3_transcript (Transcribes local audio files)

Arithmetic Tools: multiply, add, subtract, divide

🚀 How to Run
Start the Gradio interface by running the main application file:

Bash

python app.py
The application will launch on a local URL (e.g., http://127.0.0.1:7860).

Test Scenarios
Scenario,Example Query,Expected Routing
Simple Chat,"""What is the biggest city in the UK?""",BASIC
Contextual Q&A,"""What is the capital of Turkey?"" followed by ""What is its population?""",AGENT (Uses memory)
Tool Use,"""What is the weather like in New York City right now?""",AGENT (my_weather_tool)
Complex Reasoning,"""Who wrote 'The Hitchhiker's Guide to the Galaxy'?""",AGENT (DuckDuckGo or Wikipedia)

🛑 Troubleshooting Common Issues

Error Message,Likely Cause,Solution
requests.exceptions.ConnectionError,Ollama service is unreachable or the CLOUDFLARE_TUNNEL_URL is incorrect.,Verify your Ollama server is running and the tunnel URL is correct and active.
"ValueError: ""ReActAgent"" object has no field ""memory""",Direct assignment to Agent's memory is restricted by Pydantic.,"Ensure agent_response uses llm_agent.memory.reset() and llm_agent.memory.put() methods to update the content, rather than trying to reassign the entire memory object."
AttributeError: 'ChatMessage' object has no attribute 'get',Agent is returning a LlamaIndex object instead of a clean string.,"In agent.py, ensure the proc function returns the answer as a final string: return str(response.response)."
Agent loses context after a few turns.,Memory token_limit is too low.,"In agent.py, update ChatMemoryBuffer.from_defaults(token_limit=7500) (or highest safe value) to allocate more space for history."
