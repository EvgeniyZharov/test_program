import subprocess

def add_echo(input_path, output_path, delay=1000, decay=0.5):
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-af', f'aecho=0.8:0.9:{delay}:{decay}',
        '-y',
        output_path
    ]
    subprocess.run(cmd, check=True)

# Пример использования
add_echo('audio_1.wav', 'with_echo.wav')
