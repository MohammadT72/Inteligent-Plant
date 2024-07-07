import json
import random
import glob
import time
import cv2
import base64
import simpleaudio as sa
import os
from pygame import mixer
from functions.logics import parse_sensors_data

def get_sensors_data_func(sen_list=None):
    """retireving the sensors data"""
    data={
        'temp':23,
        'moisture':0.2,
        'brightness':500,
    }
    data = parse_sensors_data(data)
    return json.dumps(data)
    # data=parse_sensors_data(data)
    # if data['temp']==None or data['moisture']==None:
      # raise ToolException('The sensors data are not available.')
    # output_text=''
    # for _,value in data.items():
    #   output_text+=value
    # return output_text
'''
def encode_image(image, size=(512,512)):
    # Resize the image
    resized_image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)

    # Encode the image to JPEG format
    _, buffer = cv2.imencode('.jpg', resized_image)

    # Encode the bytes buffer to base64
    return base64.b64encode(buffer).decode('utf-8')
'''
def play_music_func():
    list_musics = glob.glob(os.path.join(os.getcwd(),'musics','*.mp3'))
    index = random.randint(0,len(list_musics)-1)
    mixer.init()
    sound = mixer.Sound(list_musics[index])
    playing = sound.play()
    return json.dumps({'status':'the music is playing'})
def encode_image(image_path=r'/home/mohammadt72/myprojects/plant/captured_image.jpg'):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
def capture_and_save_image_func(output_filename='captured_image.jpg', device_num=8):
    # Open a connection to the default camera (usually the first camera)
    cap = cv2.VideoCapture(device_num)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return json.dumps({ 'status': 'Camera is not working right now'})
    # Read a frame from the camera
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame.")
        return json.dumps({ 'status': 'Camera is not working right now'})
    encoded_image = encode_image()
    # Save the captured frame to a file
    cv2.imwrite(output_filename, frame)
    # Release the camera
    cap.release()
    return json.dumps([{'type':'text', 'text':'Describe what in the image'},{'type':'image_url','image_url':{'url':f'data:image/jpeg;base64,{encoded_image}'}}])
