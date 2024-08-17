from typing import Union
import RealtimeSTT, RealtimeTTS
import openai, os
from groq import Groq
from openai import OpenAI
from dotenv import load_dotenv
from settings import api_key_map, tp_model_map
from prompts.agent_response import AUDIO_HANDLING_PROMPT

tts_model = 'tts-1-hd'
chat_client_type = 'groq'
tp_model_name = tp_model_map[chat_client_type]
stt_model_name = "tiny"


def get_chat_response(client: Union[OpenAI, Groq], messages: list):
    for chunk in client.chat.completions.create(model=tp_model_name, messages=messages, stream=True):
            if (text_chunk := chunk.choices[0].delta.content): yield text_chunk



def get_chat_client(client_type):
    if client_type == "openai":
        return OpenAI(api_key=api_key_map["openai"])
    elif client_type == "groq":
        return Groq(api_key=api_key_map["groq"])
    else:
        raise ValueError("Invalid client type")


if __name__ == '__main__':
    load_dotenv()
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    character_prompt = AUDIO_HANDLING_PROMPT
    text_to_audio_engine = RealtimeTTS.OpenAIEngine(model='tts-1-hd', voice='nova')
    stream = RealtimeTTS.TextToAudioStream(text_to_audio_engine, log_characters=True)

    chat_client = get_chat_client(chat_client_type)
    recorder = RealtimeSTT.AudioToTextRecorder(model=stt_model_name)

    history = []
    while True:
        print("\n\nSpeak when ready")
        print(f'>>> {(user_text := recorder.text())}\n<<< ', end="", flush=True)
        history.append({'role': 'user', 'content': user_text})
        assistant_response = get_chat_response(chat_client, [{ 'role': 'system',  'content': character_prompt}] + history[-10:])
        
        # print("\n\nAssistant Response:")
        # for stream_chunk in assistant_response:
        #     print(f'>>> {stream_chunk}\n<<< ', end="", flush=True)
        
        stream.feed(assistant_response).play()
        history.append({'role': 'assistant', 'content': stream.text()})