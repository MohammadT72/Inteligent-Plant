# functions.py
import pyaudio
import wave
import io
import requests
import collections
import logging
import time
import psutil
import base64
import os
import simpleaudio as sa
from pydub import AudioSegment
import webrtcvad
import threading
import queue
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AudioProcessor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        self.poor_connection_audio_path = r'/home/mohammadt72/myprojects/plant/pre_saved_voices/serious/internet_connection.wav'
        self.goodbye_audio_path = r'/home/mohammadt72/myprojects/plant/pre_saved_voices/serious/goodbye.wav'
    def record_voice(self, fs=16000, channels=1):
        """Continuously record audio from the microphone until human voice is detected or no detection for 2 seconds."""
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=fs,
                        input=True,
                        frames_per_buffer=1024)

        logging.info("Recording...")
        frames = []
        last_two_seconds = collections.deque(maxlen=int(fs / 1024 * 3))
        start_time = time.time()
        last_detection_time = start_time
        human_detection_num = 0

        while True:
            data = stream.read(1024)
            frames.append(data)
            last_two_seconds.append(data)

            # Only process the last 2 seconds of recorded frames
            buffer = self.save_wave(list(last_two_seconds), fs, channels)

            # Check if human voice is detected
            human_detected = self.detect_voice_in_audio(buffer, offset_duration_ms=30, repeat_threshold=5)
            if human_detected:
                last_detection_time = time.time()
                human_detection_num += 1

            # Stop recording if no human voice detected for 5 seconds
            if time.time() - last_detection_time > 5:
                logging.info("No human voice detected for 5 seconds. Stopping recording.")
                break

        logging.info(f"Recording complete. Total recording time: {time.time() - start_time:.2f} seconds")

        stream.stop_stream()
        stream.close()
        p.terminate()

        return frames, fs, channels, human_detection_num

    def save_wave(self, frames, fs, channels):
        """Save the recorded frames as a wave file in memory."""
        start_time = time.time()
        buffer = io.BytesIO()
        wf = wave.open(buffer, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        buffer.seek(0)
        return buffer

    def read_wave(self, buffer):
        audio = AudioSegment.from_file(buffer, format="wav")
        if audio.frame_rate not in (8000, 16000, 32000, 48000):
            audio = audio.set_frame_rate(16000)
        if audio.channels != 1:
            audio = audio.set_channels(1)
        if audio.sample_width != 2:
            audio = audio.set_sample_width(2)

        pcm_data = audio.raw_data
        sample_rate = audio.frame_rate

        return pcm_data, sample_rate
    def sample_generator(self, frame_duration_ms, offset_duration_ms, audio, sample_rate):
        frame_size = int(sample_rate * frame_duration_ms / 1000) * 2  # Multiply by 2 for 16-bit audio
        offset_size = int(sample_rate * offset_duration_ms / 1000) * 2  # Multiply by 2 for 16-bit audio
        audio_length = len(audio)
        for offset in range(0, audio_length - frame_size + 1, offset_size):
            yield audio[offset:offset + frame_size]

    def vad_collector(self, sample_rate, frame_duration_ms, vad, frames):
        total_frames = 0
        speech_frames = 0

        for frame in frames:
            is_speech = vad.is_speech(frame, sample_rate)
            total_frames += 1

            if is_speech:
                speech_frames += 1

        confidence = speech_frames / total_frames if total_frames > 0 else 0
        return confidence
    def detect_voice_in_audio(self, buffer, aggressiveness=3, frame_duration_ms=30, offset_duration_ms=500,
                                    conf_threshold=0.7, repeat_threshold=10):
        vad = webrtcvad.Vad(aggressiveness)
        audio, sample_rate = self.read_wave(buffer)
        frames = self.sample_generator(frame_duration_ms, offset_duration_ms, audio, sample_rate)
        consecutive_chunks = 0
        chunk_size_ms = 300  # Define the chunk size
        chunk_duration_frames = chunk_size_ms // frame_duration_ms

        chunk_frames = []
        for frame in frames:
            chunk_frames.append(frame)
            confidence = self.vad_collector(sample_rate, frame_duration_ms, vad, chunk_frames)
            if confidence > conf_threshold:
                consecutive_chunks += 1
                if consecutive_chunks >= repeat_threshold:
                    return True
        return False
    def get_human_voice(self, pre_saved_audio_filenames_5, pre_saved_audio_filenames_20):
        """A tool that the plant can use to listen to the human voice, and understand what they say."""
        def play_pre_saved_audio(audio_filenames, stop_event):
            """Play the pre-saved audio files in sequence while waiting for the API response."""
            for filename in audio_filenames:
                if stop_event.is_set():
                    break
                wave_obj = sa.WaveObject.from_wave_file(filename)
                play_obj = wave_obj.play()
                play_obj.wait_done()
                if stop_event.is_set():  # Stop playing if response is ready
                    break

        def api_call(files, response_queue, stop_event):
            """Perform the API call and put the response in the queue."""
            logging.info("Sending request to OpenAI API...")
            start_time = time.time()
            mem_before = process.memory_info().rss
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers=self.headers,
                files=files
            )
            mem_after = process.memory_info().rss
            logging.info(f"API request time: {time.time() - start_time:.2f} seconds")
            logging.info(f"API request memory usage: {(mem_after - mem_before) / (1024 * 1024):.2f} MB")
            response_queue.put(response)
            stop_event.set()  # Signal to stop any pre-saved audio playback

        def start_audio_timer(audio_filenames, delay, stop_event):
            """Start a timer to play pre-saved audio after a delay."""
            time.sleep(delay)
            if not stop_event.is_set():
                play_pre_saved_audio(audio_filenames, stop_event)

        try:
            process = psutil.Process()

            # Record the voice
            mem_before = process.memory_info().rss
            frames, fs, channels, human_detection_num = self.record_voice()
            mem_after = process.memory_info().rss
            logging.info(f"Recording memory usage: {(mem_after - mem_before) / (1024 * 1024):.2f} MB")

            # Save the recorded audio to an in-memory wave file
            mem_before = process.memory_info().rss
            audio_buffer = self.save_wave(frames, fs, channels)
            mem_after = process.memory_info().rss
            logging.info(f"Saving wave memory usage: {(mem_after - mem_before) / (1024 * 1024):.2f} MB")

            if human_detection_num > 0:
                # Prepare the request headers and data
                files = {
                    "file": ("audio.wav", audio_buffer, "audio/wav"),
                    "model": (None, "whisper-1"),
                    "response_format": (None, "text")
                }

                # Manually set the content type in the files dictionary
                files['file'] = ("audio.wav", audio_buffer.read(), "audio/wav")
                audio_buffer.seek(0)  # Reset the buffer position

                response_queue = queue.Queue(maxsize=1)
                stop_event = threading.Event()

                # Start the API call in a separate thread
                api_thread = threading.Thread(target=api_call, args=(files, response_queue, stop_event))
                api_thread.start()

                # Start the timers to play pre-saved audio after 5 and 10 seconds
                timer_thread_5 = threading.Thread(target=start_audio_timer, args=(pre_saved_audio_filenames_5, 5, stop_event))
                timer_thread_20 = threading.Thread(target=start_audio_timer, args=(pre_saved_audio_filenames_20, 20, stop_event))
                timer_thread_5.start()
                timer_thread_20.start()

                # Wait for the API call to finish
                api_thread.join()

                # Ensure the pre-saved audio stops if still playing
                stop_event.set()
                timer_thread_5.join(timeout=0)
                timer_thread_20.join(timeout=0)

                # Get the API response from the queue
                response = response_queue.get()
                logging.info(f"Status Code: {response.status_code}")
                logging.info(f"Response Content: {response.content}")

                if response.status_code == 200:
                    logging.info("Transcription successful.")
                    return response.text.strip()
                else:
                    logging.error(f"Request failed with status code {response.status_code}: {response.text}")
                    raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
            else:
                logging.info("Human voice not detected.")
                return False

        except Exception as e:
            logging.exception("An error occurred during transcription.")
            raise e

    def create_plant_voice(self, text, voice='nova', response_format='wav', speed=1.0):
        """Convert text to speech using the OpenAI API."""
        try:
            # Prepare the request headers and data
            data = {
                "model": "tts-1",
                "input": text,
                "voice": voice,
                "response_format": response_format,
                "speed": speed
            }

            # Make the POST request to the API
            logging.info("Sending text-to-speech request to OpenAI API...")
            start_time = time.time()
            process = psutil.Process()
            mem_before = process.memory_info().rss
            response = requests.post(
                "https://api.openai.com/v1/audio/speech",
                headers=self.headers,
                json=data
            )
            print(response)
            mem_after = process.memory_info().rss
            logging.info(f"TTS request time: {time.time() - start_time:.2f} seconds")
            logging.info(f"TTS request memory usage: {(mem_after - mem_before) / (1024 * 1024):.2f} MB")

            # Log the response
            logging.info(f"Status Code: {response.status_code}")

            # Check the response status and get the audio content
            if response.status_code == 200:
                logging.info("Text-to-speech conversion successful.")
                return response.content
            else:
                logging.error(f"Request failed with status code {response.status_code}: {response.text}")
                self.play_audio(self.poor_connection_audio_path)
        except Exception as e:
            logging.exception("An error occurred during text-to-speech conversion.")
            raise e

    def play_audio(self, filename):
        """Play the generated audio content."""
        # Play the WAV file using simpleaudio
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    def text_to_speech_to_file(self, text, output_filename='output_audio.wav', voice='nova', response_format='wav', speed=1.0):
        """Convert text to speech and save the audio to a file."""
        audio_content = self.create_plant_voice(text, voice=voice, response_format=response_format, speed=speed)
        audio = AudioSegment.from_file(io.BytesIO(audio_content), format=response_format)
        audio.export(output_filename, format='wav')
        logging.info(f"Audio content saved as '{output_filename}'")
        return output_filename

