import numpy as np
import librosa
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import correlate


def calculate_snr(y):
    # Найдём участки с речью
    intervals = librosa.effects.split(y)

    # Собираем только участки с речью
    y_speech = librosa.effects.remix(y, intervals)

    # Приводим к одинаковой длине
    min_len = min(len(y), len(y_speech))
    y = y[:min_len]
    y_speech = y_speech[:min_len]

    # Предполагаемый шум = разница между оригиналом и "речевыми" участками
    noise_estimate = y - y_speech

    signal_power = np.mean(y_speech ** 2)
    noise_power = np.mean(noise_estimate ** 2)

    snr = 10 * np.log10(signal_power / (noise_power + 1e-10))
    return snr


def spectral_flatness(y, sr):
    S = np.abs(librosa.stft(y))
    flatness = librosa.feature.spectral_flatness(S=S)
    return np.mean(flatness)


def estimate_echo(y, sr, min_delay_ms=50, threshold_ratio=0.2):
    autocorr = correlate(y, y, mode='full')
    autocorr = autocorr[len(autocorr) // 2:]  # только положительные задержки

    min_samples = int(sr * (min_delay_ms / 1000.0))

    main_peak = autocorr[0]
    search_area = autocorr[min_samples:]

    peak_value = np.max(search_area)
    peak_index = np.argmax(search_area) + min_samples

    if peak_value > main_peak * threshold_ratio:
        echo_delay_time = peak_index / sr
    else:
        echo_delay_time = 0.0  # эхо не выражено

    return echo_delay_time, autocorr


def analyze_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)

    snr_value = calculate_snr(y)
    flatness_value = spectral_flatness(y, sr)
    echo_delay, autocorr = estimate_echo(y, sr)

    print(f"[📊] Результаты анализа '{file_path}':")
    # print(f" - Оценка SNR (соотношение сигнал/шум): {snr_value:.2f} дБ")
    print(f" - Средняя спектральная плоскостность: {flatness_value:.4f}")
    print(f" - Эхо задержка (прибл.): {echo_delay:.3f} сек")

    # # Визуализация автокорреляции
    # plt.figure(figsize=(10, 4))
    # plt.plot(np.arange(len(autocorr)) / sr, autocorr)
    # plt.title("Автокорреляция (для оценки эха)")
    # plt.xlabel("Задержка (сек)")
    # plt.ylabel("Амплитуда")
    # plt.grid(True)
    # plt.show()


# Пример использования
if __name__ == "__main__":
    audio_file = "with_echo.wav"  # замените на свой файл
    print(audio_file)
    analyze_audio(audio_file)

    audio_file = "processed_output.wav"  # замените на свой файл
    print(audio_file)
    analyze_audio(audio_file)
