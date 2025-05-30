import subprocess
import os
import shutil
import concurrent.futures
from utils import mkdir_path

checkpoint_path = "./fish-speech-1.5/firefly-gan-vq-fsq-8x1024-21hz-generator.pth"
model_path = "./fish-speech-1.5"

def text_to_npy(text, npy_dir):
    script_path = "fish-speech/fish_speech/models/text2semantic/inference.py"
    device = "cpu"
    args = [
        "--text", text,
        "--checkpoint-path", model_path,
        "--device", device, 
        "--output-dir", npy_dir,
        "--half",
        "--compile", 
    ]
    command = ["python", script_path] + args
    subprocess.run(command, check=True)

def npy_to_audio(npy_dir, output_file):
    script_path = "fish-speech/fish_speech/models/vqgan/inference.py"
    device = "cpu"
    args = [
        "--input-path", npy_dir + "/codes_0.npy", 
        "--checkpoint-path", checkpoint_path,
        "--device", device,
        "--output-path", output_file, 
        "--compile", 
        "--half",
    ]
    command = ["python", script_path] + args
    subprocess.run(command, check=True)

def text_to_audio(text, audio_path, index):
    index += 10000
    npy_dir = f"./temp_npy_{index}"
    audio_file = f"{audio_path}/audio_{index}.wav"
    mkdir_path(npy_dir)
    text_to_npy(text, npy_dir)
    npy_to_audio(npy_dir, audio_file)
    return True

def fish_process_all_text_to_audio(datas, audio_path):
    mkdir_path(audio_path)

    MAX_WORKERS = 3
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(text_to_audio, data, audio_path, index): index for index, data in enumerate(datas)}
        for future in concurrent.futures.as_completed(future_to_url):
            index = future_to_url[future]
            try:
                result = future.result() # 获取任务执行结果
            except Exception as exc:
                print(f"[任务 {index}] 错误: {exc}")

