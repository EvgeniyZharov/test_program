import subprocess
import os
import re

def get_volume_stats(input_path):
    """
    Выполняет анализ громкости через volumedetect и возвращает max_volume (в dB).
    """
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-af', 'volumedetect',
        '-f', 'null',
        '-'
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = result.stdout

    match = re.search(r'max_volume: ([\-\d\.]+) dB', output)
    if match:
        return float(match.group(1))
    else:
        print("⚠️  Не удалось определить max_volume")
        return 0.0  # по умолчанию — не усиливать

def denoise_audio(input_path):
    out_path = input_path
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Файл не найден: {input_path}")

    # Анализируем громкость
    max_volume = get_volume_stats(input_path)
    print(f"[i] Обнаруженная максимальная громкость: {max_volume} dB")

    # Вычисляем необходимое усиление, если max_volume < -1.5 dB
    gain = 0.0
    target_peak = -1.5
    if max_volume < target_peak:
        gain = target_peak - max_volume
        print(f"[i] Применим усиление на {gain:.2f} dB")
    else:
        print("[i] Усиление не требуется")

    # Сборка фильтров
    filter_chain = [
        'highpass=f=200',
        'lowpass=f=3000',
        'afftdn=nf=-25',
        f'volume={gain:.2f}dB' if gain > 0 else None,
        'dynaudnorm=f=250:g=5',
        'loudnorm=I=-16:LRA=11:TP=-1.5'
    ]
    filters = ','.join(filter for filter in filter_chain if filter)

    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-af', filters,
        '-ar', '16000',
        '-ac', '1',
        '-y',
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"[✓] Аудио успешно обработано: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"[✗] Ошибка при выполнении ffmpeg: {e}")

# Пример использования
if __name__ == "__main__":
    input_audio = 'noisy_output.wav'
    denoise_audio(input_audio)
