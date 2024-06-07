import typing
import langchain_core.messages.ai
import langchain_core.messages.human
import langchain_core.messages.chat
import langchain_core.messages.system
import langchain_core.messages.function
import langchain_core.messages.tool
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate, HumanMessagePromptTemplate,SystemMessagePromptTemplate

input_variables = ['agent_scratchpad', 'input']
input_types = {
    'chat_history': typing.List[typing.Union[
        langchain_core.messages.ai.AIMessage,
        langchain_core.messages.human.HumanMessage,
        langchain_core.messages.chat.ChatMessage,
        langchain_core.messages.system.SystemMessage,
        langchain_core.messages.function.FunctionMessage,
        langchain_core.messages.tool.ToolMessage
    ]],
    'agent_scratchpad': typing.List[typing.Union[
        langchain_core.messages.ai.AIMessage,
        langchain_core.messages.human.HumanMessage,
        langchain_core.messages.chat.ChatMessage,
        langchain_core.messages.system.SystemMessage,
        langchain_core.messages.function.FunctionMessage,
        langchain_core.messages.tool.ToolMessage
    ]]
}
metadata = {
    'lc_hub_owner': 'hwchase17',
    'lc_hub_repo': 'openai-tools-agent',
    'lc_hub_commit_hash': 'c18672812789a3b9697656dd539edf0120285dcae36396d0b548ae42a4ed66f5'
}
messages = [
    SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], template='You are a helpful assistant')),
    MessagesPlaceholder(variable_name='chat_history', optional=True),
    HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], template='{input}')),
    MessagesPlaceholder(variable_name='agent_scratchpad')
]

prompt=ChatPromptTemplate(name='chat',input_variables=input_variables, input_types=input_types,
                          metadata=metadata, messages=messages)