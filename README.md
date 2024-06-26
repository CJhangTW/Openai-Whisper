# Openai-Whisper

使用Openai-Whisper套件, 將語音檔案轉成文字稿.

## 環境設定

### 新增虛擬機

`py -m venv venv`

### 啟用虛擬工作環境

`.\venv\Scripts\activate`

升級pip套件
`py -m pip install --upgrade pip`

列出所有已安裝套件
`pip freeze`

常見相依性套件安裝方法
`pip install -r requirements.txt`

相依性套件輸出
`pip freeze > requirements.txt`

更新你的虛擬環境中的套件, 也可以使用
`pip install -r requirements.txt --upgrade`

### 安裝 Whisper

安裝 Whisper 已被包在requirements.txt當中
不需要特別使用`pip install openai-whisper`

## 使用方式

### 使用 whisper

編輯定義音訊檔案和目錄

```
audio_file = '錄製.m4a'
mins = 10 # 單位:分鐘
model_setting = "large" # 您可以選擇不同大小的模型，例如 "small", "medium", "large", "base"
```

後

終端機 執行 `py .\App.py`

---

## 未來版本

### 更新內文

新增可辨識時間的內容段落



