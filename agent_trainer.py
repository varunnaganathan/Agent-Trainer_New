import os
from openai import OpenAI
import speech_recognition as sr
import playsound
from settings import OPENAI_API_KEY
from prompts.agent_response import AUDIO_HANDLING_PROMPT


class SpeechBot:
    def __init__(
            self, 
            audio_handling_prompt,
            tp_model_name='gpt-4',
            stt_model_name='whisper-1',
            tts_model_name='tts-1',
            tts_voice='alloy'
        ):
        self.recognizer = sr.Recognizer()
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

        self.audio_handling_prompt = audio_handling_prompt
        self.stt_model_name = stt_model_name
        self.tp_model_name = tp_model_name
        self.tts_model_name = tts_model_name
        self.tts_voice = tts_voice

        self.messages = [
            {
                "role": "system",
                "content": audio_handling_prompt
            }
        ]
    
    def listen(self):
        """Capture audio from the microphone until the user stops speaking and return as text."""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            
            # Listen continuously until the user stops speaking
            audio = self.recognizer.listen(source, phrase_time_limit=None, timeout=None)
            
            audio_file_path = 'data/user_input.wav'
            with open(audio_file_path, 'wb') as f:
                f.write(audio.get_wav_data())

        try:
            # audio_file_path = 'data/harvard.wav'
            print("Recognizing...")
            response = self.client.audio.transcriptions.create(
                file=open(audio_file_path, 'rb'),
                model=self.stt_model_name
            )
            print(response)
            text = response.text.strip()

            self.messages.append({
                "role": "user",
                "content": text
            })

            os.remove(audio_file_path)
            
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, there seems to be a problem with the service.")
            return ""
    

    def process_text(self):
        response = self.client.chat.completions.create(
            model=self.tp_model_name,
            messages=self.messages,
        )
        response_text = response.choices[0].message.content.strip()
        self.messages.append({
            "role": "assistant",
            "content": response_text
        })
        print("Assistant:", response_text)
        return response_text
    
    def speak(self, text):
        speech_file_path = 'data/assistant_output.wav'
        with self.client.audio.speech.with_streaming_response.create(
            model=self.tts_model_name,
            voice=self.tts_voice,
            input=text,
            response_format='wav',
            speed=1.0,
        ) as response: 
            response.stream_to_file(speech_file_path)
        
        playsound.playsound(speech_file_path, True)
        
        # os.remove(speech_file_path)

    def run(self):
        while True:
            text = self.listen()
            if not text:
                continue
            response = self.process_text()
            
            self.speak(response)
            break


if __name__ == "__main__":
    bot = SpeechBot(AUDIO_HANDLING_PROMPT)
    bot.run()