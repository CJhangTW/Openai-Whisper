import logging
from pydub import AudioSegment
import whisper
import os
from datetime import datetime

# 定义音频文件和目录
audio_file = 'SHMeet.m4a'
mins = 10
model_setting = "large" # 您可以选择不同大小的模型，如 "small", "medium", "large", "base"

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 检查并创建目录的函数
def ensure_directory_exists(directory_name):
    try:
        if not os.path.exists(directory_name):
            os.makedirs(directory_name, exist_ok=True)
            logging.info(f"Created directory: {directory_name}")
        else:
            logging.info(f"Directory already exists: {directory_name}")
    except Exception as e:
        logging.error(f"Error creating directory {directory_name}: {e}")
        raise

# 创建目录
audio_files_directory = 'audio_files'
chunk_directory = 'chunks'
output_directory = 'output'
ensure_directory_exists(audio_files_directory)
ensure_directory_exists(chunk_directory)
ensure_directory_exists(output_directory)

# 确定完整的音频文件路径
full_audio_path = os.path.join(audio_files_directory, audio_file)

# 加载和分割音频文件
audio = AudioSegment.from_file(full_audio_path)
chunk_length_ms = mins * 60 * 1000  # 分钟
for i in range(0, len(audio), chunk_length_ms):
    chunk = audio[i:i+chunk_length_ms]
    chunk_path = os.path.join(chunk_directory, f"chunk_{i//chunk_length_ms}.wav")
    chunk.export(chunk_path, format="wav")

# 加载 Whisper 模型
model = whisper.load_model(model_setting)  # 您可以选择不同大小的模型，如 "small", "medium", "large", "base"

# 获取不带扩展名的音频文件名用作输出文件前缀
audio_file_prefix = os.path.splitext(audio_file)[0]

# 获取当前时间并格式化为字符串，适合文件名
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

# 处理每个音频片段并将结果写入文件
output_path = os.path.join(output_directory, f"{audio_file_prefix}_result_{current_time}.txt")
with open(output_path, 'w', encoding='utf-8') as file:
    for chunk_file in sorted(os.listdir(chunk_directory)):
        if chunk_file.endswith(".wav"):
            chunk_path = os.path.join(chunk_directory, chunk_file)
            print(f"Processing {chunk_file}...")
            result = model.transcribe(chunk_path)
            print(result["text"])
            file.write(result["text"] + "\n\n")
