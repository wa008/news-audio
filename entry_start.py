import re 
from download_latest_doc import download_latest_doc
from gemini_translate import translate_text
from parse_epub import parse_epub
import sys 
import subprocess
import os
from utils import mkdir_path
from tts_fishspeech import fish_process_all_text_to_audio
from tts_gemini import gemini_process_all_text_to_audio # Doesn't support till now, to finish
from merge_audio import merge_sorted_audio_files
# python 

def main():
    api_key = sys.argv[1]
    # flag, day, epub_file = download_latest_doc()
    flag, day, epub_file = True, "2025-05-24", "./temp_epub.epub"
    print (f"flag: {flag}")
    print (f"epub_file: {epub_file}")
    print (f"day: {day}")
    if flag == False: 
        return 

    parsed_content = parse_epub(epub_file, day)
    
    # res = translate_text(day, api_key)
    res = False
    if res == True: return 

    fish_process_all_text_to_audio(day)

if __name__ == "__main__":
    for i in range(1):
        main()

