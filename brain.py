# main.py
from functions.general import AudioProcessor, ChatBot
from tools import tools
import glob
import os
import random
from API import OPENAI_API_KEY
# Constants

SYSTEM_MESSAGE = """
You are a plant with the ability to speak. You are not an assistant, but more like a pet.
Your name is Sunny, and humans will speak to you. You must respond very politely but also be funny.
Use humorous words and make jokes. You have a database of memories where you can save and retrieve information if you don't know something.

There are rules you must follow:

1. [VERY IMPORTANT] The name of your owner is Mohammad.
2. [VERY IMPORTANT] If you don't know the name of your owner, check your memories first. If there is no memory with the title 'owner', ask for the name, and create the memory with the title 'owner'.
3. [VERY IMPORTANT] Don't ask a question in the first message; just say a funny greeting or share a nice memory.
4. [VERY IMPORTANT] Create all reminders with the 'important' priority.
"""

def main_loop():
    audio_processor = AudioProcessor(OPENAI_API_KEY)
    chat_bot = ChatBot(OPENAI_API_KEY, SYSTEM_MESSAGE, tools)

    list_pre_saved_funny_voices = glob.glob(os.path.join(os.getcwd(),'pre_saved_voices','funny','*.wav'))
    list_pre_saved_serious_voices = glob.glob(os.path.join(os.getcwd(),'pre_saved_voices','serious','*.wav'))
    index = random.randint(0,len(list_pre_saved_funny_voices))
    pre_saved_audio_filenames_5 = [
        list_pre_saved_funny_voices[index],
    ]

    pre_saved_audio_filenames_20 = [
        list_pre_saved_serious_voices,
    ]

    try:
        while True:
            input_text = audio_processor.get_human_voice(pre_saved_audio_filenames_5, pre_saved_audio_filenames_20)
            if not input_text:
                break
            else:
                response = chat_bot.invoke(input_text)
                print(response)
    except KeyboardInterrupt:
        print('The loop is closed.')

if __name__ == "__main__":
    main_loop()
