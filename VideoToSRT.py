import moviepy.editor as mp
import pysrt
import speech_recognition as sr

# Load the video file
video = mp.VideoFileClip("video.mp4")

# Extract the audio from the video
audio = video.audio

# Convert audio to text
r = sr.Recognizer()
with sr.AudioFile(audio) as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data)

# Create a new SRT file
srt_file = pysrt.SubRipFile()

# Add the subtitles
srt_index = 1
for line in text.splitlines():
    start = srt_index
    end = srt_index + 1
    start_time = video.duration / len(text) * (start - 1)
    end_time = video.duration / len(text) * end
    subtitle = pysrt.SubRipItem(
        index=srt_index,
        start=pysrt.SubRipTime.from_seconds(start_time),
        end=pysrt.SubRipTime.from_seconds(end_time),
        text=line,
    )
    srt_file.append(subtitle)
    srt_index += 1

# Save the SRT file
srt_file.save("subtitles.srt")

# Add the subtitles to the video
video = video.set_audio(audio)
video = video.set_subtitles("subtitles.srt")
video.write_videofile("video_with_subtitles.mp4")
