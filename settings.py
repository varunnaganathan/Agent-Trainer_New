from dotenv import load_dotenv
import os


load_dotenv()


DEFAULT_GROQ_LLM = "llama-3.1-70b-versatile"
# DEFAULT_GROQ_LLM = "llama3-70b-8192"
OPENAI_URL = "https://api.openai.com/v1"
OPENAI_LLM = 'gpt-4'

GROQ_API_KEY = os.environ.get('GROQ_API_KEY_DOT')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

data_dir = 'LLM-Data'