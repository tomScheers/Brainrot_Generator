import subprocess
import time

from mutagen.mp3 import MP3

import reddit
# import transcript
import tts


def format_time(seconds, time_format):
    return time.strftime(time_format, time.gmtime(seconds))


def main():
    story = reddit.get_post("AmItheAsshole")
    story_txt = story["data"]["children"][1]["data"]["selftext"]
    audio_path = "./Vid_Com/story.mp3"
    tts.text_to_speech(story_txt, path=audio_path)

    audio = MP3(audio_path)
    audio_length = audio.info.length

    video_path = "./Vid_Com/vid.mp4"
    output_path = "Output/result.mp4"
    trimmed_video_path = "./Vid_Com/trimmed_vid.mp4"

    start_time_seconds = 20
    end_time_padding = 3
    end_time_seconds = start_time_seconds + audio_length + end_time_padding

    time_format = "%H:%M:%S"
    formatted_start_time = format_time(start_time_seconds, time_format)
    formatted_end_time = format_time(end_time_seconds, time_format)


    # Trim video to be the appropiate length based on the mp3 length
    subprocess.run([
        "ffmpeg", "-y",
        "-hide_banner",
        "-loglevel", "error",
        "-i", video_path,
        "-ss", formatted_start_time,
        "-to", formatted_end_time,
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "experimental",
        trimmed_video_path
    ])

    # Merge audio and video file
    subprocess.run([
        "ffmpeg", "-y",
        "-hide_banner",
        "-loglevel", "error",
        "-i", trimmed_video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest", output_path
    ])

    subprocess.run([
        "rm", trimmed_video_path, audio_path
    ])

    # transcript.add_subtitles_to_video(output_path, story_txt, "./output/subtitles.mp4")


if __name__ == "__main__":
    main()
