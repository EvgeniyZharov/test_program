import numpy as np
from pydub import AudioSegment
import soundfile as sf


def add_white_noise(input_path, output_path, noise_level_db=-20):
    """
    Добавляет белый шум к аудиофайлу.

    :param input_path: путь к исходному .wav файлу
    :param output_path: путь к выходному файлу
    :param noise_level_db: уровень шума в децибелах относительно полной шкалы
    """
    # Загружаем аудио через pydub
    audio = AudioSegment.from_file(input_path, format="wav")

    # Конвертируем в numpy массив
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    if audio.channels == 2:
        samples = samples.reshape((-1, 2))

    # Генерация белого шума той же длины и амплитуды
    noise = np.random.normal(0, 1, samples.shape)

    # Приведение уровня шума к заданному dB
    rms_audio = np.sqrt(np.mean(samples ** 2))
    rms_noise = np.sqrt(np.mean(noise ** 2))
    desired_rms_noise = rms_audio * (10 ** (noise_level_db / 20))
    noise = noise * (desired_rms_noise / rms_noise)

    # Суммируем сигнал и шум
    noisy_samples = samples + noise

    # Ограничиваем по int16
    noisy_samples = np.clip(noisy_samples, -32768, 32767).astype(np.int16)

    # Сохраняем в файл
    sf.write(output_path, noisy_samples, audio.frame_rate)
    print(f"[✓] Шум добавлен: {output_path}")


# Пример использования:
# Добавим -15 dB белого шума
add_white_noise("audio_1.wav", "noisy_output.wav", noise_level_db=-15)
