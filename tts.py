from gtts import gTTS
import os
import subprocess


def text_to_speech(text, path="story.mp3", lang='en', tld="us"):
    obj = gTTS(text=text, lang=lang, slow=False, tld=tld)
    temp_path = "temp.mp3"
    obj.save(temp_path)
    speed_up_audio(temp_path, path)


def speed_up_audio(input_path, output_path, speed=1.3):
    subprocess.run([
        "ffmpeg",
        "-i", input_path,
        "-filter:a", f"atempo={speed}",
        "-vn",
        output_path
    ])


if __name__ == '__main__':
    print("Hello World")
    text_to_speech("Hello beautiful world!")
    os.system("play story.mp3")
