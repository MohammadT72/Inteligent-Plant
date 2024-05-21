from langchain.tools import BaseTool, StructuredTool, tool
from input_schema import *
from functions.general import *

# get_current_time_and_date_tool = StructuredTool.from_function(
#     func=get_current_time_and_date,
#     name="get_current_time_and_date",
#     description="This tool returns the current date and time in Tehran.",
#     args_schema=GetCurrentTimeAndDateInput
# )
# play_a_random_song = StructuredTool.from_function(
#     func=play_a_random_song,
#     name="play_a_random_song",
#     description="This tool can play a random song",
#     # rgs_schema=PlayARandomSongInput,
#     # coroutine= ... <- you can specify an async method if desired as well
# )
# play_a_song = StructuredTool.from_function(
#     func=play_a_song,
#     name="play_a_song",
#     description="This tool can play a song by it's name",
#     rgs_schema=PlayASongInput,
#     # coroutine= ... <- you can specify an async method if desired as well
# )
# check_the_time = StructuredTool.from_function(
#     func=check_the_time,
#     name="check_the_time",
#     description="This tool tell the plant current time like 10:15 PM",
#     # rgs_schema=CreateMemoryInput,
#     # coroutine= ... <- you can specify an async method if desired as well
# )
# check_the_date = StructuredTool.from_function(
#     func=check_the_date,
#     name="check_the_date",
#     description="This tool tell the plant current date",
#     # rgs_schema=CreateMemoryInput,
#     # coroutine= ... <- you can specify an async method if desired as well
# )
# create_memory = StructuredTool.from_function(
#     func=create_memory,
#     name="create_memory",
#     description="This tool can create a memory to remember important thing based on date of the moment, title, type of event, the description, and the priority",
#     rgs_schema=CreateMemoryInput,
#     # coroutine= ... <- you can specify an async method if desired as well
# )
# get_memory_by_priority = StructuredTool.from_function(
#     func=get_memory_by_priority,
#     name="get_memory_by_priority",
#     description="This tool can retrieve an specific memory by it's priority",
#     rgs_schema=GetMemoryByPriorityInput,
#     # coroutine= ... <- you can specify an async method if desired as well
# )
# get_memory_by_title = StructuredTool.from_function(
#     func=get_memory_by_title,
#     name="get_memory_by_title",
#     description="This tool can retrieve an specific memory by it's title",
#     rgs_schema=GetMemoryByTitleInput,
#     # coroutine= ... <- you can specify an async method if desired as well
# )
# get_reminders_memory = StructuredTool.from_function(
#     func=get_reminders_memory,
#     name="get_reminders_memory",
#     description="This tool can all the reminders",
#     rgs_schema=GetRemindersMemoryInput,
#     # coroutine= ... <- you can specify an async method if desired as well
# )
# get_all_memories = StructuredTool.from_function(
#     func=get_all_memories,
#     name="get_all_memories",
#     description="This tool can retrieve all memories",
#     rgs_schema=GetMemoryAllMemories,
#     # coroutine= ... <- you can specify an async method if desired as well
# )

get_sensors_data_tool = StructuredTool.from_function(
    func=get_sensors_data_func,
    name="get_sensors_data",
    description="A tool for retrieving the sensors data",
    rgs_schema=GetSensorsDataInput,
    # coroutine=get_sensors_data_async_func,
)
# get_weather_forcast = StructuredTool.from_function(
#     func=get_weather_forcast,
#     name="get_weather_forcast",
#     description="A tool that the plant can use to extract a three day weather forcast",
#     rgs_schema=GetWeatherForcastInput,
#     # coroutine= ... <- you can specify an async method if desired as well
# )
# get_human_voice = StructuredTool.from_function(
#     func=get_human_voice,
#     name="get_human_voice",
#     description="A tool that the plant can use to record to the human voice, and understand what they say",
#     # coroutine= ... <- you can specify an async method if desired as well
# )

create_plant_voice_tool = StructuredTool.from_function(
      func=create_plant_voice_func,
      name="create_plant_voice",
      description="A tool that the plant can convert the text, or it's thoughts to voice, so it can be played through speakers",
     args_schema=CreatePlantVoiceInput,
     # coroutine= ... <- you can specify an async method if desired as well
     )

# search_Arxiv = StructuredTool.from_function(
#     func=search_Arxiv,
#     name="search_Arxiv",
#     description="A tool that the plant can search scientific articles in ArXive web database",
#     args_schema=SearchArxiveInput,
#     # coroutine= ... <- you can specify an async method if desired as well
# )
