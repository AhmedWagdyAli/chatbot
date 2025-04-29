import json
import os

CHAT_DIR = "chat_sessions"
os.makedirs(CHAT_DIR, exist_ok=True)


def save_chat(session_id: str, role: str, content: str):
    """
    Save a chat message to a session's chat history.

    This function appends a new chat message to the session's chat history file.
    If the file does not exist, it creates a new one. Each message includes the
    role (e.g., "user" or "assistant") and the content of the message.

    Args:
        session_id (str): The unique identifier for the chat session.
        role (str): The role of the message sender (e.g., "user" or "assistant").
        content (str): The content of the chat message.

    Returns:
        None
    """
    path = os.path.join(CHAT_DIR, f"{session_id}.json")
    history = []

    if os.path.exists(path):
        with open(path, "r") as f:
            history = json.load(f)

    history.append({"role": role, "content": content})

    with open(path, "w") as f:
        json.dump(history, f, indent=2)


def get_chat_history(session_id: str):
    """
    Retrieve the chat history for a given session.

    This function reads the chat history from the session's chat history file.
    If the file does not exist or is corrupted, it returns an empty list.

    Args:
        session_id (str): The unique identifier for the chat session.

    Returns:
        List[dict]: A list of chat messages, where each message is represented
                    as a dictionary with "role" and "content" keys.
    """
    path = os.path.join(CHAT_DIR, f"{session_id}.json")
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r") as f:
            history = json.load(f)
            # Ensure the history is a list of dictionaries
            if isinstance(history, list) and all(
                isinstance(msg, dict) for msg in history
            ):
                return history
            else:
                # If the file content is invalid, return an empty list
                return []
    except (json.JSONDecodeError, IOError):
        # Handle cases where the file is corrupted or unreadable
        return []
