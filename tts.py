from gtts import gTTS
import os
import subprocess
import re


def sanitize_text(text):
    translation_dict = {r"aita": "am I the asshole", r"(\d+)m": r"\1em"}

    new_text = text
    for translation_key, translation_val in translation_dict.items():
        new_text = re.sub(translation_key,
                          translation_val,
                          new_text,
                          flags=re.IGNORECASE)
    print(new_text)
    return new_text


def text_to_speech(text,
                   path="Vid_Com/story.mp3",
                   lang='en',
                   tld="us",
                   speed=1.3):
    text = sanitize_text(text)
    obj = gTTS(text=text, lang=lang, slow=False, tld=tld)
    temp_path = "Vid_Com/temp.mp3"
    obj.save(temp_path)
    speed_up_audio(temp_path, path, speed)
    os.remove(temp_path)


def speed_up_audio(input_path, output_path, speed=1.3):
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", input_path,
        "-filter:a", f"atempo={speed}", "-vn", output_path
    ])


if __name__ == '__main__':
    print(sanitize_text("aita? I 39m"))
