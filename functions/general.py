# import glob
import os
from datetime import datetime
from langchain_core.tools import ToolException
from pydub import AudioSegment
from pydub.playback import play
# import simpleaudio as sa
from functions.logics import *
from models import stt_tts_model

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
    if data['temp']==None or data['moisture']==None:
      raise ToolException('The sensors data are not available.')
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

# def get_human_voice(duration=None):
#     """A tool that the plant can use to listen to the human voice, and understand what they say"""
#     file_name=record_audio()
#     audio_file= open(f"/content/{file_name}", "rb")
#     transcription = stt_tts_model.audio.transcriptions.create(
#         model='whisper-1',file=audio_file)
#     return transcription.text
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
