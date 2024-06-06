import webrtcvad
import wave
import collections
from pydub import AudioSegment

def read_wave(path):
    audio = AudioSegment.from_file(path)
    if audio.frame_rate not in (8000, 16000, 32000, 48000):
        audio = audio.set_frame_rate(16000)
    if audio.channels != 1:
        audio = audio.set_channels(1)
    if audio.sample_width != 2:
        audio = audio.set_sample_width(2)

    pcm_data = audio.raw_data
    sample_rate = audio.frame_rate

    return pcm_data, sample_rate

def sample_generator(frame_duration_ms, offset_duration_ms, audio, sample_rate):
    frame_size = int(sample_rate * frame_duration_ms / 1000) * 2  # Multiply by 2 for 16-bit audio
    offset_size = int(sample_rate * offset_duration_ms / 1000) * 2  # Multiply by 2 for 16-bit audio
    audio_length = len(audio)
    for offset in range(0, audio_length - frame_size + 1, offset_size):
        yield audio[offset:offset + frame_size]

def vad_collector(sample_rate, frame_duration_ms, vad, frames):
    total_frames = 0
    speech_frames = 0

    for frame in frames:
        is_speech = vad.is_speech(frame, sample_rate)
        total_frames += 1

        if is_speech:
            speech_frames += 1

    confidence = speech_frames / total_frames if total_frames > 0 else 0
    return confidence

def detect_voice_in_audio(file_path, aggressiveness=3, frame_duration_ms=30, offset_duration_ms=50):
    vad = webrtcvad.Vad(aggressiveness)
    audio, sample_rate = read_wave(file_path)
    frames = sample_generator(frame_duration_ms, offset_duration_ms, audio, sample_rate)

    consecutive_chunks = 0
    chunk_size_ms = 300  # Define the chunk size
    chunk_duration_frames = chunk_size_ms // frame_duration_ms

    chunk_frames = []
    for frame in frames:
        chunk_frames.append(frame)
        confidence = vad_collector(sample_rate, frame_duration_ms, vad, chunk_frames)
        if confidence > 0.7:
            consecutive_chunks += 1
            if consecutive_chunks >= 5:
                return True

    return False

def main_loop():
    while True:
        # Assume `recording.wav` is the file being recorded
        recording_file_path = "output_audio.wav"
        
        # Here you would add your code to record audio into `recording.wav`
        
        # Check if human voice is detected
        human_detected = detect_voice_in_audio(recording_file_path)
        if human_detected:
            print("Human voice detected with confidence above 0.7 in 10 consecutive chunks. Processing the recording...")
            return True
        else:
            print("No human voice detected with sufficient confidence. Breaking the loop.")
            return False

if __name__ == "__main__":
    main_loop()
