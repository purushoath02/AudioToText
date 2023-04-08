import moviepy.editor as mp
import pysrt
import speech_recognition as sr
import os
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
#from app import app

# Load the video file


def VideoToSrt(filename):
    video = mp.VideoFileClip('static/uploads/'+filename)
    video.audio.write_audiofile(r"temp/sample.wav")
    
    #audio = video.audio
    #audio.write_audiofile("sample.WAV")
    ''
    r = sr.Recognizer()
    with sr.AudioFile('temp/sample.wav') as source:
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
            start=pysrt.SubRipTime(start_time),
            end=pysrt.SubRipTime(end_time),
            text=line,
        )
        srt_file.append(subtitle)
        srt_index += 1
    srt_path = "static/subtitles/subtitle_"+filename[:-3]+"srt"
    srt_file.save(srt_path)
    subtitle = SubtitlesClip(srt_path)
    subtitle = subtitle.set_position(("center", "bottom")).set_duration(video.duration)
    final_clip = mp.CompositeVideoClip([video, subtitle])
    final_clip.write_videofile('static/uploads/final_'+filename)
    return "final_"+filename
    
    #video = video.set_audio('sample.wav')
    #video = video.set_subtitles("subtitles.srt")
    #video.write_videofile(os.path.join(app.config['UPLOAD_FOLDER'],filename))

#video = mp.VideoFileClip("video.mp4")

# Load the subtitle file
#subtitle = mp.SubtitlesClip("subtitle.srt")

# Set the position and duration of the subtitle


# Combine the video and subtitle clips


# Write the final clip to a new file
