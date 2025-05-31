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
from tts_chatts import chattts_process_all_text_to_audio
from merge_audio import merge_sorted_audio_files
from generate_rss_xml import create_rss_feed
# python 

def main():
    api_key = sys.argv[1]
    flag, day, epub_file = download_latest_doc()
    # flag, day, epub_file = True, "2025-05-24", "./temp_epub.epub"
    print (f"flag: {flag}")
    print (f"epub_file: {epub_file}")
    print (f"day: {day}")
    if flag == False: 
        return 
    
    path = f"the_economist/{day}"
    parsed_content = parse_epub(epub_file, path)
    
    res = translate_text(path, api_key)
    if res == True: return 

    chattts_process_all_text_to_audio(path)

    # auto generate rss.xml 
    create_rss_feed(path, "rss.xml")

if __name__ == "__main__":
    for i in range(1):
        main()

