import moviepy.editor as mp
import pysrt
import speech_recognition as sr
import os
from app import app

# Load the video file


def VideoToSrt(filename):
    video = mp.VideoFileClip(filename)


    audio = video.audio

    
    r = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)

   
    srt_file = pysrt.SubRipFile()

   
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

    srt_file.save("subtitles.srt")

    
    video = video.set_audio(audio)
    video = video.set_subtitles("subtitles.srt")
    video.write_videofile(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    