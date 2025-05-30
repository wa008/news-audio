import re 
from download_latest_doc import download_latest_doc
from gemini_translate import translate_text
from parse_epub import parse_epub
import sys 
import subprocess
import os
from utils import mkdir_path
from tts_fishspeech import fish_process_all_text_to_audio
from tts_gemini import gemini_process_all_text_to_audio
from merge_audio import merge_sorted_audio_files
# python 

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
    audio_path = './temp_audio'
    fish_process_all_text_to_audio(datas, audio_path)

    final_audio_file = "merged_audio_file.wav"
    merge_sorted_audio_files(audio_path, final_audio_file)

if __name__ == "__main__":
    for i in range(1):
        main()

