import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq


def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)
    return y, sr


def plot_waveform(y, sr, ax):
    ax.plot(np.linspace(0, len(y) / sr, len(y)), y)
    ax.set_title("Временная волна")
    ax.set_xlabel("Время (с)")
    ax.set_ylabel("Амплитуда")


def plot_spectrogram(y, sr, ax):
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    img = librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log', ax=ax)
    ax.set_title("Спектрограмма")
    plt.colorbar(img, ax=ax, format="%+2.0f dB")


def plot_mel_spectrogram(y, sr, ax):
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', ax=ax)
    ax.set_title("Мел-спектрограмма")
    plt.colorbar(img, ax=ax, format="%+2.0f dB")


def plot_fft(y, sr, ax):
    n = len(y)
    yf = fft(y)
    xf = fftfreq(n, 1 / sr)
    ax.plot(xf[:n // 2], np.abs(yf[:n // 2]))
    ax.set_title("Частотный спектр (БПФ)")
    ax.set_xlabel("Частота (Гц)")
    ax.set_ylabel("Амплитуда")


def plot_mfcc(y, sr, ax):
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    img = librosa.display.specshow(mfccs, x_axis='time', ax=ax)
    ax.set_title("MFCC")
    plt.colorbar(img, ax=ax)


def plot_all(file_path, output_path):
    y, sr = load_audio(file_path)

    fig, axes = plt.subplots(3, 2, figsize=(14, 10))
    axes = axes.flatten()

    plot_waveform(y, sr, axes[0])
    plot_spectrogram(y, sr, axes[1])
    plot_mel_spectrogram(y, sr, axes[2])
    plot_fft(y, sr, axes[3])
    plot_mfcc(y, sr, axes[4])

    axes[5].axis('off')  # Пустая ячейка
    plt.suptitle("Анализ аудиофайла: " + file_path, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()


# Замените путь на нужный вам аудиофайл
if __name__ == "__main__":
    audio_file = "file_music.wav"
    output_path = "spectrograms_output_1.png"
    plot_all(audio_file, output_path)

    audio_file = "processed_output.wav"
    output_path = "spectrograms_output_2.png"
    plot_all(audio_file, output_path)

