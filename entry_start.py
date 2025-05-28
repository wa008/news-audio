import re
from download_latest_doc import download_latest_doc
from gemini_translate import translate_text
from parse_epub import parse_epub
import sys 
import subprocess
import os
# python 

checkpoint_path = "/root/.cache/modelscope/hub/models/fishaudio/fish-speech-1.5/firefly-gan-vq-fsq-8x1024-21hz-generator.pth"
model_path = "/root/.cache/modelscope/hub/models/fishaudio/fish-speech-1.5"

def text_to_audio(text, audio_file):
    npy_dir = "./temp_npy"
    text_to_npy(model_path, text, npy_dir)
    npy_to_audio(checkpoint_path, npy_dir, audio_file)

def main():
    api_key = sys.argv[1]
    # flag, epub_file, text_file = download_latest_doc()
    flag, epub_file, text_file = True, "./local_file.epub", "./the_economist/2025-05-24-parse.txt"
    print (f"flag: {flag}")
    print (f"epub_file: {epub_file}")
    print (f"text_file: {text_file}")
    if flag == False: 
        return 

    # parsed_content = parse_epub(epub_file, text_file)
    
    translated_file = text_file.replace("parse", "translated")
    # translate_text(text_file, translated_file, api_key)

    datas = open(translated_file, 'r').read().split("\n\n" + "-" * 50 + "\n\n")
    index = 10000
    for data in datas:
        index += 1
        # title = data.split("\n")[0]
        # content = "\n".join(data.split("\n")[1: ])
        audio_file = f"./audio_{index}.wav"
        text_to_audio(data, audio_file)


if __name__ == "__main__":
    for i in range(3):
        main()


