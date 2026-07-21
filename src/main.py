import os
import sys

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Name of the model used for chat completions.
# You can swap this for any chat model your OpenAI account has access to.
MODEL_NAME = "gpt-5-mini"

# The system message defines the assistant's behavior/persona.
# It is sent once and stays at the start of the conversation history.
SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are a helpful, friendly assistant. Keep answers clear and concise.",
}


def load_api_key() -> str:
    """
    Load the OpenAI API key from an environment variable.

    Loads variables from a local .env file (if present) using python-dotenv,
    then reads OPENAI_API_KEY from the environment. The key is never
    written into the source code.
    """
    load_dotenv()  # Reads a local .env file and loads its variables into os.environ

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print(
            "ERROR: OPENAI_API_KEY not found.\n"
            "Create a .env file (see .env.example) and set your API key there."
        )
        sys.exit(1)

    return api_key


def get_ai_response(client: OpenAI, conversation_history: list) -> str:
    """
    Send the full conversation history to the OpenAI API and return the
    assistant's reply as a string.

    Sending the entire history (not just the latest message) is what
    allows the model to "remember" earlier turns in the conversation.
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=conversation_history,
    )

    # The API returns a list of "choices"; we only requested one completion,
    # so we read the assistant's message from choices[0].
    return response.choices[0].message.content


def chat_loop() -> None:
    """
    Run the main interactive loop:
    - Read user input
    - Send it (with history) to the API
    - Print the AI's reply
    - Repeat until the user types 'exit' or 'quit'
    """
    api_key = load_api_key()
    client = OpenAI(api_key=api_key)

    # Conversation history starts with the system message only.
    # Every user message and assistant reply gets appended to this list.
    conversation_history = [SYSTEM_MESSAGE]

    print("AI Chatbot (type 'exit' or 'quit' to end the conversation)")
    print("-" * 60)

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("Chatbot: Goodbye!")
            break

        if not user_input:
            # Skip empty input instead of sending a blank message to the API.
            continue

        # Add the user's message to the history before calling the API.
        conversation_history.append({"role": "user", "content": user_input})

        try:
            ai_reply = get_ai_response(client, conversation_history)

        except OpenAIError as e:
            # Covers authentication errors, rate limits, invalid requests, etc.
            print(f"Chatbot: Sorry, an API error occurred: {e}")
            # Remove the last user message so the failed turn isn't kept
            # in history and doesn't confuse the next request.
            conversation_history.pop()
            continue

        except Exception as e:
            # Covers network issues (no internet, DNS failure, timeouts, etc.)
            print(f"Chatbot: Sorry, something went wrong: {e}")
            conversation_history.pop()
            continue

        # Add the assistant's reply to the history so future requests
        # include it as context.
        conversation_history.append({"role": "assistant", "content": ai_reply})

        print(f"Chatbot: {ai_reply}")


if __name__ == "__main__":
    chat_loop()
