import subprocess
import os

checkpoint_path = "/root/.cache/modelscope/hub/models/fishaudio/fish-speech-1.5/firefly-gan-vq-fsq-8x1024-21hz-generator.pth"
device = "cpu"
npy_dir = "./npy"

def text_to_npy():
    model_path = "/root/.cache/modelscope/hub/models/fishaudio/fish-speech-1.5"
    text = "4月30日，一项衡量新出口订单的指标跌至2022年以来的最低水平。"
    
    script_path = "fish-speech/fish_speech/models/text2semantic/inference.py"
    args = [
        "--text", text,
        "--checkpoint-path", model_path,
        "--output-dir", npy_dir,
    ]
    command = ["python", script_path] + args
    subprocess.run(command, check=True)

def npy_to_audio():

    script_path = "fish-speech/fish_speech/models/vqgan/inference.py"
    args = [
        "--input-path", npy_dir + "/codes_0.npy", 
        "--checkpoint-path", checkpoint_path,
        "--device", device,
    ]
    command = ["python", script_path] + args
    subprocess.run(command, check=True)

text_to_npy()
npy_to_audio()
