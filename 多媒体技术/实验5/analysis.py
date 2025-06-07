# 使用 Python 分析 WAV 文件头
import wave

with wave.open('record01.wav', 'rb') as wav_file:
    channels = wav_file.getnchannels()
    sample_rate = wav_file.getframerate()
    sample_width = wav_file.getsampwidth() * 8  # 转换为位
    print(f"声道数: {channels}")
    print(f"采样频率: {sample_rate} Hz")
    print(f"样本精度: {sample_width} 位")