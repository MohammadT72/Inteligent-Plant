# import glob
import cv2
import base64
import os
from datetime import datetime
import pyaudio
import wave
import io
import requests
import logging
import time
import psutil
from functions.langchain.logics import *
from functions.face_recognition.general import verify_face_in_db

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# def play_a_song(name)-> None:
#   '''This tool can play a song by it's name'''
#   display(Audio(f'/content/{name}.mp3',rate=44100, autoplay=True))
# def play_a_random_song(name=None)-> None:
#   '''This tool can play a random song'''
#   songs_path=glob.glob(os.path.join(os.getcwd(),'songs','*'))
#   selected_song=songs_path[0]
#   name=os.path.basename(selected_song).split('.mp3')[0]
#   display(Audio(selected_song,rate=44100, autoplay=True))
#   return f"The song named {name} is playing"

def encode_image(image_path, size):
    # Read the image using cv2
    image = cv2.imread(image_path)

    # Resize the image
    resized_image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)

    # Encode the image to JPEG format
    _, buffer = cv2.imencode('.jpg', resized_image)

    # Encode the bytes buffer to base64
    return base64.b64encode(buffer).decode('utf-8')
def capture_and_save_image(output_filename='captured_image.jpg'):
    # Open a connection to the default camera (usually the first camera)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    # Read a frame from the camera
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame.")
        return
    # Save the captured frame to a file
    cv2.imwrite(output_filename, frame)
    # Release the camera
    cap.release()

def recognize_a_face_func():
  capture_and_save_image()
  base_path = os.getcwd()
  captured_image_path = os.path.join(base_path,'captured_image.jpg')
  db_path = os.path.join(base_path,'embeddings.db')
  result = verify_face_in_db(captured_image_path,db_path)
  if result != None:
    names = ','.join(result)
    return f"The recognized faces are {names}"
  else:
    return "No face detected"
def parse_out_memory(memory_row):
  return f'date:{memory_row[0]} and description:{memory_row[-2]}. '
def parse_in_memory(description,mem_type='moment',title='None',priority='normal'):
  date="{:%B %d, %Y}".format(datetime.now())
  memory=(date,title,mem_type,description,priority)
  return memory
# tools
# def create_memory(description,mem_type='moment',title='None',priority='normal') -> None:
#     """This tool can create a memory based on date of the moment, title, type of event
#         , the description, and the priority
#     """
#     memory=parse_in_memory(description,mem_type,title,priority)
#     sql = ''' INSERT INTO memories(date,title,type,data,priority)
#               VALUES(?,?,?,?,?) '''
#     cur = conn.cursor()
#     cur.execute(sql, memory)
#     return None

# def check_the_date(day)->str:
#     """This tool tell the plant current date"""
#     tehran = ZoneInfo('Asia/Tehran')
#     date="{:%B %d, %Y}".format(datetime.now(tehran))
#     return date

# def check_the_time(time)->str:
#     """This tool tell the plant current time like 10:15 PM"""
#     tehran = ZoneInfo('Asia/Tehran')
#     time = datetime.now(tehran).strftime("%H:%M %p")
#     return time

# def get_all_memories() -> str:
#     """This tool can retrieve all memories"""
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM memories")
#     rows = cur.fetchall()
#     text=''
#     for row in rows:
#         parsed_mem=parse_out_memory(row)
#         text+=parsed_mem
#     return text
# def get_memory_by_title(title) -> str:
#     """This tool can retrieve an specific memory by it's title"""
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM memories WHERE title LIKE ?", (title,))
#     rows = cur.fetchall()
#     text=''
#     for row in rows:
#         parsed_mem=parse_out_memory(row)
#         text+=parsed_mem
#     return text
# def get_reminders_memory(title) -> str:
#     """This tool can retrieve all the reminders"""
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM memories WHERE title LIKE ?", ('%reminder%',))
#     rows = cur.fetchall()
#     text=''
#     for row in rows:
#         parsed_mem=parse_out_memory(row)
#         text+=parsed_mem
#     return text
# def get_memory_by_priority(priority) -> str:
#     """This tool can retrieve an specific memory by it's priority"""
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM memories WHERE priority=?", (priority,))
#     rows = cur.fetchall()
#     text=''
#     for row in rows:
#         parsed_mem=parse_out_memory(row)
#         text+=parsed_mem
#     return text
def get_sensors_data_func(sen_list=None):
    """retireving the sensors data"""
    data={
        'temp':23,
        'moisture':0.2,
        'brightness':500,
    }
    data=parse_sensors_data(data)
    # if data['temp']==None or data['moisture']==None:
      # raise ToolException('The sensors data are not available.')
    output_text=''
    for _,value in data.items():
      output_text+=value
    return output_text
