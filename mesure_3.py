import numpy as np
import librosa
import matplotlib.pyplot as plt


def estimate_noise_from_non_speech(y, sr):
    # Выделим только участки с речью
    speech_intervals = librosa.effects.split(y, top_db=25)
    mask = np.zeros(len(y), dtype=bool)

    for start, end in speech_intervals:
        mask[start:end] = True

    # Всё, что не речь — потенциальный шум
    noise = y[~mask]

    if len(noise) == 0:
        return -1  # если нет "тишины", вернуть что-то особенное

    noise_power = np.mean(noise ** 2)
    noise_db = 10 * np.log10(noise_power + 1e-10)

    return noise_db


def spectral_flatness(y, sr):
    S = np.abs(librosa.stft(y))
    flatness = librosa.feature.spectral_flatness(S=S)
    return np.mean(flatness)


def analyze_noisy_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)

    noise_db = estimate_noise_from_non_speech(y, sr)
    flatness = spectral_flatness(y, sr)

    print(f"[📊] Анализ: {file_path}")
    print(f" - Шум в 'тишине' (предполагаемый): {noise_db:.2f} дБ")
    print(f" - Спектральная плоскостность: {flatness:.4f}")

    # Визуализация спектра
    plt.figure(figsize=(10, 4))
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz')
    plt.title("Спектрограмма")
    plt.colorbar(format="%+2.0f dB")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    analyze_noisy_audio("noisy_output.wav")