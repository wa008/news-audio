import subprocess
import os
import shutil
import concurrent.futures
import json 
from google import genai
from google.genai import types
import wave 
import time
import sys
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
        try:
            contents = "Read this in chinese: ${user_input}"
            MODEL_ID = "gemini-2.5-flash-preview-tts"
            response = client.models.generate_content(
                model=MODEL_ID,
                contents = contents,
                config={"response_modalities": ['Audio']},
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

if __name__ == "__main__":
    # Example
    datas = ["Say cheerfully: Have a wonderful day!"]
    audio_path = "tmp_audio_output"
    api_key = sys.argv[1] if len(sys.argv) > 1 else 'default'
    gemini_process_all_text_to_audio(datas, audio_path, api_key)
