import subprocess
import time
import requests
import re
import os
import gTTS
from mutagen.mp3 import MP3


def sanitize_text(text, translation_dict) -> None:
    for translation_key, translation_val in translation_dict.items():
        text = re.sub(translation_key,
                      translation_val,
                      text,
                      flags=re.IGNORECASE)


def text_to_speech(text,
                   path="Vid_Com/story.mp3",
                   lang="en",
                   tld="us",
                   speed=1.3) -> None:
    # A translation dict with regexes on sentences or words you want to translate to suit the tts better
    translation_dict = {r"aita": "am I the asshole", r"(\d+)m": r"\1em"}
    sanitize_text(text, translation_dict)  # Sanitizes the text, removing
    obj = gTTS(text=text, lang=lang, slow=False, tld=tld)
    temp_path = "Vid_Com/temp.mp3"
    obj.save(temp_path)

    speed_up_audio(temp_path, path, speed)
    os.remove(temp_path)


def speed_up_audio(input_path, output_path, speed=1.3) -> None:
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", input_path,
        "-filter:a", f"atempo={speed}", "-vn", output_path
    ])


def get_post(sr) -> str:
    url = f'https://www.reddit.com/r/{sr}/random.json'
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    response = res.json()  # Directly get the JSON response
    return response


def main() -> None:
    # Get the post from an api
    subreddit = "AmItheAsshole"
    story = get_post(subreddit)

    story_txt = story["data"]["children"][1]["data"]["selftext"]

    # Generate The audio file
    audio_path = "./Vid_Com/story.mp3"
    text_to_speech(story_txt, path=audio_path)

    audio = MP3(audio_path)
    audio_length = audio.info.length

    # Define paths to videos
    video_path = "./Vid_Com/vid.mp4"
    output_path = "Output/result.mp4"
    trimmed_video_path = "./Vid_Com/trimmed_vid.mp4"

    start_time_seconds = 20  # At which seconds point you want to start the video
    end_time_padding = 3  # How many second of silents you want at the end of the video
    end_time_seconds = start_time_seconds + audio_length + end_time_padding

    # Get the start and end time of the video, so that the program can trim the video file right
    time_format = "%H:%M:%S"
    formatted_start_time = time.strftime(time_format,
                                         time.gmtime(start_time_seconds))
    formatted_end_time = time.strftime(time_format,
                                       time.gmtime(end_time_seconds))

    # Trim video to be the appropiate length based on the mp3 length
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", video_path,
        "-ss", formatted_start_time, "-to", formatted_end_time, "-c:v", "copy",
        "-c:a", "aac", "-strict", "experimental", trimmed_video_path
    ])

    # Merge audio and video file
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i",
        trimmed_video_path, "-i", audio_path, "-c:v", "copy", "-map", "0:v:0",
        "-map", "1:a:0", "-shortest", output_path
    ])

    # Remove any tmp files
    subprocess.run(["rm", trimmed_video_path, audio_path])


if __name__ == "__main__":
    main()
