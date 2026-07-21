# AI Chatbot (CLI) using the OpenAI API

## 1. Project Overview
This is a simple, beginner-friendly command-line chatbot built in Python. It uses the official OpenAI API to generate conversational responses and keeps track of the conversation history for the duration of a single session, so the assistant can refer back to earlier messages in the same run.

The project was built as a clear, well-commented learning/portfolio piece — the goal is to demonstrate a solid understanding of API integration, environment variable management, and basic conversational state, not to build a production system.

## 2. Problem Statement
Many beginner AI projects either hardcode API keys (a security risk) or skip conversation memory entirely, producing a chatbot that forgets everything after each message. This project solves both problems in the simplest way possible:
- API keys are loaded securely from environment variables, never from source code.
- Conversation history is stored in memory and resent with every request, so the chatbot has context of the ongoing conversation.

## 3. Features
- Command-line interface for chatting with an AI assistant.
- Secure API key handling via a `.env` file (never committed to Git).
- Session-based conversation memory (the bot remembers earlier turns in the same run).
- Configurable system message to define the assistant's behavior.
- Graceful handling of API and network errors.
- Exit the chat anytime by typing `exit` or `quit`.

## 4. Technologies Used
- **Python 3.9+**
- **OpenAI Python SDK** (`openai` package) — official client for the OpenAI API
- **python-dotenv** — loads environment variables from a `.env` file

## 5. Project Architecture / Workflow

```
      User
       |
       v
  Python CLI
       |
       v
Conversation History  <----+
       |                   |
       v                   |
   OpenAI API              |
       |                   |
       v                   |
   AI Response  -----------+
       |
       v
      User
```

Each time the user sends a message, it is appended to the conversation history. The **entire** history (not just the latest message) is sent to the OpenAI API so the model has full context. The model's reply is then appended back into the history before being shown to the user, and the loop continues.

## 6. Folder Structure
```
AI-Chatbot/
│
├── README.md
├── src/
│   └── main.py
├── requirements.txt
├── .gitignore
└── .env.example
```

## 7. How the Chatbot Works — Step by Step
1. The program loads environment variables from a local `.env` file using `python-dotenv`.
2. It reads the `OPENAI_API_KEY` value and uses it to create an OpenAI client. If the key is missing, the program exits with a clear error instead of crashing unexpectedly.
3. A conversation history list is initialized with a single **system message** that tells the model how to behave (a helpful, concise assistant).
4. The program enters a loop and prompts the user for input.
5. If the user types `exit` or `quit`, the loop ends and the program says goodbye.
6. Otherwise, the user's message is appended to the conversation history and the full history is sent to the OpenAI Chat Completions API.
7. The API's reply is extracted from the response, appended to the conversation history, and printed to the console.
8. The loop repeats, so each new request includes everything said so far in the session.

## 8. Installation Instructions
1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd AI-Chatbot
   ```
2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 9. Creating and Using the `.env` File
1. Copy the example file to a new `.env` file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and replace the placeholder with your actual OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-real-key-here
   ```
3. The `.env` file is listed in `.gitignore`, so it will never be committed to version control.

## 10. How to Run the Chatbot
From the project root, run:
```bash
python src/main.py
```
Type your message and press Enter. Type `exit` or `quit` at any time to end the session.

## 11. Example Conversation
```
AI Chatbot (type 'exit' or 'quit' to end the conversation)
------------------------------------------------------------
You: Hi! Who are you?
Chatbot: Hi there! I'm an AI assistant here to help answer your questions.
You: Can you remind me what I just asked?
Chatbot: You asked me who I am.
You: exit
Chatbot: Goodbye!
```
*(This is an illustrative example — actual wording from the model will vary.)*

## 12. API Key Security Explanation
- The API key is **never** written into any `.py` file.
- It is stored locally in a `.env` file, which is excluded from Git via `.gitignore`.
- `.env.example` contains only a placeholder (`your_api_key_here`) so collaborators know what variable to set without ever seeing a real key.
- At runtime, `python-dotenv` loads the key into the environment, and the code reads it with `os.getenv("OPENAI_API_KEY")`.
- If the key is missing, the program stops with an informative message instead of failing silently or exposing anything sensitive.

## 13. Limitations
- This is a **learning/portfolio project**, not a production-ready application.
- Conversation history is stored only in memory — it is lost when the program exits (no database or file persistence).
- No user authentication, multi-user support, or cloud deployment is included.
- No retrieval-augmented generation (RAG), vector database, or LangChain integration.
- Long conversations will keep growing the message history sent to the API, which can increase token usage/cost over time (no truncation or summarization is implemented).
- Basic error handling is included, but it is not exhaustive (e.g., no retry-with-backoff logic).

## 14. Future Improvements (Optional, Not Implemented)
- Persist conversation history to a file or database between sessions.
- Add a token/length limit with automatic trimming or summarization of older messages.
- Build a simple web interface (e.g., Flask or Streamlit).
- Add streaming responses for a more real-time typing effect.
- Add unit tests for core functions.
- Add logging instead of plain `print` statements.

## 15. Author's Note
Built as a portfolio project to demonstrate practical understanding of API integration, secure credential handling, and basic conversational state management in Python.
