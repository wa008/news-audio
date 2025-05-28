import json 
from google import genai
from google.genai import types


def translate_single(client, systemp_prompt, user_input):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=systemp_prompt),
        contents=user_input
    )
    print(f"###{response.text}###")


def translate_text(text_file, translated_file):
    client = genai.Client(api_key="")

    prompt = json.load(open('./prompt/translate.json', 'r', encoding='utf-8'))
    user_input = prompt['user'].format(text = "This is a dog")
    systemp_prompt = prompt['system']
    print (f"user_input: {user_input}")
    print (f"system_prompt: {systemp_prompt}")
    translate_single(client, systemp_prompt, user_input)
