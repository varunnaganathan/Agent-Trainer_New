from dotenv import load_dotenv
from groq import Groq
import io
import wave
import pyaudio
import os
from openai import OpenAI
import speech_recognition as sr
from prompts.agent_response import AUDIO_HANDLING_PROMPT, AUDIO_HANDLING_PROMPT_2
from settings import OPENAI_API_KEY
from settings import api_key_map, tp_model_map, stt_model_map


def byte_stream_generator(response, buffer_size=256):
    """
    Generator function that yields a stream of bytes from the response.

    :param response: The response object from the OpenAI API call.
    """
    try:
        for byte_chunk in response.iter_bytes(chunk_size=buffer_size):
            if byte_chunk:  # Only yield non-empty byte chunks
                yield byte_chunk
            else:
                print("Skipped an empty or corrupted packet")
    except Exception as e:
        print(f"Error while streaming bytes: {e}")


class SpeechBot:
    def __init__(
            self, 
            audio_handling_prompt,
            client_type='groq',
            tts_model_name='tts-1',
            tts_voice='alloy',
            pause_threshold=2
        ):
        self.recognizer = sr.Recognizer()
        self.pause_threshold = pause_threshold

        if client_type == 'openai':
            self.client = OpenAI(
                api_key=OPENAI_API_KEY,
            )
        else:
            self.client = Groq(
                api_key=api_key_map[client_type]
            )
        
        self.openai_client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

        self.audio_handling_prompt = audio_handling_prompt
        self.stt_model_name = stt_model_map[client_type]
        self.tp_model_name = tp_model_map[client_type]
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
            self.recognizer.pause_threshold = self.pause_threshold
            
            # Listen continuously until the user stops speaking
            audio = self.recognizer.listen(source)
            audio_file_path = f'data/audio_{len(self.messages)}.wav'
            with open(audio_file_path, 'wb') as f:
                f.write(audio.get_wav_data())

        try:
            print("Recognizing...")
            response = self.client.audio.transcriptions.create(
                file=open(audio_file_path, 'rb'),
                model=self.stt_model_name
            )

            # response = self.recognizer.recognize_google_cloud(audio, language='en-in')
            print(response)
            text = response.text.strip()

            self.messages.append({
                "role": "user",
                "content": text
            })

            # os.remove(audio_file_path)
            
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError as e:
            print("Sorry, I did not understand that.")
            raise e
        except sr.RequestError as e:
            print("Sorry, there seems to be a problem with the service.")
            raise e
    
    def process_text(self):
        response = self.client.chat.completions.create(
            model=self.tp_model_name,
            messages=self.messages,
            stream=True
        )
        # create variables to collect the stream of chunks
        collected_chunks = []
        collected_messages = []
        # iterate through the stream of events
        for chunk in response:
            collected_chunks.append(chunk)  # save the event response
            chunk_message = chunk.choices[0].delta.content  # extract the message
            collected_messages.append(chunk_message)  # save the message
            if chunk_message:
                print(chunk_message, end="")  # print the message
            
        collected_messages = [m for m in collected_messages if m is not None]
        full_reply_content = ''.join(collected_messages)

        self.messages.append({
            "role": "assistant",
            "content": full_reply_content
        })

        return full_reply_content
        
    
    
    def speak(self, text):
        with self.openai_client.audio.speech.with_streaming_response.create(
            model="tts-1-hd",
            voice="nova",
            input=text,
            response_format= "wav",
        ) as response:
            try:
                # Initialize PyAudio
                p = pyaudio.PyAudio()

                # Open the stream
                stream = p.open(
                    format=pyaudio.paInt16, 
                    channels=1, 
                    rate=16000, 
                    output=True
                )

                # Initialize the WAV header
                wav_header = None

                for audio_chunk in byte_stream_generator(response=response):
                    # Check if this is the first chunk (WAV header)
                    if wav_header is None:
                        wav_header = audio_chunk
                        # Extract the WAV format parameters from the header
                        wav_format = wave.open(io.BytesIO(wav_header), 'rb')
                        channels, samp_width, framerate, nframes, comptype, compname = wav_format.getparams()
                        # Reopen the stream with the correct parameters
                        stream = p.open(
                            format=p.get_format_from_width(samp_width), 
                            channels=channels, 
                            rate=framerate, 
                            output=True
                        )
                    else:
                        # Write the audio chunk to the stream
                        stream.write(audio_chunk)

                # Close the stream and PyAudio
                stream.stop_stream()
                stream.close()
                p.terminate()

            except Exception as e:
                print(f"Error during playback: {e}")
        
        # IPython.display.Audio(speech_file_path)
        # os.remove(speech_file_path)

    def run(self):
        while True:
            text = self.listen()
            if not text:
                continue
            bot_text_response = self.process_text()
            
            self.speak(bot_text_response)
            # break
            # inp = input("\nPress Enter to continue, q/quit/stop to quit...\n")
            # if inp in ['q', 'quit', 'stop']:
            #     break


if __name__ == "__main__":
    load_dotenv()
    bot = SpeechBot(AUDIO_HANDLING_PROMPT_2)
    bot.run()