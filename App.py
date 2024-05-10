import logging
from pydub import AudioSegment
import whisper
import os
import shutil
from datetime import datetime

# 定義音訊檔案和目錄
audio_file = '錄製.m4a'
mins = 10 # 單位:分鐘
model_setting = "large" # 您可以選擇不同大小的模型，例如 "small", "medium", "large", "base"

# 設定日誌記錄
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 檢查並建立目錄的函數
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

def clean_up_chunks(directory):
    try:
        shutil.rmtree(directory)
        logging.info(f"Deleted directory: {directory}")
    except Exception as e:
        logging.error(f"Error deleting directory {directory}: {e}")

# 建立目錄
audio_files_directory = 'audio_files'
chunk_directory = 'chunks'
output_directory = 'output'
ensure_directory_exists(audio_files_directory)
ensure_directory_exists(chunk_directory)
ensure_directory_exists(output_directory)

# 確定完整的音訊檔案路徑
full_audio_path = os.path.join(audio_files_directory, audio_file)

# 載入和分割音訊文件
audio = AudioSegment.from_file(full_audio_path)
chunk_length_ms = mins * 60 * 1000  # 分鐘
for i in range(0, len(audio), chunk_length_ms):
    chunk = audio[i:i+chunk_length_ms]
    chunk_path = os.path.join(chunk_directory, f"chunk_{i//chunk_length_ms}.wav")
    chunk.export(chunk_path, format="wav")

# 載入 Whisper 模型
model = whisper.load_model(model_setting)  # 您可以選擇不同大小的模型，例如 "small", "medium", "large", "base"

# 取得不含副檔名的音訊檔案名稱用作輸出檔案前綴
audio_file_prefix = os.path.splitext(audio_file)[0]

# 取得當前時間並格式化為字串，適合檔案名
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

# 處理每個音訊片段並將結果寫入文件
output_path = os.path.join(output_directory, f"{audio_file_prefix}_result_{model_setting}_{current_time}.txt")
with open(output_path, 'w', encoding='utf-8') as file:
    for chunk_file in sorted(os.listdir(chunk_directory)):
        if chunk_file.endswith(".wav"):
            chunk_path = os.path.join(chunk_directory, chunk_file)
            print(f"Processing {chunk_file}...")
            result = model.transcribe(chunk_path)
            print(result["text"])
            file.write(result["text"] + "\n\n")

# 腳本結束後清理chunks目錄
clean_up_chunks(chunk_directory)