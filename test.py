import os
from app.config import get_env_variable
from dotenv import load_dotenv

load_dotenv()
file_name = get_env_variable('YOUTUBE_CLIENT_SECRET_JSON_FILE_PATH')

if os.path.exists(file_name):
    print("File exists")
else:
    print("File does not exist")