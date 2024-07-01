from API import OPENAI_API_KEY
from functions.general import AudioProcessor, ChatBot
import requests
import base64
import json

def encode_image(image_path=r'/home/mohammadt72/myprojects/plant/captured_image.jpg'):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
    
encoded_image = encode_image()

headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
messages = [{
	'role':'user',
	'content':[{'type':'text', 'text':'Describe what in the image'},
	{'type':'image_url','image_url':{'url':f'data:image/jpeg;base64,{encoded_image}'}}]

}]

print(json.dumps(messages[0]['content']))
'''
payload = {
            "model": "gpt-4o",
            "messages": messages,
            "temperature": 0.7,
            "n": 1,
        }
        
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())
'''
