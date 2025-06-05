from pydub import AudioSegment
import numpy as np
import os
import random
import tempfile


def generate_white_noise(duration_ms, sample_rate=16000, volume_db=-30):
    num_samples = int(sample_rate * (duration_ms / 1000.0))
    noise = np.random.normal(0, 1, num_samples)
    # Нормализуем шум и уменьшаем по громкости
    noise = noise / np.max(np.abs(noise)) * (10 ** (volume_db / 20))
    audio_bytes = (noise * 32767).astype(np.int16).tobytes()

    return AudioSegment(
        audio_bytes,
        frame_rate=sample_rate,
        sample_width=2,
        channels=1
    )


def distort_audio(input_path: str, output_path: str):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Файл не найден: {input_path}")

    audio = AudioSegment.from_file(input_path).set_channels(1).set_frame_rate(16000)
    duration_ms = len(audio)

    # 1. Добавим белый шум
    noise = generate_white_noise(duration_ms, volume_db=-28)
    audio_with_noise = audio.overlay(noise)

    # 2. Сделаем громкость "скачкообразной"
    chunk_ms = 500  # каждые 0.5 сек
    chunks = []
    for i in range(0, len(audio_with_noise), chunk_ms):
        chunk = audio_with_noise[i:i + chunk_ms]
        db_change = random.uniform(-12, 6)  # хаотично ослабим/усилим
        chunk = chunk + db_change
        chunks.append(chunk)

    glitched = sum(chunks)

    # 3. Low-pass фильтр — имитируем "гул"
    glitched = glitched.low_pass_filter(2800)

    glitched.export(output_path, format='wav')
    print(f"[✓] Искажённое аудио сохранено: {output_path}")


# Пример использования
if __name__ == "__main__":
    distort_audio("audio_1.wav", "distorted.wav")
