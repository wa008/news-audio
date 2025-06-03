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

def gemini_tts(client, user_input, output_file, max_attempts = 11):
    attempt_count = 0
    delay = 1
    while attempt_count < max_attempts:
        attempt_count += 1
        try:
            contents = f"Read this in chinese: \n\n{user_input}"
            print (f"contents: {contents}")
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

def gemini_process_all_text_to_audio(path, api_key = 'default'):
    flag = False
    client = genai.Client(api_key = api_key)
    for filename in sorted(os.listdir(path)):
        if not filename.endswith("translated.txt"): continue
        translated_file = os.path.join(path, filename)
        audio_file = translated_file.replace("translated.txt", "audio.wav")
        if os.path.exists(audio_file):
            print (f"{audio_file} exists")
            continue
        text = open(translated_file, 'r').read()
        flag = True
        gemini_tts(client, text, audio_file)
        break
    if flag == False:
        done_file = f"{path}/done"
        with open(done_file, 'w') as f:
            pass
        print (f"Creat done file {done_file}")

if __name__ == "__main__":
    # Example
    path = "./the_economist/2025-05-31"
    api_key = sys.argv[1] if len(sys.argv) > 1 else 'default'
    gemini_process_all_text_to_audio(path, api_key)
