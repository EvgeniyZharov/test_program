import os
import pathlib

def apply_deep_filter(input_wav: str):
    if not os.path.exists(input_wav):
        raise FileNotFoundError(f"File is not: {input_wav}")

    os.system(f"deepFilter ./{input_wav}")

    base = pathlib.Path(input_wav).stem
    enhanced_name = f"{base}_DeepFilterNet3.wav"
    final_name = f"{base}.wav"

    if os.path.exists(enhanced_name):
        os.rename(enhanced_name, final_name)
        print(f"New file: {final_name}")
    else:
        print(f"Not founded {enhanced_name}.")


if __name__ == "__main__":
    apply_deep_filter("with_echo.wav")
