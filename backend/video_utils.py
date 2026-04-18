import moviepy.editor as mp
import librosa
import numpy as np
import os

def detect_emotional_peaks(audio_path):
    y, sr = librosa.load(audio_path)
    rms = librosa.feature.rms(y=y)[0]
    peaks = np.where(rms > np.percentile(rms, 90))[0]
    timestamps = librosa.frames_to_time(peaks, sr=sr)
    return timestamps

def process_video(video_path):
    clip = mp.VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    clip.audio.write_audiofile(audio_path)

    peaks = detect_emotional_peaks(audio_path)

    outputs = []
    os.makedirs("outputs", exist_ok=True)

    # If no peaks found, just take first 10s as fallback
    if len(peaks) == 0:
        subclip = clip.subclip(0, min(10, clip.duration))
        out_name = os.path.join("outputs", "fallback_clip.mp4")
        subclip.write_videofile(out_name, codec="libx264")
        outputs.append(out_name)
        return outputs

    for i, t in enumerate(peaks[:3]):  # top 3 moments
        subclip = clip.subclip(max(0, t-5), min(clip.duration, t+5))
        subclip = subclip.resize(height=1080, width=608)

        # Caption overlay
        txt = mp.TextClip("🔥 Viral Moment!", fontsize=70, color="white", bg_color="black")
        txt = txt.set_position(("center","bottom")).set_duration(subclip.duration)
        final = mp.CompositeVideoClip([subclip, txt])

        out_name = os.path.join("outputs", f"output_clip_{i}.mp4")
        final.write_videofile(out_name, codec="libx264")
        outputs.append(out_name)

    return outputs
