from typing import Union
from RealtimeSTT import AudioToTextRecorder
import RealtimeTTS
from colorama import Fore, Style
import colorama
from settings import api_key_map, tp_model_map
import os

from dotenv import load_dotenv
from groq import Groq
import openai


AUDIO_HANDLING_PROMPT = \
"""
You are a hiring recruiter lead at a tech saas company. A sales agent from a company "foundit" is trying to sell you a recruiting solution.
The sales agent will ask you questions about your current recruiting process and try to convince you to take a demo of their product.
You need to dig deeper into value proposition, lay objections on the product and decide if you want to take a demo or not based on the sales agents conversations.
You also need to bring up issues on the recent bad PR the company faced about its poor pricing. 
Tone of conversation - rude, blunt and a little fast paced.
"""


colorama.init()

tts_model = 'tts-1-hd'
chat_client_type = 'openai'
tp_model_name = tp_model_map[chat_client_type]
stt_model_name = "tiny"


# global full_sentences, displayed_text, history
full_sentences = []
history = []
displayed_text = ""


if __name__ == '__main__':

    print("Initializing RealtimeSTT test...")

    def clear_console():
        os.system('clear' if os.name == 'posix' else 'cls')

    def text_detected(text):
        global displayed_text
        sentences_with_style = [
            f"{Fore.YELLOW + sentence + Style.RESET_ALL if i % 2 == 0 else Fore.CYAN + sentence + Style.RESET_ALL} "
            for i, sentence in enumerate(full_sentences)
        ]
        new_text = "".join(sentences_with_style).strip() + " " + text if len(sentences_with_style) > 0 else text

        if new_text != displayed_text:
            displayed_text = new_text
            # clear_console()
            print(f"Language: {recorder.detected_language} (realtime: {recorder.detected_realtime_language})")
            print(displayed_text, end="", flush=True)


    def process_text(text):
        global full_sentences, history
        full_sentences.append(text)
        history.append({'role': 'user', 'content': text})
        text_detected("")

        # assistant_response = get_chat_response(chat_client, [{ 'role': 'system',  'content': character_prompt}] + history[-10:])
        assistant_response = ""
        for ar in get_chat_response(chat_client, [{ 'role': 'system',  'content': character_prompt}] + history[-10:]):
            assistant_response += ar

        print("Assistant response:", assistant_response)
        print("history:", history)

        stream.feed(assistant_response).play()
        history.append({'role': 'assistant', 'content': stream.text()})
        history.append({'role': 'assistant', 'content': assistant_response})

        full_sentences = list()
        # clear_console()
        print("Say something again...", end="", flush=True)

    

    def get_chat_response(client: Union[openai.OpenAI, Groq], messages: list):
        for chunk in client.chat.completions.create(model=tp_model_name, messages=messages, stream=True):
                if (text_chunk := chunk.choices[0].delta.content): yield text_chunk


    def get_chat_client(client_type):
        if client_type == "openai":
            return openai.OpenAI(api_key=api_key_map["openai"])
        elif client_type == "groq":
            return Groq(api_key=api_key_map["groq"])
        else:
            raise ValueError("Invalid client type")


    recorder_config = {
        'spinner': False,
        'model': 'tiny',
        'silero_sensitivity': 0.4,
        'webrtc_sensitivity': 2,
        'post_speech_silence_duration': 1,
        'min_length_of_recording': 0,
        'min_gap_between_recordings': 0,
        'enable_realtime_transcription': True,
        'realtime_processing_pause': 0.2,
        'realtime_model_type': 'tiny',
        'on_realtime_transcription_update': text_detected, 
        'silero_deactivity_detection': True,
    }

    load_dotenv()
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    character_prompt = AUDIO_HANDLING_PROMPT
    text_to_audio_engine = RealtimeTTS.OpenAIEngine(model='tts-1-hd', voice='nova')
    stream = RealtimeTTS.TextToAudioStream(text_to_audio_engine, log_characters=True)

    chat_client = get_chat_client(chat_client_type)

    recorder = AudioToTextRecorder(**recorder_config)

    clear_console()
    print("Say something...", end="", flush=True)

    while True:
        recorder.text(process_text)
