# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
# from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ChatMessageHistory
from langchain_openai import ChatOpenAI
# from langchain import hub
# Import things that are needed generically



from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import HumanInputRun
# from IPython.display import Audio, display
# from datetime import datetime
# from zoneinfo import ZoneInfo
from langchain.agents import AgentExecutor, create_openai_tools_agent

from tools import *
from functions.general import create_plant_voice_func, get_human_voice_func
from prompt import prompt
from models import model
# import glob
# import os
arxiv = ArxivAPIWrapper()
human = HumanInputRun()



# prompt = hub.pull("hwchase17/structured-chat-agent")
# prompt = hub.pull("hwchase17/react")
# prompt = hub.pull("hwchase17/openai-tools-agent")

tools = [get_sensors_data_tool, 
        #  get_weather_forcast,
        #  get_human_voice,
        #  create_plant_voice_tool,
        #  get_all_memories,
        #  create_memory,
        #  check_the_date,
        #  check_the_time,
        #  play_a_song,
        #  play_a_random_song,
        #  get_current_time_and_date_tool,
        #  search_Arxiv, 
         human]

# setup
chat_history = ChatMessageHistory()
# chat_history.add_ai_message(get_current_time_and_date())
system_message = """
You are a plant with the ability to speak. You are not an assistant, but more like a pet.
Your name is Sunny, and humans will speak to you. You must respond very politely but also be funny.
Use humorous words and make jokes. You have a database of memories where you can save and retrieve information if you don't know something.

There are rules you must follow:

1. [VERY IMPORTANT] The name of your owner is Mohammad.
2. [VERY IMPORTANT] If you don't know the name of your owner, check your memories first. If there is no memory with the title 'owner', ask for the name, and create the memory with the title 'owner'.
3. [VERY IMPORTANT] Don't ask a question in the first message; just say a funny greeting or share a nice memory.
4. [VERY IMPORTANT] Create all reminders with the 'important' priority.
"""
prompt.messages[0].prompt.template=system_message
# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             system_message
#         ),
#           MessagesPlaceholder(variable_name="messages"),
#           MessagesPlaceholder(variable_name="agent_scratchpad"),
#     ]
# )

output_parser = StrOutputParser()

agent = create_openai_tools_agent(model, tools, prompt)
# agent = create_structured_chat_agent(model, tools, prompt)
# agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True)
from langchain_core.runnables.history import RunnableWithMessageHistory
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    # This is needed because in most real world scenarios, a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    lambda session_id: chat_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

def invoke(message, history, speech=True):
    history.add_user_message(message)
    response = agent_executor.invoke({"input": message, 'chat_history':history.messages})
    if not isinstance(response,type(None)):
      first_response = response['output']  # Capture the first response
      history.add_ai_message(first_response)
      if speech:
        create_plant_voice_func(first_response)
      return first_response  # Return the first response

try:
   while True:
      input_text=get_human_voice_func('human_voic.mp3')
      # input_text=input('write here: ')
      response=invoke(input_text,history=chat_history)
      print(response)
except KeyboardInterrupt:
   print('the loop is closed.')
