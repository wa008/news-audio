import subprocess
import os
import shutil
import concurrent.futures
from utils import mkdir_path
from merge_audio import merge_sorted_audio_files
import ChatTTS
import torch
import torchaudio

def text_to_audio(text, audio_path, index):
    index += 10000
    text = "在经历了11周的全面封锁后，在来自美国的压力下，以色列宣布将允许少量食品进入加沙。"
    chat = ChatTTS.Chat()
    chat.load(compile=True, source="custom", custom_path="./ChatTTS", device = 'cpu')

    rand_spk = chat.sample_random_speaker()
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
    wavs = chat.infer(text, skip_refine_text=True, params_refine_text=params_refine_text,  params_infer_code=params_infer_code)
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
        break
    if flag == False:
        done_file = f"{path}/done"
        with open(done_file, 'w') as f:
            pass
        print (f"Creat done file {done_file}")

def tts_one_file(text, audio_file):
    datas = text.split("\n")
    datas = [x.strip().strip("\n") for x in datas]
    datas = [x for x in datas if len(x) > 3]
    audio_path = "./temp_audio"
    mkdir_path(audio_path)
    print (f"count: {len(datas)}")
    MAX_WORKERS = 3
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(text_to_audio, data, audio_path, index): index for index, data in enumerate(datas)}
        for future in concurrent.futures.as_completed(future_to_url):
            index = future_to_url[future]
            try:
                result = future.result() # 获取任务执行结果
            except Exception as exc:
                print(f"[任务 {index}] 错误: {exc}")
    merge_sorted_audio_files(audio_path, audio_file)

chattts_process_all_text_to_audio("the_economist/2025-05-24")
