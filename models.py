from langchain_openai import ChatOpenAI
from openai import OpenAI
from api import OPENAI_API_KEY
model = ChatOpenAI(model="gpt-4o", openai_api_key=OPENAI_API_KEY)
stt_tts_model = OpenAI(api_key=OPENAI_API_KEY)