import subprocess
import os
import shutil
import concurrent.futures

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

def mkdir_path(directory_path):
    # Check if the path exists and is a directory
    if os.path.isdir(directory_path):
        try:
            # ⚠️ Be very careful with shutil.rmtree()!
            # confirm = input(f"Are you absolutely sure you want to delete '{directory_path}' and all its contents? (yes/no): ")
            # if confirm.lower() == 'yes':
            shutil.rmtree(directory_path)
            print(f"Directory '{directory_path}' and its contents removed successfully.")
            # else:
            #     print("Deletion cancelled.")
        except OSError as e:
            print(f"Error removing directory '{directory_path}': {e.strerror}")
            print("This could be due to permission issues or files being in use.")
    elif os.path.exists(directory_path):
        # Path exists but is not a directory (it's a file)
        os.remove(file_path)
        print(f"Error: '{directory_path}' exists but is a file, not a directory. `shutil.rmtree` is for directories.")
    else:
        print(f"Directory '{directory_path}' does not exist.")
    os.mkdir(directory_path)

def text_to_audio(text, audio_path, index):
    index += 10000
    npy_dir = f"./temp_npy_{index}"
    audio_file = f"{audio_path}/audio_{index}.wav"
    mkdir_path(npy_dir)
    text_to_npy(text, npy_dir)
    npy_to_audio(npy_dir, audio_file)
    return True

def process_all_text_to_audio(datas, audio_path):
    mkdir_path(audio_path)

    MAX_WORKERS = 10
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(text_to_audio, data, audio_path, index): index for index, data in enumerate(datas)}
        for future in concurrent.futures.as_completed(future_to_url):
            index = future_to_url[future]
            try:
                result = future.result() # 获取任务执行结果
            except Exception as exc:
                print(f"[任务 {index}] 错误: {exc}")

