import subprocess
import os
import shutil
import concurrent.futures
from utils import mkdir_path
from merge_audio import merge_sorted_audio_files
import torch
import torchaudio
import ChatTTS
import traceback

def text_to_audio(text, audio_path, index):
    print (f"process text: {text}")
    index += 10000
    chat = ChatTTS.Chat()
    chat.load(compile=True, source="custom", custom_path="./ChatTTS-model", device = 'cpu')
    spk = torch.load("./seed_1397_restored_emb.pt", map_location=torch.device('cpu'))
    params_infer_code = ChatTTS.Chat.InferCodeParams(
        spk_emb = spk, # add sampled speaker
        temperature = 0.3,   # using custom temperature
        top_P = 0.7,        # top P decode
        top_K = 20,         # top K decode
    )
    params_refine_text = ChatTTS.Chat.RefineTextParams(
        prompt='[oral_2][laugh_0][break_6]',
    )

    torch.manual_seed(42) # text seed 
    wavs = chat.infer(text, skip_refine_text=True, params_refine_text=params_refine_text, params_infer_code=params_infer_code)
    if not isinstance(wavs, list):
        wavs = [wavs]
    audio_file = f"{audio_path}/{index}.wav"
    torchaudio.save(audio_file, torch.from_numpy(wavs[0]).unsqueeze(0), 24000)


def chattts_process_all_text_to_audio(path):
    flag = False
    for filename in sorted(os.listdir(path)):
        if not filename.endswith("translated.txt"): continue
        translated_file = os.path.join(path, filename)
        audio_file = translated_file.replace("translated.txt", "audio.wav")
        if os.path.exists(audio_file):
            print (f"{audio_file} exists")
            continue
        text = open(translated_file, 'r').read()
        flag = True
        tts_one_file(text, audio_file)
        audio_path = "/".join(audio_file.split("/")[:-1])
        index = int(audio_file.split("/")[-1].split("-")[0]) - 10000
        # print (audio_path, index)
        # text = "This is a dog"
        # text_to_audio(text, audio_path, index)
        break
    if flag == False:
        done_file = f"{path}/done"
        with open(done_file, 'w') as f:
            pass
        print (f"Creat done file {done_file}")

def tts_one_file(text, audio_file):
    print (f"process audio_file: {audio_file}")
    datas = text.split("\n")
    datas = [x.strip().strip("\n") for x in datas]
    datas = [x for x in datas if len(x) > 3]
    audio_path = "./temp_audio"
    mkdir_path(audio_path)

    chunk_size = 50
    res = [datas[0]]
    for i, data in enumerate(datas):
        if i == 0: continue
        if len(data) > chunk_size:
            tmp = data.split("。")
            cur = tmp[0] + "。"
            for ind, val in enumerate(tmp):
                if ind == 0: continue
                if len(val) <= 2: continue
                if len(cur) + len(val) < chunk_size:
                    cur += val + "。"
                else:
                    res.append(cur.strip())
                    cur = val + "。"
            if len(cur) > 2:
                res.append(cur.strip())
        else:
            res.append(data)
    datas = res 
    print (f"count: {len(datas)}")

    MAX_WORKERS = 1
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(text_to_audio, data, audio_path, index): data for index, data in enumerate(datas)}
        for future in concurrent.futures.as_completed(future_to_url):
            res = future_to_url[future]
            try:
                result = future.result()
            except Exception as exc:
                print(f"[task {res}] error: {exc}")

    merge_sorted_audio_files(audio_path, audio_file)

if __name__ == "__main__":
    chattts_process_all_text_to_audio("the_economist/2025-05-24")
