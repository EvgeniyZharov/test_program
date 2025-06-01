import subprocess
import os
from pydub import AudioSegment

def denoise_audio(input_path, output_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Файл не найден: {input_path}")

    # FFmpeg фильтры: шумоподавление, частотная фильтрация, нормализация
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-af', 'highpass=f=200, lowpass=f=3000, afftdn=nf=-25, dynaudnorm',
        '-ar', '16000',  # частота дискретизации
        '-ac', '1',       # моно
        '-y',             # перезаписать выход
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"[✓] Аудио успешно обработано: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"[✗] Ошибка при выполнении ffmpeg: {e}")

# Пример использования
input_audio = 'file_music.wav'
output_audio = 'processed_output.wav'

denoise_audio(input_audio, output_audio)
