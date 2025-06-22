from dotenv import load_dotenv
import os

load_dotenv()
def get_env_variable(key) -> str:
    return os.getenv(key=key, default="")