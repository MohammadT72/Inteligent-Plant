from langchain.pydantic_v1 import BaseModel, Field

# StructedTool
# class CheckDateInput(BaseModel):
#     day: str = Field(description="The day")
# Define input schema (if needed)
class GetCurrentTimeAndDateInput(BaseModel):
    dummy_field: str = Field(default="", description="A dummy field since no input is actually needed.")
class GetSensorsDataInput(BaseModel):
    dummy_field: list = Field(default=None, description="A list of sensors name which plant uses to check its health.")

class CreateMemoryInput(BaseModel):
    description: str = Field(description="The description of the moment, event or the name plant wants to remember")
    mem_type: str = Field(description="There are two types of memory: 1.moment, 2.name, 3.reminder")
    title: str = Field(description="the title of the memory so the plant can search the memories by their title")
    priority: str = Field(description="It determine how important a memory is, there are two options: 1.normal, 2.important")
class GetMemoryByPriorityInput(BaseModel):
    priority: str = Field(description="It determine how important a memory is, there are two options: 1.normal, 2.important")
class GetMemoryAllMemories(BaseModel):
    dummy_field: str = Field(default="", description="A dummy field since no input is actually needed.")
class GetMemoryByTitleInput(BaseModel):
    title: str = Field(description="It is the title of the memory that plant wants to search the database by it")
class GetRemindersMemoryInput(BaseModel):
    title: str = Field(description="It is the title reminder memories that plant wants to search the database by it")
class GetWeatherForcastInput(BaseModel):
    location: str = Field(description="The location of the weather forcast")
    day: str = Field(description="the day which the plant wants to know it's weather forcast")
class CreatePplantVoiceInput(BaseModel):
    input_text: str = Field(description="The text that plant wants to converts to speech and play it")
class SearchArxiveInput(BaseModel):
    query: str = Field(description="The query text that plant wants to search in arxiv web data base")
class PlayASongInput(BaseModel):
    name: str = Field(description="The name of the song that plant wants to play")
# class PlayARandomSongInput(BaseModel):
#     name: str = Field(description="The name of the song that plant wants to play")