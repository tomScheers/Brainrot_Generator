from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip


def add_subtitles_to_video(video_path: str, subtitles: str, output_path: str) -> None:
    # Load the video
    video = VideoFileClip(video_path)

    # Create a TextClip object with the subtitles
    subtitle_clip = TextClip(subtitles, fontsize=24, color='white', bg_color='black', size=video.size)
    subtitle_clip = subtitle_clip.set_position(('center', 'bottom')).set_duration(video.duration)

    # Overlay the subtitles on the video
    video_with_subtitles = CompositeVideoClip([video, subtitle_clip])

    # Write the result to a file
    video_with_subtitles.write_videofile(output_path, codec='libx264')


if __name__ == "__main__":
    add_subtitles_to_video("./output/result.mp4", "hello", "./output/subtitles.mp4")
