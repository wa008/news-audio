import subprocess
import os


def text_to_npy(model_path, text, npy_dir):
    script_path = "fish-speech/fish_speech/models/text2semantic/inference.py"
    args = [
        "--text", text,
        "--checkpoint-path", model_path,
        "--output-dir", npy_dir,
    ]
    command = ["python", script_path] + args
    subprocess.run(command, check=True)

def npy_to_audio(checkpoint_path, npy_dir, output_file):
    script_path = "fish-speech/fish_speech/models/vqgan/inference.py"
    device = "cpu"
    args = [
        "--input-path", npy_dir + "/codes_0.npy", 
        "--checkpoint-path", checkpoint_path,
        "--device", device,
        "--output-path", output_file
    ]
    command = ["python", script_path] + args
    subprocess.run(command, check=True)

