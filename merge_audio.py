import soundfile as sf
import numpy as np
import os

def merge_sorted_audio_files(audio_folder, output_path):
    audio_files = []
    for root, _, files in os.walk(audio_folder):
        for file in files:
            if file.endswith(".wav"):
                audio_files.append(os.path.join(root, file))

    if not audio_files:
        print(f"No WAV files found in {audio_folder}. Nothing to merge.")
        return

    # 按文件名排序
    audio_files.sort()
    print (f"audio_files_sorted: {audio_files}")

    all_audio_data = []
    print(f"Merging {len(audio_files)} audio files from {audio_folder}...")

    sample_rate = None
    for i, path in enumerate(audio_files):
        try:
            print(f"file size {path}: {os.path.getsize(path)}")
            data, sr = sf.read(path)
            if sample_rate is None:
                sample_rate = sr
                silence_duration_seconds = 2
                silence_samples = int(silence_duration_seconds * sample_rate)
                silence_data = np.zeros(silence_samples, dtype=np.float32)
            if sr != sample_rate:
                print(f"Warning: Sample rate mismatch for {path}. Expected {sample_rate}, got {sr}. This might lead to unexpected results.")
            
            # 确保是单声道。如果读取到多声道，我们会尝试将其转换为单声道（取第一个声道）
            if data.ndim > 1:
                print(f"Warning: {path} is multi-channel. Converting to mono by taking the first channel.")
                data = data[:, 0] # 取第一个声道

            all_audio_data.append(data)
            print(f"  [{i+1}/{len(audio_files)}] Loaded: {os.path.basename(path)}")
            if i < len(audio_files) - 1:
                all_audio_data.append(silence_data)
                print(f"  [{i+1}/{len(audio_files)}] Loaded: {os.path.basename(path)} and added {silence_duration_seconds}s silence.")
            else:
                print(f"  [{i+1}/{len(audio_files)}] Loaded: {os.path.basename(path)} (last file, no silence added after).")
        except Exception as e:
            print(f"Error reading {path}: {e}")
            continue

    if not all_audio_data:
        print("No valid audio data was loaded. Aborting merge.")
        return
    
    print (f"sample_rate: {sample_rate}")
    # 沿着轴 0 连接所有音频数据
    merged_audio = np.concatenate(all_audio_data, axis=0)

    # 保存合并后的音频文件
    sf.write(output_path, merged_audio, sample_rate)
    print(f"\nSuccessfully merged audio to {output_path}")
    print(f"output_path size: {os.path.getsize(output_path)}")

# --- 示例用法 ---
if __name__ == "__main__":
    # 1. 定义音频文件所在的文件夹
    audio_directory = "temp_audio"
    
    # 2. 定义合并后输出的文件路径
    output_merged_file = "final_merged_audio.wav"
    
    # 3. 定义音频文件的采样率（请确保所有输入文件都具有相同的采样率）
    # 如果您不确定，可以从其中一个文件读取，例如：

    # --- 调用合并函数 ---
    merge_sorted_audio_files(audio_directory, output_merged_file)

