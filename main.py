import tts
import reddit
import subprocess
from mutagen.mp3 import MP3
import time


# main mod
def main():
    story = reddit.get_post("AmItheAsshole")
    story_txt = story["data"]["children"][1]["data"]["selftext"]
    audio_path = "./Vid_Com/story.mp3"
    tts.text_to_speech(story_txt, path=audio_path)

    audio = MP3(audio_path)
    audio_length = audio.info.length

    video_path = "./Vid_Com/vid.mp4"
    output_path = "result.mp4"
    trimmed_video_path = "./Vid_Com/trimmed_vid.mp4"

    start_time_seconds = 20
    end_time_seconds = start_time_seconds + audio_length + 3

    time_format = "%H:%M:%S"
    formatted_start_time = time.strftime(time_format, time.gmtime(start_time_seconds))
    formatted_end_time = time.strftime(time_format, time.gmtime(end_time_seconds))


    # Trim video and merge with audio in one go
    subprocess.run([
        "ffmpeg",
        "-i", video_path,
        "-ss", formatted_start_time,
        "-to", formatted_end_time,
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "experimental",
        trimmed_video_path
    ])

    subprocess.run([
        "ffmpeg",
        "-i", trimmed_video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "experimental",
        output_path
    ])



if __name__ == "__main__":
    main()
