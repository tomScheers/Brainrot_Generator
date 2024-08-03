import tts
import reddit
from moviepy.editor import VideoFileClip, AudioFileClip


# main mod
def main():
    story = reddit.get_post("AmItheAsshole")
    story_txt = story["data"]["children"][1]["data"]["selftext"]
    audio_path = "./Vid_Com/story.mp3"
    tts.text_to_speech(story_txt, path=audio_path)
    video = VideoFileClip("./Vid_Com/vid.mp4")
    audio = AudioFileClip(audio_path)
    video = video.set_audio(audio)
    video.write_videofile("result.mp4", codec='mpeg4', audio_codec='libvorbis')



if __name__ == "__main__":
    main()