class ChatBot:
    def __init__(self, api_key, system_message, tools):
        self.api_key = api_key
        self.system_message = system_message
        self.tools = tools
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        self.history = [{"role": "system", "content": self.system_message}]

    def make_chat_completion_request(self, messages):
        """Send a chat completion request to the OpenAI API."""
        payload = {
            "model": "gpt-4o",
            "messages": messages,
            "temperature": 0.7,
            "n": 1,
            "stop": None,
            "tools": self.tools['jsons'],
            "tool_choice": "auto"
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_json = response.json()
        response_message = response_json['choices'][0]['message']
        tool_calls = False
        if 'tool_calls' in response_message:
            tool_calls = response_json['choices'][0]['message']['tool_calls']
        if tool_calls:
            messages = [response_message]  # Extend conversation with assistant's reply
            for tool_call in tool_calls:
                function_name = tool_call['function']['name']
                function_to_call = self.tools['funcs'].get(function_name)

                if function_to_call:
                    function_args = json.loads(tool_call['function']['arguments'])
                    function_response = function_to_call(**function_args)

                    messages.append(
                        {
                            "tool_call_id": tool_call['id'],
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    )
            self.history = self.history + messages
            second_response = self.make_chat_completion_request(self.history)
            return second_response
        return response.json()

    def get_image_encoded(self, image_path):
        """Encode an image to base64."""
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        return None

    def invoke(self, message, speech=True):
        image_path = os.path.join(os.getcwd(), 'captured_image.jpg')
        encoded_image = self.get_image_encoded(image_path)

        if encoded_image:
            self.history.append({
                "role": "user",
                "content": f"{message}",
                "image_url": f"data:image/png;base64,{encoded_image}"
            })
            os.remove(image_path)
        else:
            self.history.append({
                "role": "user",
                "content": message
            })

        response = self.make_chat_completion_request(self.history)
        response_message = response['choices'][0]['message']['content']
        self.history.append({
            "role": "assistant",
            "content": response_message
        })

        if speech:
            audio_processor = AudioProcessor(self.api_key)
            audio_content = audio_processor.create_plant_voice(response_message)
            audio = AudioSegment.from_file(io.BytesIO(audio_content), format='wav')
            output_filename = 'output_filename.wav'
            audio.export(output_filename, format='wav')
            logging.info(f"Audio content saved as '{output_filename}'")
            audio_processor.play_audio(output_filename)

        return response_message
