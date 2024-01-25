import os
import time
os.environ['OPENAI_API_KEY'] = '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'

from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai.chat_models import ChatOpenAI

from langchain.output_parsers import PydanticOutputParser
from moreMultipleCalls import BaseModel, Field, validator

# chat = ChatOpenAI(openai_api_key="...")

# If you have an envionrment variable set for OPENAI_API_KEY, you can just do:
chat = ChatOpenAI(temperature=0)

from typing import List


class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")


class Jokes(BaseModel):
    jokes: List[Joke] = Field(description="list of jokes")


# Set up a parser + inject instructions into the prompt template.
parser = PydanticOutputParser(pydantic_object=Jokes)

template = "Answer the user query.\n{format_instructions}\n{query}\n"
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])

parser.get_format_instructions()

# Set up a parser + inject instructions into the prompt template.
parser = PydanticOutputParser(pydantic_object=Jokes)

# Format the chat prompt:
messages = chat_prompt.format_prompt(
    format_instructions=parser.get_format_instructions(),
    query="What do you call a pig that does karate?",
).to_messages()

result = chat.invoke(messages)

joke_pydantic_object = parser.parse(result.content)

joke_pydantic_object.dict()

joke_pydantic_object.jokes
print()
print(joke_pydantic_object.jokes[0].setup)
time.sleep(5)
print(joke_pydantic_object.jokes[0].punchline)
print("--------------------")
print(result.content)
print()