# def get_weather_forcast(location='Tonekabon', day='today'):
#     """A tool that the plant can use to extract a three day weather forcast"""
#     if os.name == 'nt':
#       asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     nest_asyncio.apply()
#     loop = asyncio.get_event_loop()
#     response=loop.run_until_complete(getweather(location,day))
#     return response

def record_voice(duration=5, fs=44100, channels=2):
    """Record audio from the microphone."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=fs,
                    input=True,
                    frames_per_buffer=1024)
    
    logging.info("Recording...")
    frames = []
    start_time = time.time()  # Record the start time here
    for _ in range(0, int(fs / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    logging.info("Recording complete.")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    logging.info(f"Recording time: {time.time() - start_time:.2f} seconds")
    return frames, fs, channels

def save_wave(frames, fs, channels):
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
    
    logging.info(f"Saving wave time: {time.time() - start_time:.2f} seconds")
    return buffer

def get_human_voice_func(api_key):
    """A tool that the plant can use to listen to the human voice, and understand what they say."""
    try:
        process = psutil.Process()

        # Record the voice
        mem_before = process.memory_info().rss
        frames, fs, channels = record_voice()
        mem_after = process.memory_info().rss
        logging.info(f"Recording memory usage: {(mem_after - mem_before) / (1024 * 1024):.2f} MB")
        
        # Save the recorded audio to an in-memory wave file
        mem_before = process.memory_info().rss
        audio_buffer = save_wave(frames, fs, channels)
        mem_after = process.memory_info().rss
        logging.info(f"Saving wave memory usage: {(mem_after - mem_before) / (1024 * 1024):.2f} MB")
        
        # Prepare the request headers and data
        headers = {
            "Authorization": f"Bearer {api_key}",
        }
        files = {
            "file": ("audio.wav", audio_buffer, "audio/wav"),
            "model": (None, "whisper-1"),
            "response_format": (None, "text")
        }
        
        # Make the POST request to the API
        logging.info("Sending request to OpenAI API...")
        start_time = time.time()
        mem_before = process.memory_info().rss
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers=headers,
            files=files
        )
        mem_after = process.memory_info().rss
        logging.info(f"API request time: {time.time() - start_time:.2f} seconds")
        logging.info(f"API request memory usage: {(mem_after - mem_before) / (1024 * 1024):.2f} MB")
        
        # Log the response
        logging.info(f"Status Code: {response.status_code}")
        logging.info(f"Response Content: {response.content}")
        
        # Check the response status and get the transcription text
        if response.status_code == 200:
            logging.info("Transcription successful.")
            return response.text.strip()  # Directly return the text content
        else:
            logging.error(f"Request failed with status code {response.status_code}: {response.text}")
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    except Exception as e:
        logging.exception("An error occurred during transcription.")
        raise e

# def search_Arxiv(query=None):
#     """A tool that the plant can search scientific articles in ArXive web database"""
#     docs = arxiv.run(query)
#     return docs

def create_plant_voice_func(api_key, text, voice='nova', response_format='mp3', speed=1.0):
    """Convert text to speech using the OpenAI API."""
    try:
        # Prepare the request headers and data
        headers = {
            "Authorization": f"Bearer {api_key}",
        }
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
            headers=headers,
            json=data
        )
        mem_after = process.memory_info().rss
        logging.info(f"TTS request time: {time.time() - start_time:.2f} seconds")
        logging.info(f"TTS request memory usage: {(mem_after - mem_before) / (1024 * 1024):.2f} MB")
        
        # Log the response
        logging.info(f"Status Code: {response.status_code}")
        
        # Check the response status and get the audio content
        if response.status_code == 200:
            logging.info("Text-to-speech conversion successful.")
            return response.content  # Return the binary audio content
        else:
            logging.error(f"Request failed with status code {response.status_code}: {response.text}")
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    except Exception as e:
        logging.exception("An error occurred during text-to-speech conversion.")
        raise e
# def get_current_time_and_date() -> str:
#     """This tool returns the current date and time."""
#     tehran = ZoneInfo('Asia/Tehran')
#     current_date = datetime.now(tehran).strftime("%B %d, %Y")
#     current_time = datetime.now(tehran).strftime("%H:%M %p")
#     return f"The current date is {current_date} and the current time is {current_time}."
