import re
from download_latest_doc import download_latest_doc
from gemini_translate import translate_text
from parse_epub import parse_epub
# python 


def main():
    # flag, epub_file, text_file = download_latest_doc()
    flag, epub_file, text_file = True, "./local_file.epub", "./the_economist/2025-04-26-parse.txt"
    print (f"flag: {flag}")
    print (f"epub_file: {epub_file}")
    print (f"text_file: {text_file}")
    if flag == False: 
        return 

    # parsed_content = parse_epub(epub_file, text_file)
    
    translated_file = text_file.replace("parse", "translated")
    translate_text(text_file, translated_file)


if __name__ == "__main__":
    for i in range(1):
        main()

