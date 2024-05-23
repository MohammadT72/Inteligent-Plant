# import glob
import cv2
import base64
import os
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd
import wavio
import numpy as np
from models import stt_tts_model
from functions.langchain.logics import *
from functions.face_recognition.general import verify_face_in_db
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
def record_voice(duration=5, fs=44100):
  print("Recording...")
  recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype=np.int16)
  sd.wait()  # Wait until the recording is finished
  print("Recording complete.")
  return recording, fs

# Save the recording to a file
def save_recording(recording, fs, filename='human_input_voice.wav'):
    wavio.write(filename, recording, fs, sampwidth=2)
    return filename

def get_human_voice_func():
  """A tool that the plant can use to listen to the human voice, and understand what they say"""
  recording, fs = record_voice()
  wav_filename = save_recording(recording, fs)
  audio = AudioSegment.from_wav(wav_filename)
  transcription = stt_tts_model.audio.transcriptions.create(
      model="whisper-1", 
      file=audio, 
      response_format="text"
    )
  return transcription.text

# def search_Arxiv(query=None):
#     """A tool that the plant can search scientific articles in ArXive web database"""
#     docs = arxiv.run(query)
#     return docs

def create_plant_voice_func(input_text=None):
    """A tool that the plant can convert the text, or its thoughts to voice, so it can be played through speakers"""
    response = stt_tts_model.audio.speech.create(
        model="tts-1", voice="nova", input=input_text)
    name = 'plant_output_voice.mp3'
    path=os.path.join(os.getcwd(),name)
    response.stream_to_file(name)
    
    # Load the mp3 file and play it
    audio = AudioSegment.from_mp3(path)
    play(audio)
    return ''


# def get_current_time_and_date() -> str:
#     """This tool returns the current date and time."""
#     tehran = ZoneInfo('Asia/Tehran')
#     current_date = datetime.now(tehran).strftime("%B %d, %Y")
#     current_time = datetime.now(tehran).strftime("%H:%M %p")
#     return f"The current date is {current_date} and the current time is {current_time}."
