import json 
from google import genai
from google.genai import types

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


def translate_text(text_file, translated_file, api_key):
    client = genai.Client(api_key=api_key)
    prompt = json.load(open('./prompt/translate.json', 'r', encoding='utf-8'))
    systemp_prompt = prompt['system']

    datas = open(text_file, 'r', encoding='utf-8').read().split("\n\n" + "-" * 50 + "\n\n")
    outputs = []
    for data in datas:
        title = data.split("\n")[0]
        content = "\n".join(data.split("\n")[1:]).strip("\n")

        user_input = prompt['user'].format(text = title)
        translated_title = translate_single(client, systemp_prompt, user_input)

        user_input = prompt['user'].format(text = content)
        translated_content = translate_single(client, systemp_prompt, user_input)
        outputs.append(f"{translated_title}\n{translated_content}")

    with open(translated_file, 'w', encoding='utf-8') as f:
        f.write(("\n\n" + "-" * 50 + "\n\n").join(outputs))
