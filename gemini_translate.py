import json 
from google import genai
from google.genai import types
import os 

def translate_single(client, systemp_prompt, user_input, max_attempts = 50):
    attempt_count = 0
    delay = 1
    while attempt_count < max_attempts:
        attempt_count += 1
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    system_instruction=systemp_prompt),
                contents=user_input
            )
            # print(f"###{response.text}###\n\n")
            return response.text
        except Exception as e:
            delay *= 2
            print(
                f"Translation failed due to {type(e).__name__}: {e} Will sleep {delay} seconds"
            )
            time.sleep(delay)


def translate_text(day, api_key):
    client = genai.Client(api_key=api_key)
    prompt = json.load(open('./prompt/translate.json', 'r', encoding='utf-8'))
    systemp_prompt = prompt['system']

    path = day
    outputs = []
    flag = False
    for filename in sorted(os.listdir(path)):
        if not filename.endswith("original.txt"): continue
        text_file = os.path.join(path, filename)
        translated_file = text_file.replace("original", "translated")
        if os.path.exists(translated_file):
            print (f"{translated_file} exists")
            continue

        data = open(text_file, 'r', encoding='utf-8').read()
        title = data.split("\n")[0]
        content = "\n".join(data.split("\n")[1:]).strip("\n")

        user_input = prompt['user'].format(text = title)
        translated_title = translate_single(client, systemp_prompt, user_input)
        translated_title = translated_title.replace("\n", ". ")

        user_input = prompt['user'].format(text = content)
        translated_content = translate_single(client, systemp_prompt, user_input)
        
        flag = True
        with open(translated_file, 'w', encoding='utf-8') as f:
            f.write(f"{translated_title}\n\n{translated_content}")
    return flag
