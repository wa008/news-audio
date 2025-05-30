import subprocess
import os
import shutil
import concurrent.futures
import json 
from google import genai
from google.genai import types
import wave 
import time
from utils import mkdir_path

# Set up the wave file to save the output:
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
   with wave.open(filename, "wb") as wf:
      wf.setnchannels(channels)
      wf.setsampwidth(sample_width)
      wf.setframerate(rate)
      wf.writeframes(pcm)

def gemini_tts(client, user_input, output_file, max_attempts = 1):
    attempt_count = 0
    delay = 1
    while attempt_count < max_attempts:
        attempt_count += 1
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents="This is a dog",
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name='Kore',
                        )
                    )
                ),
            )
        )
        data = response.candidates[0].content.parts[0].inline_data.data
        wave_file(output_file, data) # Saves the file to current directory
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=user_input,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name='Kore',
                            )
                        )
                    ),
                )
            )
            data = response.candidates[0].content.parts[0].inline_data.data
            wave_file(output_file, data) # Saves the file to current directory
        except Exception as e:
            delay *= 2
            print(
                f"Translation failed due to {type(e).__name__}: {e} Will sleep {delay} seconds"
            )
            time.sleep(delay)


def gemini_process_all_text_to_audio(datas, audio_path, api_key = 'default'):
    mkdir_path(audio_path)
    client = genai.Client(api_key = api_key)
    for index, data in enumerate(datas):
        output_file = os.path.join(audio_path, f"audio_{index}.wav")
        gemini_tts(client, data, output_file)
        break 