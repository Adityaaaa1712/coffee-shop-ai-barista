import os
from pathlib import Path
from dotenv import load_dotenv

def load_env():
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        raise FileNotFoundError(
            "Missing .env file. Please copy .env.example to .env and add your OpenAI API key."
        )
    load_dotenv(env_path)

def get_openai_key():
    load_env()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        raise ValueError(
            "OpenAI API key not set. Please edit .env and add a valid OPENAI_API_KEY."
        )
    return api_key

MENU_PATH = Path(__file__).parent / "data" / "menu.json"
ORDERS_PATH = Path(__file__).parent / "data" / "orders.json"
