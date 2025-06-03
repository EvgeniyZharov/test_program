import sounddevice as sd
from scipy.io.wavfile import read

rate, data = read("with_echo.wav")
sd.play(data, samplerate=rate)
sd.wait()  # Ждёт завершения воспроизведения
